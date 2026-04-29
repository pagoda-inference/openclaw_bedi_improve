#!/usr/bin/env python3
"""
初始化环境脚本
创建必要的目录结构和配置文件
"""

from pathlib import Path
import sys


def init_environment():
    """初始化Deep Browser环境"""
    
    # 基础目录
    base_dir = Path.home() / ".openclaw" / "deep-browser"
    patterns_dir = base_dir / "patterns"
    plans_dir = base_dir / "plans"
    
    # 创建目录
    print("创建目录结构...")
    patterns_dir.mkdir(parents=True, exist_ok=True)
    plans_dir.mkdir(parents=True, exist_ok=True)
    
    # 创建初始索引文件
    print("创建索引文件...")
    
    patterns_index = patterns_dir / "INDEX.md"
    if not patterns_index.exists():
        patterns_index.write_text(
            "# 网站模式索引\n\n"
            "| 域名 | 文件 | 页面类型 | 最后使用 | 成功率 |\n"
            "|------|------|---------|---------|--------|\n",
            encoding="utf-8"
        )
        print(f"  创建: {patterns_index}")
    
    plans_index = plans_dir / "INDEX.md"
    if not plans_index.exists():
        plans_index.write_text(
            "# 浏览计划索引\n\n"
            "| 任务ID | 目标 | 状态 | 文件 | 创建时间 |\n"
            "|--------|------|------|------|---------|\n",
            encoding="utf-8"
        )
        print(f"  创建: {plans_index}")
    
    # 检查依赖
    print("\n检查依赖...")
    
    # 检查Python版本
    py_version = sys.version_info
    print(f"  Python版本: {py_version.major}.{py_version.minor}.{py_version.micro}")
    if py_version.major < 3 or (py_version.major == 3 and py_version.minor < 8):
        print("  ⚠️  警告: 建议使用Python 3.8或更高版本")
    
    # 检查OpenCLI
    import shutil
    if shutil.which("opencli"):
        print("  ✓ OpenCLI已安装")
    else:
        print("  ⚠️  警告: OpenCLI未找到，请确保已安装并添加到PATH")
    
    print("\n✅ 初始化完成！")
    print(f"\n配置目录: {base_dir}")
    print(f"  - 网站模式: {patterns_dir}")
    print(f"  - 浏览计划: {plans_dir}")
    
    return True


if __name__ == "__main__":
    init_environment()
