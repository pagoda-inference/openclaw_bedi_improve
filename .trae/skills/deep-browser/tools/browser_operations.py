#!/usr/bin/env python3
"""
Deep Browser Operations
封装OpenCLI浏览器操作的高级接口
"""

import subprocess
import json
from typing import Optional, Dict, Any, List
from pathlib import Path


class DeepBrowser:
    """深度浏览器操作类"""
    
    def __init__(self, timeout: int = 60000):
        self.timeout = timeout
        self.current_url = None
    
    def _run_opencli(self, args: List[str]) -> str:
        """执行OpenCLI命令"""
        try:
            result = subprocess.run(
                ["opencli"] + args,
                capture_output=True,
                text=True,
                timeout=self.timeout / 1000
            )
            if result.returncode != 0:
                raise Exception(f"OpenCLI error: {result.stderr}")
            return result.stdout
        except subprocess.TimeoutExpired:
            raise Exception("OpenCLI command timeout")
    
    def open(self, url: str) -> Dict[str, Any]:
        """打开URL"""
        self._run_opencli(["browser", "open", url])
        self.current_url = url
        return {"status": "opened", "url": url}
    
    def click(self, target: int) -> Dict[str, Any]:
        """点击元素"""
        result = self._run_opencli(["browser", "click", str(target)])
        return {"status": "clicked", "target": target, "result": result}
    
    def type_text(self, target: int, text: str) -> Dict[str, Any]:
        """输入文本"""
        result = self._run_opencli(["browser", "type", str(target), text])
        return {"status": "typed", "target": target, "text": text}
    
    def scroll(self, direction: str = "down", amount: int = 300) -> Dict[str, Any]:
        """滚动页面"""
        result = self._run_opencli([
            "browser", "scroll", direction, "--amount", str(amount)
        ])
        return {"status": "scrolled", "direction": direction, "amount": amount}
    
    def get_state(self) -> Dict[str, Any]:
        """获取页面状态"""
        result = self._run_opencli(["browser", "state"])
        return self._parse_state(result)
    
    def get_url(self) -> str:
        """获取当前URL"""
        result = self._run_opencli(["browser", "get", "url"])
        self.current_url = result.strip()
        return self.current_url
    
    def get_title(self) -> str:
        """获取页面标题"""
        result = self._run_opencli(["browser", "get", "title"])
        return result.strip()
    
    def get_text(self, selector: str) -> str:
        """获取元素文本"""
        result = self._run_opencli(["browser", "get", "text", selector])
        return result
    
    def extract(self) -> Dict[str, Any]:
        """提取页面内容"""
        result = self._run_opencli(["browser", "extract"])
        try:
            return json.loads(result)
        except:
            return {"content": result}
    
    def screenshot(self, save_path: str) -> Dict[str, Any]:
        """截图"""
        self._run_opencli(["browser", "screenshot", save_path])
        return {"status": "captured", "path": save_path}
    
    def network(self, filter_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """获取网络请求"""
        args = ["browser", "network"]
        if filter_type:
            args.extend(["--filter", filter_type])
        
        result = self._run_opencli(args)
        try:
            data = json.loads(result)
            return data if isinstance(data, list) else data.get("entries", [])
        except:
            return []
    
    def _parse_state(self, output: str) -> Dict[str, Any]:
        """解析页面状态"""
        elements = []
        lines = output.strip().split("\n")
        
        for line in lines:
            if line.startswith("["):
                parts = line.split("]", 1)
                if len(parts) == 2:
                    ref = int(parts[0][1:])
                    rest = parts[1].strip()
                    elements.append({
                        "ref": ref,
                        "info": rest,
                        "visible": "[hidden]" not in line
                    })
        
        return {
            "elements": elements,
            "element_count": len(elements),
            "has_more_below": "scroll-down" in output
        }


if __name__ == "__main__":
    # 测试代码
    browser = DeepBrowser()
    
    # 打开页面
    print(browser.open("https://example.com"))
    
    # 获取状态
    state = browser.get_state()
    print(f"Elements: {state['element_count']}")
    
    # 获取URL和标题
    print(f"URL: {browser.get_url()}")
    print(f"Title: {browser.get_title()}")
