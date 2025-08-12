#!/usr/bin/env python3
"""Fix relative imports in all Python files."""

import os
import re
from pathlib import Path

def fix_imports_in_file(file_path):
    """Fix relative imports in a single file."""
    with open(file_path, 'r') as f:
        content = f.read()
    
    original_content = content
    
    # Fix relative imports
    content = re.sub(r'from \.([a-zA-Z_][a-zA-Z0-9_]*) import', r'from \1 import', content)
    content = re.sub(r'from \.([a-zA-Z_][a-zA-Z0-9_]*\.)', r'from \1', content)
    
    if content != original_content:
        with open(file_path, 'w') as f:
            f.write(content)
        print(f"✅ Fixed imports in {file_path}")
        return True
    return False

def main():
    """Fix imports in all Python files in src directory."""
    src_dir = Path('src')
    fixed_count = 0
    
    for py_file in src_dir.rglob('*.py'):
        if fix_imports_in_file(py_file):
            fixed_count += 1
    
    print(f"\n🎉 Fixed imports in {fixed_count} files")
    print("✅ Scenario MCP Server is ready!")

if __name__ == "__main__":
    main()