# IoC guide


## Structure

```text
src/bootstrap/ioc/
  container.py
  providers/{module_name}/{layer}/...
```

- `{module_name}` — module name from `src/modules/`.
- `{module_name}` can be omitted if there is no `src/modules/` directory.


## Provider location rule

`src/bootstrap/ioc/providers/` mirrors `src/` by ownership and layer.
Provider files may group lifecycle wiring for a subsystem or entity instead of
matching every source file one-to-one.

Source file:

```text
src/modules/{module_name}/infra/dm/user.py
```

Provider file:

```text
src/bootstrap/ioc/providers/{module_name}/infra/dm.py
```

## Provider responsibility

A provider manages the object lifecycle.

Example:

```text
../providers/seedwork/infra/alchemy.py
```
