#!/usr/bin/env python3
"""
清理测试生成的临时文件，并同步清理 INDEX.md 中的残留条目
Run with: python scripts/cleanup_test_files.py
"""

from pathlib import Path
import re


def cleanup_test_files():
    """清理测试生成的临时文件，并同步清理 INDEX.md 中的残留条目"""

    skill_dir = Path(__file__).parent.parent
    sites_dir = skill_dir / "browser-patterns" / "sites"
    plans_dir = skill_dir / "browser-patterns" / "plans"
    states_dir = skill_dir / "states"

    cleaned_files = []
    cleaned_index_entries = []

    # 清理 sites 目录下的测试文件
    if sites_dir.exists():
        for f in sites_dir.glob("test-*.md"):
            if f.name != "INDEX.md":
                f.unlink()
                cleaned_files.append(str(f))

    # 清理 plans 目录下的测试文件
    if plans_dir.exists():
        for f in plans_dir.glob("test-*.md"):
            if f.name != "INDEX.md":
                f.unlink()
                cleaned_files.append(str(f))

    # 清理 states 目录下的所有文件
    if states_dir.exists():
        for f in states_dir.glob("*.md"):
            f.unlink()
            cleaned_files.append(str(f))

    # 同步清理 INDEX.md 中的残留条目
    for index_dir in [sites_dir, plans_dir]:
        if not index_dir.exists():
            continue
        index_file = index_dir / "INDEX.md"
        if not index_file.exists():
            continue

        lines = index_file.read_text(encoding="utf-8").split("\n")
        new_lines = []
        header_done = False

        for line in lines:
            if line.startswith("|") and "---" in line:
                header_done = True
                new_lines.append(line)
                continue
            if not header_done:
                new_lines.append(line)
                continue

            if line.startswith("|"):
                link_match = re.search(r'\[([^\]]+)\]\(\./([^)]+)\)', line)
                if link_match:
                    linked_file = index_dir / link_match.group(2)
                    if not linked_file.exists():
                        cleaned_index_entries.append(
                            f"{index_file.name}: {link_match.group(1)}"
                        )
                        continue
            new_lines.append(line)

        index_file.write_text("\n".join(new_lines), encoding="utf-8")

    if cleaned_files:
        print(f"Cleaned {len(cleaned_files)} test files:")
        for f in cleaned_files:
            print(f"  - {f}")
    else:
        print("No test files to clean.")

    if cleaned_index_entries:
        print(f"\nCleaned {len(cleaned_index_entries)} stale index entries:")
        for e in cleaned_index_entries:
            print(f"  - {e}")
    else:
        print("No stale index entries.")

    return len(cleaned_files) + len(cleaned_index_entries)


if __name__ == "__main__":
    cleanup_test_files()
