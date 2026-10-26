# IoC guide

## Structure

```text
src/bootstrap/ioc/
  container.py                            create_container() lists every provider
  providers/modules/{module_name}/{layer}/...
  providers/seedwork/{layer}/...
  providers/bootstrap/...
```

`providers/` mirrors `src/` by ownership and layer. A provider file groups
wiring for one kind of component or one feature:

```text
src/modules/billing/infra/dm/...          → providers/modules/billing/infra/dm.py
src/modules/billing/infra/queries/...     → providers/modules/billing/infra/queries.py
src/modules/billing/application/use_cases → providers/modules/billing/application/use_cases.py
```

Split a provider file by feature when it grows:
`providers/modules/billing/infra/dm/payments.py`.

## Providers

```python
class BillingDmProvider(Provider):
    payment_dm = provide(
        AlchemyPaymentDm,
        provides=IPaymentDm,
        scope=Scope.REQUEST,
    )


class BillingUseCasesProvider(Provider):
    pay_order = provide(
        PayOrderUc,
        scope=Scope.REQUEST,
    )
```

- Provide the interface, not the implementation: `provides=IPaymentDm`.
- Use `Scope.APP` for settings, engine, session factory, and clients.
- Use `Scope.REQUEST` for the session and everything that depends on it:
  transaction manager, dm, queries, services, use cases.
- A provider that opens a resource yields it and closes it after `yield`.
- Add every new provider to `create_container()`.
- Do not add constructor arguments to providers for tests; tests replace
  providers in `tests/ioc/`.

Handlers receive use cases through `FromDishka[PayOrderUc]` with `@inject`.
