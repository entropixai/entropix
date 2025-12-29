#!/usr/bin/env python3
"""
Refactoring script to rename Entropix -> FlakeStorm
This script will:
1. Rename directories and files containing 'entropix'
2. Replace all text occurrences of 'Entropix' -> 'FlakeStorm' and 'entropix' -> 'flakestorm'
3. Update imports, package names, URLs, etc.
"""

import os
import re
import shutil
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).parent

# Files and directories to skip
SKIP_PATTERNS = [
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    ".pytest_cache",
    "target",
    "dist",
    "build",
    ".mypy_cache",
    ".ruff_cache",
    "node_modules",
    "refactor_to_flakestorm.py",  # Don't refactor this script itself
]

# Text replacements: (pattern, replacement, case_sensitive)
TEXT_REPLACEMENTS = [
    # Package names
    (r"\bentropix\b", "flakestorm", False),
    (r"\bEntropix\b", "FlakeStorm", True),
    # URLs
    (r"entropix\.cloud", "flakestorm.com", False),
    (r"entropix\.dev", "flakestorm.com", False),
    (r"github\.com/entropix/entropix", "github.com/flakestorm/flakestorm", False),
    (r"github\.com/entropixai/entropix", "github.com/flakestorm/flakestorm", False),
    # PyPI
    (r"pypi\.org/project/entropix", "pypi.org/project/flakestorm", False),
    # File paths in text
    (r"entropix\.yaml", "flakestorm.yaml", False),
    (r"entropix\.py", "flakestorm.py", False),
    # Module imports
    (r"from entropix", "from flakestorm", False),
    (r"import entropix", "import flakestorm", False),
    (r"entropix\.", "flakestorm.", False),
    # CLI command
    (r"`entropix ", "`flakestorm ", False),
    (r'"entropix ', '"flakestorm ', False),
    (r"'entropix ", "'flakestorm ", False),
    # Badge text
    (r"tested%20with-entropix", "tested%20with-flakestorm", False),
]


def should_skip(path: Path) -> bool:
    """Check if a path should be skipped."""
    path_str = str(path)
    return any(pattern in path_str for pattern in SKIP_PATTERNS)


def find_files_to_rename() -> list[tuple[Path, Path]]:
    """Find all files and directories that need renaming."""
    renames = []

    # Find directories named 'entropix'
    for root, dirs, files in os.walk(BASE_DIR):
        root_path = Path(root)
        if should_skip(root_path):
            continue

        # Check directory names
        dirs_copy = dirs[:]  # Copy list to modify during iteration
        for dir_name in dirs_copy:
            if "entropix" in dir_name.lower():
                old_path = root_path / dir_name
                if not should_skip(old_path):
                    new_name = dir_name.replace("entropix", "flakestorm").replace(
                        "Entropix", "FlakeStorm"
                    )
                    new_path = root_path / new_name
                    renames.append((old_path, new_path))
                    dirs.remove(dir_name)  # Don't walk into renamed dir

        # Check file names
        for file_name in files:
            if "entropix" in file_name.lower():
                old_path = root_path / file_name
                if not should_skip(old_path):
                    new_name = file_name.replace("entropix", "flakestorm").replace(
                        "Entropix", "FlakeStorm"
                    )
                    new_path = root_path / new_name
                    renames.append((old_path, new_path))

    return renames


def replace_in_file(file_path: Path) -> bool:
    """Replace text in a file. Returns True if file was modified."""
    try:
        # Skip binary files
        if file_path.suffix in [
            ".pyc",
            ".pyo",
            ".so",
            ".dylib",
            ".dll",
            ".png",
            ".jpg",
            ".jpeg",
            ".gif",
            ".ico",
            ".pdf",
        ]:
            return False

        # Read file
        try:
            with open(file_path, encoding="utf-8") as f:
                content = f.read()
        except UnicodeDecodeError:
            # Skip binary files
            return False

        original_content = content

        # Apply all replacements
        for pattern, replacement, case_sensitive in TEXT_REPLACEMENTS:
            flags = 0 if case_sensitive else re.IGNORECASE
            content = re.sub(pattern, replacement, content, flags=flags)

        # Write back if changed
        if content != original_content:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            return True
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

    return False


def main():
    """Main refactoring function."""
    print("🔍 Finding files and directories to rename...")
    renames = find_files_to_rename()

    print(f"📝 Found {len(renames)} items to rename")
    for old, new in renames:
        print(f"  {old.relative_to(BASE_DIR)} -> {new.relative_to(BASE_DIR)}")

    # Rename files and directories (in reverse order to handle nested paths)
    renames.sort(key=lambda x: len(str(x[0])), reverse=True)

    print("\n🔄 Renaming files and directories...")
    for old_path, new_path in renames:
        if old_path.exists():
            try:
                if old_path.is_dir():
                    shutil.move(str(old_path), str(new_path))
                else:
                    old_path.rename(new_path)
                print(f"  ✓ Renamed: {old_path.relative_to(BASE_DIR)}")
            except Exception as e:
                print(f"  ✗ Error renaming {old_path}: {e}")

    # Replace text in all files
    print("\n📝 Replacing text in files...")
    modified_count = 0
    for root, dirs, files in os.walk(BASE_DIR):
        root_path = Path(root)
        if should_skip(root_path):
            continue

        for file_name in files:
            file_path = root_path / file_name
            if should_skip(file_path):
                continue

            if replace_in_file(file_path):
                modified_count += 1
                print(f"  ✓ Modified: {file_path.relative_to(BASE_DIR)}")

    print("\n✅ Refactoring complete!")
    print(f"   - Renamed {len(renames)} files/directories")
    print(f"   - Modified {modified_count} files with text replacements")
    print("\n⚠️  Please review the changes and test before committing!")


if __name__ == "__main__":
    main()
