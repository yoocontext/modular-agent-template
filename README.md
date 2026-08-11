# Modular Agent Template

Python 3.12 scaffold for a modular application with strict layer boundaries,
dependency injection, generated `AGENTS.md` guides, Docker Compose services,
and pre-commit quality checks.

## Start a project

1. Create a repository with **Use this template**.
2. Replace `project-name` (slugs, images, services) and `project_name`
   (Python/TOML/database identifiers) with the real project name.
3. Update the root `AGENTS.md` initialization checklist if the project needs
   additional bootstrap steps; keep the file in the repository.
4. Install the toolchain and hooks:

   ```bash
   uv sync --all-groups
   uv run pre-commit install
   ```

5. Create `.dev.env`. The Compose files expect at least:

   ```dotenv
   APP_PORT=8003

   PG__PORT=5432
   PG__DB=project_name
   PG__USER=project_name
   PG__PASSWORD=change-me
   PGADMIN_EMAIL=admin@example.com
   PGADMIN_PASSWORD=change-me
   PGADMIN_PORT=5050

   REDIS__PORT=6379
   REDIS__PASSWORD=change-me

   MINIO__API_PORT=9000
   MINIO__CONSOLE_PORT=9001
   MINIO__ROOT_USER=minioadmin
   MINIO__ROOT_PASSWORD=change-me
   ```

6. Add the project-specific `Dockerfile` and
   `src/bootstrap/main.py:create_app` entrypoint before running the app
   container. They are intentionally not implemented by this scaffold.

## Daily commands

```bash
just pg redis minio                 # start infrastructure
just pg-down redis-down minio-down  # stop infrastructure
just app                            # build/start the implemented app

uv run pre-commit run --all-files   # Ruff, mypy, pyright, AGENTS sync
uv run pytest                       # tests
```

RabbitMQ is not included in Compose; provide a broker and configure
`RMQ__RABBIT_BROKER_URL` when the application uses FastStream.

## Add a module

Replace `billing` with the module name, create the configured layer
directories, then generate their local architecture guides:

```bash
mkdir -p \
  src/modules/billing/application/use_cases \
  src/modules/billing/delivery \
  src/modules/billing/infra/dm \
  src/modules/billing/infra/orm

uv run scripts/sync_agents.py --write
uv run scripts/sync_agents.py
```

Commit the generated `AGENTS.md` files with the module. Configuration lives in
`[[tool.project_name.agents]]` inside `pyproject.toml`; templates live in
`agents/`.

## Architecture

| Layer | May depend on |
| --- | --- |
| `bootstrap` | all layers; owns assembly and IoC |
| `delivery` | `application`, `seedwork/delivery`, `seedwork/application` |
| `application` | `seedwork/application` |
| `infra` | application contracts and `seedwork/infra` |
| `seedwork` | no project layer |

`src/modules/{module_name}` is a vertical area, not a layer. Direct imports
between different modules are forbidden; communicate through HTTP or event-bus
contracts. Register every dependency in `src/bootstrap/ioc/`.
