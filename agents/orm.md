# PostgreSQL ORM

These instructions apply to SQLAlchemy ORM models under
`src/modules/*/infra/orm/**`.

## Declaration Order

- Inside each ORM class, keep declarations grouped in this order:
  primary key columns, blank line, `relationship(...)` attributes, blank line,
  `ForeignKey(...)` columns, blank line, regular table columns.

## Module Structure

- Do not collect unrelated ORM models in one large module.
- Split ORM models by stable domain/aggregate ownership, for example
  `billing`, `subscription`, `promo`, `access`, `catalog`, and `config`.
- Keep models that form one aggregate or are changed together in the same
  module. Move cross-aggregate relationships through typed forward references
  instead of merging domains into one file.
- A legacy or package-level module may re-export models for compatibility, but
  it must not become the place where new ORM classes are implemented.

## Relationship Rules

- Keep SQLAlchemy relationships explicit with `back_populates` on both sides.
- Use database-level `ForeignKey(..., ondelete="CASCADE")` for real delete behavior.
- Add ORM `cascade` only on owner-side collection relationships, for example
  `UserOrm.subscriptions`, `UserOrm.mock_payments`, and
  `SubscriptionOrm.vpn_accesses`.
- Use `passive_deletes=True` with DB cascades so SQLAlchemy does not need to
  load child collections just to delete a parent.
- DAL queries should still filter by FK columns directly when the use-case only
  needs IDs or rows. Do not expose ORM relationship graphs outside infra.
