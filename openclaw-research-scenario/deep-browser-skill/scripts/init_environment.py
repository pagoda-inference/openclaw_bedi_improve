#!/usr/bin/env python3
"""
初始化环境脚本
创建必要的目录结构，检查 OpenCLI 可用性
"""

from pathlib import Path
import sys
import shutil
import subprocess


def check_opencli():
    """检查 OpenCLI 是否可用"""
    if not shutil.which("opencli"):
        return False, "OpenCLI not found in PATH"

    try:
        result = subprocess.run(
            ["opencli", "doctor"],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode == 0:
            return True, "OpenCLI ready"
        else:
            return False, f"opencli doctor failed: {result.stderr.strip()}"
    except subprocess.TimeoutExpired:
        return False, "opencli doctor timed out"
    except Exception as e:
        return False, f"opencli check error: {e}"


def init_environment():
    """初始化 Deep Browser 环境"""

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
            "| Domain | File | Pattern | Last Used |\n"
            "|--------|------|---------|----------|\n",
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

    opencli_ok, opencli_msg = check_opencli()
    if opencli_ok:
        print(f"  ✓ {opencli_msg}")
    else:
        print(f"  ⚠️  Warning: {opencli_msg}")
        print("     Deep Browser requires OpenCLI for browser operations.")
        print("     Install: npm install -g @jackwener/opencli")
        print("     Fallback: OpenClaw browser tool or web-fetch")

    print("\n✅ Initialization complete!")
    print(f"\nSkill directory: {skill_dir}")
    print(f"Patterns directory: {base_dir}")
    print(f"  - Sites: {sites_dir}")
    print(f"  - Plans: {plans_dir}")
    print(f"States directory: {states_dir}")

    return True


if __name__ == "__main__":
    init_environment()
