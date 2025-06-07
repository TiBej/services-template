`docker compose up`
http://localhost:15672

passwort / login: admin admin

install a project:

initializing:

- poetry init

```
[tool.poetry]
package-mode = false
```

```
poetry run python your_script.py
```

ruff for liniting and formatting.

"poetry new --flat name_service"

## create new service

`poetry new --flat my-package`
tests folder and readme.md can be deleted we are not using it, we are using for all projects flat layout. https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/

we are using poetry only for package-mode:

**init**.py can be deleted not anymore neccesray

```
[tool.poetry]
package-mode = false
```

ìnclude common

```
[tool.poetry.dependencies]
common = {path = '../common'}
```

All meta data under [project] can be removed from pyproject.toml
