# Fix: `pip install .` vs `pip install -e .` Issue

## Problem

When running `python -m pip install .`, you get:
```
ModuleNotFoundError: No module named 'flakestorm.reports'
```

But `pip install -e .` works fine.

## Root Cause

This is a known issue with how `pip` builds wheels vs editable installs:
- **`pip install -e .`** (editable): Links directly to source, all files available
- **`pip install .`** (regular): Builds a wheel, which may not include all subpackages if hatchling doesn't discover them correctly

## Solutions

### Solution 1: Use Editable Mode (Recommended for Development)

```bash
pip install -e .
```

This is the recommended approach for development as it:
- Links directly to your source code
- Reflects changes immediately without reinstalling
- Includes all files and subpackages

### Solution 2: Clean Build and Reinstall

If you need to test the wheel build:

```bash
# Clean everything
rm -rf build/ dist/ *.egg-info src/*.egg-info

# Build wheel explicitly
python -m pip install build
python -m build --wheel

# Check wheel contents
unzip -l dist/*.whl | grep reports

# Install from wheel
pip install dist/*.whl
```

### Solution 3: Verify pyproject.toml Configuration

Ensure `pyproject.toml` has:

```toml
[tool.hatch.build.targets.wheel]
packages = ["src/flakestorm"]
```

Hatchling should auto-discover all subpackages, but if it doesn't, the editable install is the workaround.

## For Publishing to PyPI

When publishing to PyPI, the wheel build should work correctly because:
1. The build process is more controlled
2. All subpackages are included in the source distribution
3. The wheel is built from the source distribution

If you encounter issues when publishing, verify the wheel contents:

```bash
python -m build
unzip -l dist/*.whl | grep -E "flakestorm/.*__init__\.py"
```

All subpackages should be listed.

## Recommendation

**For development:** Always use `pip install -e .`

**For testing wheel builds:** Use `python -m build` and install from the wheel

**For publishing:** The standard `python -m build` process should work correctly
