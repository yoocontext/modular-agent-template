"""Sync generated AGENTS.md files from configured templates.

Usage:
    uv run scripts/sync_agents.py
    uv run scripts/sync_agents.py --write

By default, the script checks whether generated AGENTS.md files are in sync
with the templates configured in pyproject.toml. Pass --write to create or
update those files.
"""

from __future__ import annotations

import argparse
import sys
import tomllib
from dataclasses import dataclass
from pathlib import Path
from string import Template

ROOT = Path(__file__).resolve().parents[1]
AGENTS_FILE_NAME = "AGENTS.md"


@dataclass(frozen=True)
class AgentRule:
    template: Path
    target: str
    create: bool


@dataclass(frozen=True)
class PlannedFile:
    target: Path
    content: str


def load_rules() -> list[AgentRule]:
    pyproject = ROOT / "pyproject.toml"
    config = tomllib.loads(pyproject.read_text())
    raw_rules = config.get("tool", {}).get("project_name", {}).get("agents", [])

    rules: list[AgentRule] = []
    for raw_rule in raw_rules:
        rules.append(
            AgentRule(
                template=ROOT / raw_rule["template"],
                target=raw_rule["target"],
                create=raw_rule.get("create", False),
            )
        )
    return rules


def module_names() -> list[str]:
    modules_root = ROOT / "src" / "modules"
    if not modules_root.exists():
        return []

    return sorted(
        path.name
        for path in modules_root.iterdir()
        if path.is_dir() and not path.name.startswith("__")
    )


def render_template(template_path: Path, variables: dict[str, str]) -> str:
    content = template_path.read_text()
    rendered = Template(content).safe_substitute(variables)
    return rendered.rstrip() + "\n"


def expand_target(rule: AgentRule, module_name: str | None) -> Path:
    variables = {}
    if module_name is not None:
        variables["module_name"] = module_name

    return ROOT / rule.target.format(**variables) / AGENTS_FILE_NAME


def plan_files(rules: list[AgentRule]) -> list[PlannedFile]:
    planned: list[PlannedFile] = []
    names = module_names()

    for rule in rules:
        if "{module_name}" in rule.target:
            for name in names:
                variables = {"module_name": name}
                target = expand_target(rule, name)
                target_dir = target.parent
                if not rule.create and not target_dir.exists():
                    continue

                planned.append(
                    PlannedFile(
                        target=target,
                        content=render_template(rule.template, variables),
                    )
                )
            continue

        target = expand_target(rule, None)
        if not rule.create and not target.parent.exists():
            continue

        planned.append(
            PlannedFile(
                target=target, content=render_template(rule.template, {})
            )
        )

    return planned


def check(planned_files: list[PlannedFile]) -> int:
    stale: list[Path] = []

    for planned_file in planned_files:
        if not planned_file.target.exists():
            stale.append(planned_file.target)
            continue

        if planned_file.target.read_text() != planned_file.content:
            stale.append(planned_file.target)

    if not stale:
        return 0

    print("AGENTS.md files are out of sync. Run:")
    print()
    print("  uv run scripts/sync_agents.py --write")
    print()
    print("Stale files:")
    for path in stale:
        print(f"  {path.relative_to(ROOT)}")

    return 1


def write(planned_files: list[PlannedFile]) -> None:
    for planned_file in planned_files:
        planned_file.target.parent.mkdir(parents=True, exist_ok=True)
        planned_file.target.write_text(planned_file.content)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--write",
        action="store_true",
        help="write generated AGENTS.md files instead of checking them",
    )
    args = parser.parse_args()

    planned_files = plan_files(load_rules())

    if args.write:
        write(planned_files)
        return 0

    return check(planned_files)


if __name__ == "__main__":
    sys.exit(main())
