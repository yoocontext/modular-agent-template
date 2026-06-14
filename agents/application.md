# Application layer guide

## Module structure

- use_cases — business workflows and orchestration.
- interfaces — contracts between components.
- services — reusable logic shared across use cases.

### Interfaces

One component → one interface.

```text
infra/dm/payments/*
→ interfaces/dm/payments.py

infra/s3/*
→ interfaces/s3.py
```