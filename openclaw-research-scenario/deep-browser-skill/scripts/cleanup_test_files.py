#!/usr/bin/env python3
"""
清理测试生成的临时文件
Run with: python scripts/cleanup_test_files.py
"""

from pathlib import Path
import shutil


def cleanup_test_files():
    """清理测试生成的临时文件"""
    
    skill_dir = Path(__file__).parent.parent
    sites_dir = skill_dir / "browser-patterns" / "sites"
    plans_dir = skill_dir / "browser-patterns" / "plans"
    states_dir = skill_dir / "states"
    
    cleaned = []
    
    # 清理 sites 目录下的测试文件
    if sites_dir.exists():
        for f in sites_dir.glob("test-*.md"):
            if f.name != "INDEX.md":
                f.unlink()
                cleaned.append(str(f))
    
    # 清理 plans 目录下的测试文件
    if plans_dir.exists():
        for f in plans_dir.glob("test-*.md"):
            if f.name != "INDEX.md":
                f.unlink()
                cleaned.append(str(f))
    
    # 清理 states 目录下的所有文件
    if states_dir.exists():
        for f in states_dir.glob("*.md"):
            f.unlink()
            cleaned.append(str(f))
    
    if cleaned:
        print(f"Cleaned {len(cleaned)} test files:")
        for f in cleaned:
            print(f"  - {f}")
    else:
        print("No test files to clean.")
    
    return len(cleaned)


if __name__ == "__main__":
    cleanup_test_files()
