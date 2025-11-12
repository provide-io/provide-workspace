# Common Issues

Common problems and solutions.

## Import Errors

**Problem**: `ModuleNotFoundError: No module named 'pyvider'`

**Solution**:
```bash
source .venv/bin/activate
./scripts/setup.sh
```

## Missing Repositories

**Problem**: Some repositories not cloned

**Solution**:
```bash
./scripts/bootstrap.sh  # Safe to re-run
```

## Virtual Environment Issues

**Problem**: Wrong environment active

**Solution**:
```bash
deactivate
cd /path/to/provide-workenv
source .venv/bin/activate
```

## Documentation Status

📝 Full troubleshooting guide coming soon. See [Validation Guide](../getting-started/validation.md) for setup verification.
