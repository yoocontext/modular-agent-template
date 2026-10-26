"""Create a module and its configured AGENTS.md guides.

Usage:
    uv run scripts/create_module.py billing
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from sync_agents import (
    ROOT,
    AgentRule,
    PlannedFile,
    load_rules,
    render_template,
)


def validate_module_name(module_name: str) -> None:
    if re.fullmatch(r"[a-z][a-z0-9_]*", module_name) is None:
        raise ValueError(
            "module name must use snake_case and start with a lowercase letter",
        )


def plan_module_files(
    module_name: str,
    rules: list[AgentRule],
    root: Path,
) -> list[PlannedFile]:
    module_root = root / "src" / "modules" / module_name
    planned: list[PlannedFile] = []

    for rule in rules:
        if "{module_name}" not in rule.target:
            continue

        target_dir = root / rule.target.format(module_name=module_name)
        target = target_dir / "AGENTS.md"
        if not target.is_relative_to(module_root):
            continue

        planned.append(
            PlannedFile(
                target=target,
                content=render_template(
                    rule.template,
                    {"module_name": module_name},
                ),
            ),
        )

    if not planned:
        raise RuntimeError("no module AGENTS.md templates are configured")

    return planned


def create_module(
    module_name: str,
    rules: list[AgentRule],
    root: Path,
) -> list[Path]:
    validate_module_name(module_name)
    module_root = root / "src" / "modules" / module_name

    if module_root.exists():
        raise FileExistsError(f"module already exists: {module_root}")

    planned_files = plan_module_files(module_name, rules, root)
    for planned_file in planned_files:
        planned_file.target.parent.mkdir(parents=True, exist_ok=True)
        planned_file.target.write_text(planned_file.content)

    return [planned_file.target for planned_file in planned_files]


def main() -> int:
    parser = argparse.ArgumentParser(
        description="create a module with configured AGENTS.md guides",
    )
    parser.add_argument("module_name", help="module name in snake_case")
    args = parser.parse_args()

    try:
        created_files = create_module(args.module_name, load_rules(), ROOT)
    except (FileExistsError, RuntimeError, ValueError) as error:
        parser.error(str(error))

    print(f"Created module {args.module_name}:")
    for path in created_files:
        print(f"  {path.relative_to(ROOT)}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
