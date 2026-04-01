# AGENTS.md

This file provides guidance for AI assistants working in this repository.

## What This Repo Is

`provide-workspace` is a development workspace bootstrapper for the provide.io ecosystem.
It is **not published to PyPI** and contains no source code. Its sole purpose is `uv sync`
to install all provide.io repos as editable local packages in one shot.

## Setup

```bash
git clone git@github.com:provide-io/provide-workspace.git
cd provide-workspace

# Clone repos into the repos/ subdirectory
for repo in \
  provide-foundation provide-testkit \
  pyvider pyvider-components pyvider-cty pyvider-hcl pyvider-rpcplugin \
  provide-foundry plating \
  flavorpack wrknv tofusoup supsrc \
  terraform-provider-pyvider; do
  git clone git@github.com:provide-io/$repo.git repos/$repo
done

uv sync
source .venv/bin/activate
```

## What's In This Repo

| File | Purpose |
|------|---------|
| `pyproject.toml` | Lists all 14 ecosystem packages as dependencies with `repos/<name>` paths |
| `uv.lock` | Pinned lock file for reproducible installs |
| `repos/` | Clone ecosystem repos here (gitignored via `repos/*/`) |

## What NOT To Do

- Do not add source code to this repo
- Do not add test suites — there is nothing to test here
- Do not publish this to PyPI
- Do not add docs build infrastructure — that belongs in `provide-foundry`
