# Contributing to provide-workspace

This repo is a development workspace bootstrapper — it has no source code of its own. Contributions here are limited to:

- Updating `pyproject.toml` when provide.io packages are added or renamed
- Updating `uv.lock` via `uv lock`
- Improving README or documentation

## Adding a New Ecosystem Package

1. Add the package name to `[project].dependencies` in `pyproject.toml`
1. Add a `[tool.uv.sources]` entry pointing to `repos/<name>`
1. Run `uv lock` to update the lock file
1. Update the package table in `README.md`

## Running `uv sync`

Requires all referenced repos to be present in `repos/`:

```bash
git clone git@github.com:provide-io/<name>.git repos/<name>
uv sync
```

Missing repos will cause `uv sync` to fail with a "path does not exist" error.
