# Contributing

## Local checks

- uvx ruff check tap_yandex_cloud tests
- uvx ruff format tap_yandex_cloud tests
- uv run pytest

## Useful commands

- build package by command: uv build
- run tests by command: uv run pytest
- run tests by command: uvx --with tox-uv tox
- format code by command: uvx ruff format tap_yandex_cloud tests
- lint code by command: uvx ruff check tap_yandex_cloud tests
- fix linter errors by command: uvx ruff check tap_yandex_cloud tests --fix
