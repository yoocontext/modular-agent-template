# DataMapper (dm)

## Purpose

`dm` is an abstraction for interacting with the database

## Restrictions

- `commit` is forbidden in `dm`

## Mapping

- `dm` must not contain mapping details; move them to:

  ```text
  ../infra/dm/mappers/
  ```

## File Structure

- in `../dm/` and `../infra/dm/mappers/`, split files and folders by logical modules:

  ```text
  ../dm/payments/tax.py
  ../infra/dm/mappers/payments/tax.py
  ```

- and also by entity:

  ```text
  ../dm/payments/user/tax.py
  ../infra/dm/mappers/payments/user/tax.py
  ```