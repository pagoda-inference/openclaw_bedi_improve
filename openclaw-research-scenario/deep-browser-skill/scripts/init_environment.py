#!/usr/bin/env python3
"""
初始化环境脚本
创建必要的目录结构和配置文件
"""

from pathlib import Path
import sys


def init_environment():
    """初始化Deep Browser环境"""
    
    # Path(__file__) = init_environment.py
    # .parent = scripts/
    # .parent.parent = deep-browser/ (skill根目录)
    skill_dir = Path(__file__).parent.parent
    base_dir = skill_dir / "browser-patterns"
    sites_dir = base_dir / "sites"
    plans_dir = base_dir / "plans"
    states_dir = skill_dir / "states"
    
    print("Creating directory structure...")
    sites_dir.mkdir(parents=True, exist_ok=True)
    plans_dir.mkdir(parents=True, exist_ok=True)
    states_dir.mkdir(parents=True, exist_ok=True)
    
    print("Creating index files...")
    
    sites_index = sites_dir / "INDEX.md"
    if not sites_index.exists():
        sites_index.write_text(
            "# Website Patterns Index\n\n"
            "| Domain | File | Page Types | Last Used | Success Rate |\n"
            "|--------|------|------------|-----------|--------------|\n",
            encoding="utf-8"
        )
        print(f"  Created: {sites_index}")
    
    plans_index = plans_dir / "INDEX.md"
    if not plans_index.exists():
        plans_index.write_text(
            "# Browsing Plans Index\n\n"
            "| Task ID | Goal | Status | File | Created |\n"
            "|---------|------|--------|------|---------|\n",
            encoding="utf-8"
        )
        print(f"  Created: {plans_index}")
    
    print("\nChecking dependencies...")
    
    py_version = sys.version_info
    print(f"  Python version: {py_version.major}.{py_version.minor}.{py_version.micro}")
    if py_version.major < 3 or (py_version.major == 3 and py_version.minor < 8):
        print("  ⚠️  Warning: Python 3.8+ recommended")
    
    import shutil
    if shutil.which("opencli"):
        print("  ✓ OpenCLI installed")
    else:
        print("  ⚠️  Warning: OpenCLI not found in PATH")
    
    print("\n✅ Initialization complete!")
    print(f"\nSkill directory: {skill_dir}")
    print(f"Patterns directory: {base_dir}")
    print(f"  - Sites: {sites_dir}")
    print(f"  - Plans: {plans_dir}")
    print(f"States directory: {states_dir}")
    
    return True


if __name__ == "__main__":
    init_environment()
