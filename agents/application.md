# Application layer guide

## Module structure

- entities — state and invariants; see `entities/AGENTS.md`.
- use_cases — business workflows and orchestration.
- services — domain rules spanning several entities or ports.
- interfaces — ports between components, implemented in infra.
- contracts — types the module exposes through `api.py` or the event bus:
  commands, events, and their payloads.
- `api.py` — the module's in-process public API. Other modules import only
  from it.

## Where logic goes

| Component | Called by | Responsibility |
|---|---|---|
| use case | delivery, background jobs, use cases | one scenario end to end |
| service | use cases, services | domain rule over several entities or ports |
| entity | use cases, services | rules over its own state |
| dm, queries | use cases, services | data access, no decisions |

Pick the first that fits:

1. A rule over one entity's state → entity method.
2. Data access → dm or queries.
3. An external system or another module → interface in `interfaces/`,
   implemented in infra.
4. A rule or step sequence that spans several entities or ports and names a
   domain concept → service.
5. Anything else → private method of the use case.

| Logic | Goes to |
|---|---|
| `order.mark_paid(at)` | entity |
| price from order, plan, and promo | service `PricingCalculator` |
| charge a card | interface `IPaymentProvider` |
| send a receipt, only in checkout | private method of checkout use case |

## Interfaces

One component → one interface.

```text
infra/dm/payments/payment.py
→ interfaces/dm/payments/payment.py

infra/queries/billing/autopay.py
→ interfaces/queries/billing/autopay.py

infra/s3/client.py
→ interfaces/s3.py
```

See `infra/dm/AGENTS.md` and `infra/queries/AGENTS.md` for what belongs in
`dm` and what belongs in `queries`.
