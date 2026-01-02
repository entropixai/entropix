# Fix: ModuleNotFoundError: No module named 'flakestorm.reports'

## Problem
After running `python -m pip install .`, you get:
```
ModuleNotFoundError: No module named 'flakestorm.reports'
```

## Solution

### Step 1: Clean Previous Builds
```bash
# Remove old build artifacts
rm -rf build/ dist/ *.egg-info src/*.egg-info

# If installed, uninstall first
pip uninstall flakestorm -y
```

### Step 2: Make Sure You're in Your Virtual Environment
```bash
# Activate your venv
source venv/bin/activate  # macOS/Linux
# OR
venv\Scripts\activate      # Windows

# Verify you're in the venv
which python  # Should show venv path
```

### Step 3: Reinstall in Editable Mode
```bash
# Install in editable mode (recommended for development)
pip install -e .

# OR install normally
pip install .
```

### Step 4: Verify Installation
```bash
# Check if package is installed
pip show flakestorm

# Test the import
python -c "from flakestorm.reports.models import TestResults; print('OK')"

# Test the CLI
flakestorm --version
```

## If Still Not Working

### Check Package Contents
```bash
# List installed package files
python -c "import flakestorm; import os; print(os.path.dirname(flakestorm.__file__))"
ls -la <path_from_above>/reports/
```

### Rebuild from Scratch
```bash
# Clean everything
rm -rf build/ dist/ *.egg-info src/*.egg-info .eggs/

# Rebuild
python -m build

# Check what's in the wheel
unzip -l dist/*.whl | grep reports

# Reinstall
pip install dist/*.whl
```

## Root Cause
The `reports` module exists in the source code, but might not be included in the installed package if:
1. The package wasn't built correctly
2. You're not in the correct virtual environment
3. There's a cached/stale installation

The fix above should resolve it.
