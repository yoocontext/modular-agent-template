# Init instructions for the AI agent

If you are reading this, the AI has been initialized in the project for the first time.

Complete the following steps:

1. Add `ruff`, `pyright`, and `mypy` to the `pre-commit` hook.
2.1212 In `docker_compose/`, rename containers, aliases, volumes, and related items to match the project name.
3. After completing these steps, delete these instructions and this file.


# Project architecture
- bootstrap — application assembly and dependency wiring.
- delivery — transport layer: controllers, schemas, validation, auth.
- application — business use cases and orchestration.
- infra — external integrations and implementations.
- seedwork — shared entities, base abstractions, common infrastructure.

## Layer dependencies
- bootstrap — knows all layers
- delivery — may know only application, seedwork/delivery, seedwork/application
- application — knows only seedwork/application
- infra — knows only application contracts & interfaces, seedwork/infra
- seedwork — knows no other layer

### Import rule
- Import only layers listed above.

## Modules
- `src/modules/{module_name}` is a vertical area, not a layer.

### Module import rule
- Forbidden: `modules.{module_a}.*` imports from `modules.{module_b}.*`.
- Module communication only through HTTP or event bus contracts.

## src/bootstrap
- Assembly layer, entrypoint.
- Register all new dependencies in `bootstrap/ioc/`.
- Do not instantiate dependencies outside IoC.


## File and folder granularity

### File structure

Prefer small files.

Organize code by module, then by entity.

```text
payments/tax.py
payments/user/tax.py
```

Refactor freely as the domain evolves:

```text
users.py
→ users/tax.py
→ payments/users/tax.py
```

Do not preserve file structure for backward compatibility. Prefer correct ownership and cohesion.


## Code rules

Do not create `helpers` or `utils` modules.

Avoid nested classes and nested functions.

Do not introduce constants for configuration values.
Use `settings` sourced from `.env` or `config.toml`.
