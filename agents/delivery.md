# Delivery layer guide

```text
/api/v{version}/{transport}/
```

Examples:

```text
/api/v1/http/
/api/v1/grpc/
/api/v1/events/
```

- `handlers.py` → few endpoints.
- `handlers/` → multiple entities or modules.
- `schemas/{endpoint}.py`
- `mappers/{endpoint}.py`

Use matching names for endpoint, schema, and mapper files.