# bootstrap.sh Reference

📝 Detailed documentation coming soon.

## Quick Usage

```bash
./scripts/bootstrap.sh
```

Clones all ecosystem repositories as siblings to provide-workenv.

## Options

Run `./scripts/bootstrap.sh --help` for options.

## What It Does

1. Reads `wrknv.toml` to find all sibling repositories
2. Checks if each repository exists
3. Clones missing repositories using `gh` or `git`
4. Skips existing directories (idempotent)

##See Also

- [Installation Guide](../getting-started/installation.md)
- [wrknv Integration](../architecture/wrknv-integration.md)
