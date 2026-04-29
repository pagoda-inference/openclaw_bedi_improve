#!/usr/bin/env python3
"""
市场调研示例
演示如何使用Deep Browser进行市场调研
"""

import sys
from pathlib import Path

# 添加工具目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent / "tools"))

from browser_operations import DeepBrowser
from llm_analyzer import LLMAnalyzer
from memory_manager import MemoryManager


def market_research_example():
    """市场调研示例"""
    
    # 初始化组件
    browser = DeepBrowser()
    analyzer = LLMAnalyzer()
    memory = MemoryManager()
    
    # 目标网站
    target_url = "https://example-shop.com/products"
    domain = "example-shop.com"
    
    print(f"开始市场调研: {target_url}")
    print("=" * 60)
    
    # 1. 打开页面
    print("\n1. 打开页面...")
    browser.open(target_url)
    
    # 2. 获取页面状态
    print("\n2. 获取页面状态...")
    state = browser.get_state()
    print(f"   元素数量: {state['element_count']}")
    
    # 3. 检查是否有已保存的模式
    print("\n3. 检查记忆...")
    cached_pattern = memory.load_site_pattern(domain)
    if cached_pattern:
        print(f"   找到已保存的模式: {domain}")
        print(f"   页面类型: {list(cached_pattern.get('page_types', {}).keys())}")
    else:
        print("   未找到已保存的模式，将进行新分析")
    
    # 4. 分析页面
    print("\n4. 分析页面结构...")
    page_content = format_page_for_llm(state)
    analysis = analyzer.analyze_page(page_content, cached_pattern)
    
    print(f"   页面类型: {analysis['page_type']}")
    print(f"   置信度: {analysis['page_type_confidence']}")
    print(f"   布局模式: {analysis['layout_pattern']}")
    
    # 5. 分析元素交互性
    print("\n5. 分析元素交互性...")
    element_list = format_elements_for_llm(state)
    interactivity = analyzer.analyze_elements(element_list)
    
    print(f"   可交互元素: {len(interactivity['interactive_elements'])}")
    for elem in interactivity['interactive_elements'][:5]:
        print(f"   - [{elem['ref']}] {elem['interaction_type']}: {elem['purpose']}")
    
    # 6. 网络分析
    print("\n6. 分析网络请求...")
    network_entries = browser.network()
    if network_entries:
        network_analysis = analyzer.analyze_network(network_entries)
        
        print(f"   API端点: {len(network_analysis['api_endpoints'])}")
        for endpoint in network_analysis['api_endpoints'][:3]:
            print(f"   - {endpoint['purpose']}: {endpoint['url']}")
    
    # 7. 数据采集
    print("\n7. 采集数据...")
    if analysis.get('data_regions'):
        for region in analysis['data_regions']:
            print(f"   采集区域: {region['description']}")
            # 实际采集代码
            # data = browser.get_text(region['selector'])
            # print(f"   数据: {data[:100]}...")
    
    # 8. 保存记忆
    print("\n8. 保存记忆...")
    pattern = {
        "domain": domain,
        "page_types": {
            analysis['page_type']: {
                "type": analysis['page_type'],
                "indicators": [hint['path'] for hint in analysis.get('navigation_hints', [])],
                "data_regions": analysis.get('data_regions', []),
                "pagination": analysis.get('pagination')
            }
        },
        "selectors": {},
        "learned_at": get_current_time(),
        "last_used": get_current_time(),
        "success_count": 1,
        "failure_count": 0
    }
    
    memory.save_site_pattern(pattern)
    print(f"   模式已保存: {domain}")
    
    print("\n" + "=" * 60)
    print("市场调研完成！")


def format_page_for_llm(state):
    """格式化页面状态为LLM输入"""
    lines = [
        f"页面元素数量: {state['element_count']}",
        f"可交互元素: {len([e for e in state['elements'] if e.get('visible')])}",
        "",
        "元素列表:",
        ""
    ]
    
    for elem in state['elements'][:50]:
        visibility = "" if elem.get('visible') else "[隐藏]"
        lines.append(f"[{elem['ref']}] {elem['info']}{visibility}")
    
    if len(state['elements']) > 50:
        lines.append(f"\n... 还有 {len(state['elements']) - 50} 个元素")
    
    return "\n".join(lines)


def format_elements_for_llm(state):
    """格式化元素列表为LLM输入"""
    lines = []
    
    for elem in state['elements'][:30]:
        lines.append(f"[{elem['ref']}] {elem['info']}")
    
    return "\n".join(lines)


def get_current_time():
    """获取当前时间"""
    from datetime import datetime
    return datetime.now().isoformat()


if __name__ == "__main__":
    market_research_example()
