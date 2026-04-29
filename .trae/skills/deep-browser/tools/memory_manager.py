#!/usr/bin/env python3
"""
Memory Manager
管理网站模式和浏览计划的Markdown记忆系统
"""

import json
from typing import Dict, Any, List, Optional
from pathlib import Path
from datetime import datetime
import re


class MemoryManager:
    """记忆管理器"""
    
    def __init__(self, base_dir: Optional[Path] = None):
        if base_dir is None:
            base_dir = Path.home() / ".openclaw" / "deep-browser"
        
        self.base_dir = Path(base_dir)
        self.patterns_dir = self.base_dir / "patterns"
        self.plans_dir = self.base_dir / "plans"
        
        # 确保目录存在
        self.patterns_dir.mkdir(parents=True, exist_ok=True)
        self.plans_dir.mkdir(parents=True, exist_ok=True)
    
    def save_site_pattern(self, pattern: Dict[str, Any]) -> Path:
        """保存网站模式"""
        domain = pattern.get("domain", "unknown")
        file_path = self.patterns_dir / f"{domain}.md"
        
        content = self._format_pattern_md(pattern)
        file_path.write_text(content, encoding="utf-8")
        
        # 更新索引
        self._update_patterns_index(pattern)
        
        return file_path
    
    def load_site_pattern(self, domain: str) -> Optional[Dict[str, Any]]:
        """加载网站模式"""
        file_path = self.patterns_dir / f"{domain}.md"
        
        if not file_path.exists():
            return None
        
        content = file_path.read_text(encoding="utf-8")
        return self._parse_pattern_md(content)
    
    def save_browsing_plan(self, plan: Dict[str, Any]) -> Path:
        """保存浏览计划"""
        plan_id = plan.get("id", "unknown")
        file_path = self.plans_dir / f"{plan_id}.md"
        
        content = self._format_plan_md(plan)
        file_path.write_text(content, encoding="utf-8")
        
        # 更新索引
        self._update_plans_index(plan)
        
        return file_path
    
    def load_browsing_plan(self, plan_id: str) -> Optional[Dict[str, Any]]:
        """加载浏览计划"""
        file_path = self.plans_dir / f"{plan_id}.md"
        
        if not file_path.exists():
            return None
        
        content = file_path.read_text(encoding="utf-8")
        return self._parse_plan_md(content)
    
    def list_patterns(self) -> List[Dict[str, Any]]:
        """列出所有网站模式"""
        index_path = self.patterns_dir / "INDEX.md"
        
        if not index_path.exists():
            return []
        
        content = index_path.read_text(encoding="utf-8")
        return self._parse_index_md(content)
    
    def list_plans(self) -> List[Dict[str, Any]]:
        """列出所有浏览计划"""
        index_path = self.plans_dir / "INDEX.md"
        
        if not index_path.exists():
            return []
        
        content = index_path.read_text(encoding="utf-8")
        return self._parse_index_md(content)
    
    def _format_pattern_md(self, pattern: Dict[str, Any]) -> str:
        """格式化网站模式为Markdown"""
        lines = [
            f"# {pattern.get('domain', 'unknown')}",
            "",
            f"> 域名: {pattern.get('domain', '')}",
            f"> 学习时间: {pattern.get('learned_at', datetime.now().isoformat())}",
            f"> 最后使用: {pattern.get('last_used', datetime.now().isoformat())}",
            f"> 成功次数: {pattern.get('success_count', 0)}",
            f"> 失败次数: {pattern.get('failure_count', 0)}",
            "",
            "## 页面类型",
            ""
        ]
        
        # 添加页面类型
        for type_name, type_data in pattern.get("page_types", {}).items():
            lines.append(f"### {type_name}")
            lines.append("")
            
            # 识别特征
            if type_data.get("indicators"):
                lines.append("**识别特征**：")
                for indicator in type_data["indicators"]:
                    lines.append(f"- {indicator}")
                lines.append("")
            
            # 数据区域
            if type_data.get("data_regions"):
                lines.append("**数据区域**：")
                lines.append("")
                lines.append("| 选择器 | 类型 | 说明 |")
                lines.append("|--------|------|------|")
                for region in type_data["data_regions"]:
                    lines.append(f"| {region.get('selector', '')} | {region.get('type', '')} | |")
                lines.append("")
            
            # 分页机制
            if type_data.get("pagination"):
                pagination = type_data["pagination"]
                lines.append("**分页机制**：")
                lines.append(f"- 类型: {pagination.get('type', '')}")
                lines.append(f"- 选择器: {pagination.get('selector', '')}")
                lines.append("")
        
        # 添加选择器
        if pattern.get("selectors"):
            lines.append("## 选择器")
            lines.append("")
            lines.append("| 名称 | 选择器 |")
            lines.append("|------|--------|")
            for name, selector in pattern["selectors"].items():
                lines.append(f"| {name} | {selector} |")
            lines.append("")
        
        return "\n".join(lines)
    
    def _parse_pattern_md(self, content: str) -> Dict[str, Any]:
        """解析Markdown格式的网站模式"""
        pattern = {
            "id": "",
            "domain": "",
            "page_types": {},
            "navigation_flows": [],
            "data_endpoints": [],
            "selectors": {},
            "learned_at": "",
            "last_used": "",
            "success_count": 0,
            "failure_count": 0
        }
        
        lines = content.split("\n")
        current_section = ""
        current_page_type = ""
        
        for line in lines:
            if line.startswith("# "):
                pattern["domain"] = line[2:].strip()
                pattern["id"] = pattern["domain"]
            elif line.startswith("> 域名:"):
                pattern["domain"] = line.split(":", 1)[1].strip()
            elif line.startswith("> 学习时间:"):
                pattern["learned_at"] = line.split(":", 1)[1].strip()
            elif line.startswith("> 最后使用:"):
                pattern["last_used"] = line.split(":", 1)[1].strip()
            elif line.startswith("> 成功次数:"):
                pattern["success_count"] = int(line.split(":", 1)[1].strip() or 0)
            elif line.startswith("> 失败次数:"):
                pattern["failure_count"] = int(line.split(":", 1)[1].strip() or 0)
            elif line.startswith("### "):
                current_page_type = line[4:].split("（")[0].strip()
                current_section = "page_type"
                pattern["page_types"][current_page_type] = {
                    "type": current_page_type,
                    "indicators": [],
                    "data_regions": []
                }
            elif line.startswith("## "):
                current_section = line[3:].lower().replace(" ", "_")
        
        return pattern
    
    def _format_plan_md(self, plan: Dict[str, Any]) -> str:
        """格式化浏览计划为Markdown"""
        lines = [
            f"# 浏览计划: {plan.get('goal', '')}",
            "",
            f"> 任务ID: {plan.get('id', '')}",
            f"> 目标: {plan.get('goal', '')}",
            f"> 当前深度: {plan.get('current_depth', 0)}",
            f"> 最大深度: {plan.get('max_depth', 3)}",
            f"> 状态: {plan.get('status', 'pending')}",
            f"> 创建时间: {plan.get('created_at', datetime.now().isoformat())}",
            "",
            "## 进度概览",
            "",
            f"- 总步骤: {len(plan.get('steps', []))}",
            f"- 已完成: {len([s for s in plan.get('steps', []) if s.get('status') == 'completed'])}",
            f"- 进行中: {len([s for s in plan.get('steps', []) if s.get('status') == 'in_progress'])}",
            f"- 待执行: {len([s for s in plan.get('steps', []) if s.get('status') == 'pending'])}",
            "",
            "## 执行步骤",
            ""
        ]
        
        # 添加步骤
        for step in plan.get("steps", []):
            status_icon = {
                "completed": "✅",
                "in_progress": "🔄",
                "failed": "❌",
                "pending": "⏳"
            }.get(step.get("status", "pending"), "⏳")
            
            status_text = {
                "completed": "已完成",
                "in_progress": "进行中",
                "failed": "失败",
                "pending": "待执行"
            }.get(step.get("status", "pending"), "待执行")
            
            lines.append(f"### Step {step.get('id', '').replace('step-', '')}: {step.get('description', '')} {status_icon}")
            lines.append("")
            lines.append(f"- 状态: {status_text}")
            lines.append(f"- 操作: {step.get('action', '')}")
            lines.append(f"- 参数: {json.dumps(step.get('params', {}), ensure_ascii=False)}")
            
            if step.get("dependencies"):
                lines.append(f"- 依赖: {', '.join(step['dependencies'])}")
            
            lines.append(f"- 预期: {step.get('expected_outcome', '')}")
            
            if step.get("executed_at"):
                lines.append(f"- 执行时间: {step['executed_at']}")
            
            lines.append("")
        
        return "\n".join(lines)
    
    def _parse_plan_md(self, content: str) -> Dict[str, Any]:
        """解析Markdown格式的浏览计划"""
        plan = {
            "id": "",
            "goal": "",
            "current_depth": 0,
            "max_depth": 3,
            "steps": [],
            "completed_steps": [],
            "current_step": None,
            "collected_data": [],
            "created_at": "",
            "status": "pending"
        }
        
        lines = content.split("\n")
        current_step = None
        
        for line in lines:
            if line.startswith("> 任务ID:"):
                plan["id"] = line.split(":", 1)[1].strip()
            elif line.startswith("> 目标:"):
                plan["goal"] = line.split(":", 1)[1].strip()
            elif line.startswith("> 当前深度:"):
                plan["current_depth"] = int(line.split(":", 1)[1].strip() or 0)
            elif line.startswith("> 最大深度:"):
                plan["max_depth"] = int(line.split(":", 1)[1].strip() or 3)
            elif line.startswith("> 状态:"):
                plan["status"] = line.split(":", 1)[1].strip()
            elif line.startswith("> 创建时间:"):
                plan["created_at"] = line.split(":", 1)[1].strip()
            elif line.startswith("### Step "):
                if current_step:
                    plan["steps"].append(current_step)
                
                match = re.match(r"### Step (\d+): (.+?)(?:\s*(✅|🔄|⏳|❌))?$", line)
                if match:
                    status_map = {
                        "✅": "completed",
                        "🔄": "in_progress",
                        "❌": "failed",
                        "⏳": "pending"
                    }
                    
                    current_step = {
                        "id": f"step-{match.group(1)}",
                        "description": match.group(2).strip(),
                        "action": "",
                        "params": {},
                        "dependencies": [],
                        "status": status_map.get(match.group(3), "pending"),
                        "retry_count": 0,
                        "max_retries": 3,
                        "expected_outcome": ""
                    }
            elif current_step:
                if line.startswith("- 操作:"):
                    current_step["action"] = line.split(":", 1)[1].strip()
                elif line.startswith("- 参数:"):
                    try:
                        current_step["params"] = json.loads(line.split(":", 1)[1].strip())
                    except:
                        pass
                elif line.startswith("- 依赖:"):
                    current_step["dependencies"] = [
                        d.strip() for d in line.split(":", 1)[1].split(",") if d.strip()
                    ]
        
        if current_step:
            plan["steps"].append(current_step)
        
        plan["completed_steps"] = [
            s["id"] for s in plan["steps"] if s.get("status") == "completed"
        ]
        plan["current_step"] = next(
            (s["id"] for s in plan["steps"] if s.get("status") == "in_progress"),
            None
        )
        
        return plan
    
    def _update_patterns_index(self, pattern: Dict[str, Any]):
        """更新网站模式索引"""
        index_path = self.patterns_dir / "INDEX.md"
        
        # 读取现有索引
        entries = self.list_patterns()
        
        # 更新或添加条目
        domain = pattern.get("domain", "")
        success_count = pattern.get("success_count", 0)
        failure_count = pattern.get("failure_count", 0)
        success_rate = (
            f"{int(success_count / (success_count + failure_count) * 100)}%"
            if success_count + failure_count > 0
            else "N/A"
        )
        
        new_entry = {
            "domain": domain,
            "file": f"{domain}.md",
            "page_types": list(pattern.get("page_types", {}).keys()),
            "last_used": pattern.get("last_used", datetime.now().isoformat()).split("T")[0],
            "success_rate": success_rate
        }
        
        # 查找并更新
        found = False
        for i, entry in enumerate(entries):
            if entry.get("domain") == domain:
                entries[i] = new_entry
                found = True
                break
        
        if not found:
            entries.append(new_entry)
        
        # 写入索引
        lines = [
            "# 网站模式索引",
            "",
            "| 域名 | 文件 | 页面类型 | 最后使用 | 成功率 |",
            "|------|------|---------|---------|--------|"
        ]
        
        for entry in entries:
            lines.append(
                f"| {entry.get('domain', '')} | "
                f"[{entry.get('file', '')}](./{entry.get('file', '')}) | "
                f"{', '.join(entry.get('page_types', []))} | "
                f"{entry.get('last_used', '')} | "
                f"{entry.get('success_rate', '')} |"
            )
        
        index_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    
    def _update_plans_index(self, plan: Dict[str, Any]):
        """更新浏览计划索引"""
        index_path = self.plans_dir / "INDEX.md"
        
        # 读取现有索引
        entries = self.list_plans()
        
        # 更新或添加条目
        plan_id = plan.get("id", "")
        goal = plan.get("goal", "")
        if len(goal) > 30:
            goal = goal[:30] + "..."
        
        new_entry = {
            "id": plan_id,
            "goal": goal,
            "status": plan.get("status", "pending"),
            "created": plan.get("created_at", datetime.now().isoformat()).split("T")[0]
        }
        
        # 查找并更新
        found = False
        for i, entry in enumerate(entries):
            if entry.get("id") == plan_id:
                entries[i] = new_entry
                found = True
                break
        
        if not found:
            entries.append(new_entry)
        
        # 写入索引
        lines = [
            "# 浏览计划索引",
            "",
            "| 任务ID | 目标 | 状态 | 文件 | 创建时间 |",
            "|--------|------|------|------|---------|"
        ]
        
        for entry in entries:
            lines.append(
                f"| {entry.get('id', '')} | "
                f"{entry.get('goal', '')} | "
                f"{entry.get('status', '')} | "
                f"[{entry.get('id', '')}.md](./{entry.get('id', '')}.md) | "
                f"{entry.get('created', '')} |"
            )
        
        index_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    
    def _parse_index_md(self, content: str) -> List[Dict[str, Any]]:
        """解析索引Markdown"""
        entries = []
        lines = content.split("\n")
        
        for line in lines:
            if line.startswith("|") and not line.startswith("|---") and not line.startswith("| 域名") and not line.startswith("| 任务ID"):
                cells = [cell.strip() for cell in line.split("|") if cell.strip()]
                if cells:
                    entries.append({
                        "field_{}".format(i): cell
                        for i, cell in enumerate(cells)
                    })
        
        return entries


if __name__ == "__main__":
    # 测试代码
    manager = MemoryManager()
    
    # 测试保存网站模式
    test_pattern = {
        "domain": "example.com",
        "page_types": {
            "listing": {
                "type": "listing",
                "indicators": ["商品列表布局", "分页控件存在"],
                "data_regions": [
                    {"selector": ".product-list", "type": "product-list"}
                ],
                "pagination": {"type": "click", "selector": ".next-page"}
            }
        },
        "selectors": {
            "search_box": "#search",
            "submit_button": ".search-btn"
        },
        "learned_at": datetime.now().isoformat(),
        "last_used": datetime.now().isoformat(),
        "success_count": 5,
        "failure_count": 0
    }
    
    path = manager.save_site_pattern(test_pattern)
    print(f"Pattern saved to: {path}")
    
    # 测试加载
    loaded = manager.load_site_pattern("example.com")
    print(f"Loaded pattern: {loaded.get('domain')}")
    
    # 测试列表
    patterns = manager.list_patterns()
    print(f"Total patterns: {len(patterns)}")
