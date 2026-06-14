# Tests guide

## Structure

```text
tests/{module_name}/{test_type_name}/...
tests/mocks/{module_name}/{layer}/
tests/ioc/
  container.py
  providers/
```

`tests/ioc/container.py` overrides the real IoC container and replaces real implementations with mocks.

- `{module_name}` — module name from `src/modules/`.
- `{module_name}` can be omitted if there is no `src/modules/` directory.
- `{test_type_name}` — `unit`, `integration`, `e2e`.
- `{layer}` — `delivery`, `infra`, `application`, `domain`.

## Test types

- `unit` — tests one function / class in isolation.
- `integration` — tests several parts together.
- `e2e` — tests a full scenario through an external entry point.

## Grouping

Group files by meaning or entity.

Bad:

```text
test_create_duble_user.py
test_update_user.py
```

Good:

```text
user/test_create_duble.py
user/test_update.py
```