# provide-workspace

Development workspace bootstrapper for the provide.io ecosystem.

Clone the repos you need into the `repos/` subdirectory, run `uv sync` once, and every package is installed as an editable local install — changes you make to any repo are immediately reflected without reinstalling.

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

> **Future:** `git submodule add git@github.com:provide-io/pyvider.git repos/pyvider` will work transparently once submodules are adopted.

## Ecosystem Packages

### Foundation

| Package                                                                | Description                                                                |
| ---------------------------------------------------------------------- | -------------------------------------------------------------------------- |
| [provide-foundation](https://github.com/provide-io/provide-foundation) | Core library: structured logging, telemetry, config, resilience primitives |
| [provide-testkit](https://github.com/provide-io/provide-testkit)       | Testing utilities and fixtures for provide.io packages                     |

### Pyvider Framework

| Package                                                                                | Description                           |
| -------------------------------------------------------------------------------------- | ------------------------------------- |
| [pyvider](https://github.com/provide-io/pyvider)                                       | Core Terraform provider framework     |
| [pyvider-cty](https://github.com/provide-io/pyvider-cty)                               | CTY type system implementation        |
| [pyvider-hcl](https://github.com/provide-io/pyvider-hcl)                               | HCL parsing with CTY integration      |
| [pyvider-rpcplugin](https://github.com/provide-io/pyvider-rpcplugin)                   | gRPC plugin protocol implementation   |
| [pyvider-components](https://github.com/provide-io/pyvider-components)                 | Standard reusable provider components |
| [terraform-provider-pyvider](https://github.com/provide-io/terraform-provider-pyvider) | Official Pyvider Terraform provider   |

### Documentation

| Package                                                          | Description                                                             |
| ---------------------------------------------------------------- | ----------------------------------------------------------------------- |
| [provide-foundry](https://github.com/provide-io/provide-foundry) | Shared MkDocs theme, plugins, and doc infrastructure                    |
| [plating](https://github.com/provide-io/plating)                 | Auto-generates Terraform Registry documentation from pyvider components |

### Tools

| Package                                                | Description                                                 |
| ------------------------------------------------------ | ----------------------------------------------------------- |
| [flavorpack](https://github.com/provide-io/flavorpack) | PSPF packaging system for self-contained executable bundles |
| [wrknv](https://github.com/provide-io/wrknv)           | Task runner and work environment management                 |
| [tofusoup](https://github.com/provide-io/tofusoup)     | Cross-language conformance testing for Terraform providers  |
| [supsrc](https://github.com/provide-io/supsrc)         | Automated Git commit/push utility                           |

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                      Tools Layer                        │
│   flavorpack │ wrknv │ plating │ tofusoup │ supsrc      │
├─────────────────────────────────────────────────────────┤
│                    Framework Layer                      │
│   pyvider │ pyvider-cty │ pyvider-hcl │ pyvider-*       │
├─────────────────────────────────────────────────────────┤
│                   Foundation Layer                      │
│         provide-foundation │ provide-testkit            │
└─────────────────────────────────────────────────────────┘
```

## License

Apache-2.0. See individual package repos for details.
