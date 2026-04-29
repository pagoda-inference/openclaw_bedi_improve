#!/usr/bin/env python3
"""
LLM Analyzer
使用LLM进行页面分析、元素交互性检测和网络请求分析
"""

import subprocess
import json
import hashlib
import time
from typing import Dict, Any, List, Optional
from pathlib import Path


class LLMAnalyzer:
    """LLM分析器"""
    
    def __init__(self, cache_ttl: int = 300):
        self.cache_ttl = cache_ttl
        self.cache: Dict[str, Dict[str, Any]] = {}
    
    def _hash_content(self, content: str) -> str:
        """生成内容哈希"""
        return hashlib.md5(content.encode()).hexdigest()
    
    def _get_cached(self, key: str) -> Optional[Any]:
        """获取缓存"""
        if key in self.cache:
            cached = self.cache[key]
            if time.time() - cached["timestamp"] < self.cache_ttl:
                return cached["result"]
        return None
    
    def _set_cache(self, key: str, result: Any):
        """设置缓存"""
        self.cache[key] = {
            "result": result,
            "timestamp": time.time()
        }
    
    def _call_llm(self, prompt: str) -> str:
        """调用LLM"""
        try:
            result = subprocess.run(
                ["opencli", "llm", "ask", prompt],
                capture_output=True,
                text=True,
                timeout=60
            )
            if result.returncode != 0:
                raise Exception(f"LLM error: {result.stderr}")
            return result.stdout.strip()
        except subprocess.TimeoutExpired:
            raise Exception("LLM call timeout")
    
    def analyze_page(
        self, 
        page_content: str,
        cached_pattern: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """分析页面结构"""
        content_hash = self._hash_content(
            page_content + str(cached_pattern.get("domain", "") if cached_pattern else "")
        )
        
        # 检查缓存
        cached = self._get_cached(f"page_{content_hash}")
        if cached:
            return cached
        
        # 加载提示词
        prompt = self._load_prompt("page_analysis.md")
        prompt = prompt.replace("{PAGE_CONTENT}", page_content)
        
        # 添加已知模式
        if cached_pattern and cached_pattern.get("page_types"):
            prompt += f"\n\n已知网站模式:\n{json.dumps(cached_pattern['page_types'], indent=2)}"
        
        try:
            result = self._call_llm(prompt)
            analysis = json.loads(result)
            self._set_cache(f"page_{content_hash}", analysis)
            return analysis
        except Exception as e:
            return self._get_default_analysis()
    
    def analyze_elements(self, element_list: str) -> Dict[str, Any]:
        """分析元素交互性"""
        content_hash = self._hash_content(element_list)
        
        # 检查缓存
        cached = self._get_cached(f"element_{content_hash}")
        if cached:
            return cached
        
        # 加载提示词
        prompt = self._load_prompt("element_interactivity.md")
        prompt = prompt.replace("{ELEMENTS}", element_list)
        
        try:
            result = self._call_llm(prompt)
            analysis = json.loads(result)
            self._set_cache(f"element_{content_hash}", analysis)
            return analysis
        except:
            return {"interactive_elements": [], "element_groups": []}
    
    def analyze_network(self, entries: List[Dict]) -> Dict[str, Any]:
        """分析网络请求"""
        # 格式化请求列表
        entry_list = "\n".join([
            f"[{i}] {e.get('method', 'GET')} {e.get('url', 'unknown')} - {e.get('content_type', 'unknown')}"
            for i, e in enumerate(entries[:20])
        ])
        
        content_hash = self._hash_content(entry_list)
        
        # 检查缓存
        cached = self._get_cached(f"network_{content_hash}")
        if cached:
            return cached
        
        # 加载提示词
        prompt = self._load_prompt("network_analysis.md")
        prompt = prompt.replace("{NETWORK_ENTRIES}", entry_list)
        
        try:
            result = self._call_llm(prompt)
            analysis = json.loads(result)
            self._set_cache(f"network_{content_hash}", analysis)
            return analysis
        except:
            return {"api_endpoints": [], "data_sources": []}
    
    def _load_prompt(self, filename: str) -> str:
        """加载提示词文件"""
        prompt_path = Path(__file__).parent.parent / "prompts" / filename
        if prompt_path.exists():
            return prompt_path.read_text(encoding="utf-8")
        else:
            # 返回默认提示词
            return self._get_default_prompt(filename)
    
    def _get_default_prompt(self, filename: str) -> str:
        """获取默认提示词"""
        if filename == "page_analysis.md":
            return """分析以下页面内容，返回JSON格式的分析结果：

{PAGE_CONTENT}

返回格式：
{
  "page_type": "页面类型",
  "page_type_confidence": 0.95,
  "layout_pattern": "布局模式",
  "data_regions": [],
  "pagination": null,
  "forms": [],
  "navigation_hints": [],
  "suggested_actions": []
}

只返回JSON。"""
        
        elif filename == "element_interactivity.md":
            return """分析以下页面元素，判断可交互性：

{ELEMENTS}

返回格式：
{
  "interactive_elements": [
    {
      "ref": 元素编号,
      "interaction_type": "交互类型",
      "purpose": "交互目的",
      "importance": "重要性"
    }
  ],
  "element_groups": []
}

只返回JSON。"""
        
        elif filename == "network_analysis.md":
            return """分析以下网络请求：

{NETWORK_ENTRIES}

返回格式：
{
  "api_endpoints": [
    {
      "url": "请求URL",
      "purpose": "请求用途",
      "importance": "重要性"
    }
  ],
  "data_sources": []
}

只返回JSON。"""
        
        return ""
    
    def _get_default_analysis(self) -> Dict[str, Any]:
        """获取默认分析结果"""
        return {
            "page_type": "generic",
            "page_type_confidence": 0.5,
            "layout_pattern": "fluid",
            "data_regions": [],
            "pagination": None,
            "forms": [],
            "navigation_hints": [],
            "suggested_actions": [
                {
                    "action": "wait",
                    "target": "page",
                    "purpose": "手动分析页面结构",
                    "priority": "high"
                }
            ]
        }


if __name__ == "__main__":
    # 测试代码
    analyzer = LLMAnalyzer()
    
    # 测试页面分析
    test_content = """
    页面元素数量: 50
    可交互元素: 10
    
    元素列表:
    [1] button "搜索"
    [2] input "输入关键词"
    [3] a "首页"
    """
    
    result = analyzer.analyze_page(test_content)
    print(json.dumps(result, indent=2, ensure_ascii=False))
