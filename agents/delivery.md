# Delivery layer guide

## Structure

```text
api/v{version}/{transport}/
```

Examples:

```text
api/v1/http/
api/v1/grpc/
api/v1/events/
```

- `handlers.py` → few endpoints.
- `handlers/` → multiple entities or workflows.
- `schemas/{endpoint}.py`
- `mappers/{endpoint}.py`

Use matching names for endpoint, schema, and mapper files.

## Handlers

A handler only calls a use case:

```text
request schema → mapper → Cm → use case → Rs → mapper → response schema
```

- No business logic. Do not call dm, queries, or services; reads go through
  use cases too.
- Do not call `commit()` or `rollback()` in handlers.
