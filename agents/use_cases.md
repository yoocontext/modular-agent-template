# Use Cases guide

## Use Case Class Shape

Every use case must inherit from `BaseUseCase` with explicit generics:

Naming:
- `Cm` — command.
- `Rs` — result.
- `Uc` — use case.

```python
@dataclass
class ExpireSubscriptionsUc(
    BaseUseCase[ExpireSubscriptionsCm, ExpireSubscriptionsRs]
):
    _subscription_dm: ISubscriptionDm
    _transaction_manager: ITransactionManager

    async def act(
        self,
        command: ExpireSubscriptionsCm,
    ) -> ExpireSubscriptionsRs:
        ...
```

- Use `@dataclass` for dependency aggregation.
- All dependencies must be constructor-injected.
- Store dependencies as protected fields, for example `_subscription_dm: ISubscriptionDm`.

- Only use cases may call transaction `commit()`.

## Docstrings

Every use case must have a docstring.

Describe the scenario as a pipeline.

Template:

```python
"""Short scenario description.

Pipeline:
1. Load ...
2. Validate ...
3. Call ...
4. Persist ...
5. Return ...

Edge cases:
- ...
"""
```

Include:
- loads;
- validations and branches;
- ports and side effects;
- persisted changes;
- result;
- edge cases.

## File Structure

One file → one use case.

Group use cases by module.
Create entity subdirectories only when an entity has multiple use cases.

```text
use_cases/payments/create_invoice.py

use_cases/payments/invoice/create.py
use_cases/payments/invoice/delete.py
use_cases/payments/invoice/calculate_tax.py
```

Refactor freely as the domain evolves:

```text
users.py
→ use_cases/users/tax.py
→ use_cases/payments/user/tax.py
```

Do not preserve file structure for backward compatibility. Prefer correct
ownership and cohesion.


## Mapping

One use case → one mapper file.

```text
use_cases/payments/user/create.py
→ use_cases/mappers/payments/user/create.py
```

Keep mapper structure identical to use case structure.
