# Modular Agent Template

A Python 3.12 foundation for modular backend applications. It provides the
project structure, dependency rules, Docker Compose infrastructure, dependency
injection, and code-quality checks; the application itself is added on top of
this foundation.

Architecture rules for coding agents live in `AGENTS.md`. The root file contains
project-wide rules, while files inside specific directories add instructions for
the layer or module an agent is currently working with.

## Synchronizing agent instructions

`scripts/sync_agents.py` reads the `[[tool.project_name.agents]]` configuration
from `pyproject.toml`, renders templates from `agents/`, and keeps the generated
`AGENTS.md` files in sync. It only generates module guides for configured
directories that already exist, unless the rule sets `create = true`.

```bash
uv run scripts/sync_agents.py --write  # create or update generated guides
uv run scripts/sync_agents.py          # check that guides are up to date
```

## Adding a module

`scripts/create_module.py` creates `src/modules/{module_name}` with every
configured layer directory and its `AGENTS.md` guide:

```bash
uv run scripts/create_module.py billing
uv run scripts/sync_agents.py --write
```

Commit the generated `AGENTS.md` files with the module.

The check is also part of pre-commit, preventing outdated generated guides from
being committed.

## Development

```bash
uv sync --all-groups
uv run pre-commit install

just pg redis minio                 # start infrastructure
just pg-down redis-down minio-down  # stop infrastructure
uv run pre-commit run --all-files   # run project checks
uv run pytest                       # run tests
```
