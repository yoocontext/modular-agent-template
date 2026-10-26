# Use Cases guide

A use case runs one scenario end to end. See "Where logic goes" in
`application/AGENTS.md`.

## Shape

```python
@dataclass
class ExpireSubscriptionsUc(
    BaseUc[ExpireSubscriptionsCm, ExpireSubscriptionsRs],
):
    _subscription_dm: ISubscriptionDm
    _transaction_manager: ITransactionManager

    async def act(
        self,
        *,
        command: ExpireSubscriptionsCm,
    ) -> ExpireSubscriptionsRs:
        ...
```

- One file holds the command `XCm`, the result `XRs`, and the use case `XUc`.
- Declare `Cm` and `Rs` with `@dataclass(frozen=True, slots=True,
  kw_only=True)` and inherit `BaseCm` and `BaseRs`.
- Inherit `BaseUc[XCm, XRs]`. Use `None` as the result type when nothing
  is returned.
- Declare the use case as a `@dataclass` and inject dependencies as protected
  fields: `_subscription_dm: ISubscriptionDm`.

## Mapping

- Build `Rs` in the use case when it only passes fields.
- Move mapping with nested results, collections, or computed values into a
  mapper that mirrors the use case path:

  ```text
  use_cases/payments/invoice/create.py
  → use_cases/mappers/payments/invoice/create.py
  ```

## File structure

One file → one use case. Group by feature; create entity subdirectories only
when an entity has several use cases.

```text
use_cases/payments/create_invoice.py
use_cases/payments/invoice/create.py
use_cases/payments/invoice/delete.py
```

Queries follow this grouping, see `infra/queries/AGENTS.md`.
