---
name: "deep-browser"
description: "Deep browser automation with LLM-powered page analysis, intelligent navigation, and memory accumulation. Invoke when user needs to browse websites, collect data, analyze page structures, or perform automated web interactions."
---

# Deep Browser Skill

深度浏览器技能：使用LLM理解网站系统、规划浏览路径、执行多步交互、积累记忆。

## 核心能力

### 1. 页面理解 (understand)
- 使用LLM分析页面结构、布局、数据区域
- 识别页面类型（listing/product/search/login等）
- 检测分页机制和导航路径
- 结合已有记忆进行智能分析

### 2. 智能操作 (operate)
- 点击、输入、滚动、选择等操作
- 基于LLM分析选择最优操作策略
- 自动等待页面加载和动态内容

### 3. 观察变化 (observe)
- 监控页面状态变化
- 截图保存
- 提取关键信息

### 4. 记忆管理 (remember)
- 保存网站模式到Markdown文件
- 积累浏览经验
- 支持模式复用

### 5. 数据采集 (collect)
- 提取页面内容
- 支持CSS选择器定位
- 自动保存采集结果

### 6. 浏览规划 (plan)
- 基于LLM分析生成多步浏览计划
- 自动识别数据采集路径
- 支持深度控制和任务恢复

### 7. 网络分析 (network)
- 使用LLM识别API端点用途
- 区分数据获取、认证、追踪等请求
- 发现隐藏的数据源

### 8. 页面分析 (analyze)
- 独立的页面结构分析
- 支持自定义分析提示词
- 返回结构化分析结果

## 工具集成

本Skill提供Python工具脚本，位于 `tools/` 目录：

### browser_operations.py
浏览器操作工具，封装OpenCLI命令：
- 页面导航
- 元素交互
- 内容提取
- 网络监控

### llm_analyzer.py
LLM分析工具：
- 页面结构分析
- 元素交互性检测
- 网络请求分析
- 结果缓存

### memory_manager.py
记忆管理工具：
- Markdown格式存储
- 索引机制
- 模式匹配

## 使用方法

### 基本调用

```python
from tools.browser_operations import DeepBrowser

browser = DeepBrowser()

# 理解页面
result = browser.understand(url="https://example.com")

# 执行操作
browser.click(target=123)
browser.type(target=456, text="search query")

# 采集数据
data = browser.collect(selector=".product-list")

# 保存记忆
browser.remember(site_pattern_id="example.com")
```

### 高级用法

```python
# 带任务上下文的浏览规划
plan = browser.plan(
    task_context={
        "task_id": "market-research-001",
        "sub_topic": "竞品价格分析",
        "depth": 0,
        "max_depth": 3
    }
)

# 网络分析
network = browser.network()
print(network["api_endpoints"])

# 自定义分析
analysis = browser.analyze(
    page_content="...",
    analysis_prompt="分析这个页面的产品信息结构"
)
```

## LLM提示词

提示词文件位于 `prompts/` 目录：

- `page_analysis.md` - 页面结构分析提示词
- `element_interactivity.md` - 元素交互性检测提示词
- `network_analysis.md` - 网络请求分析提示词

## 记忆格式

记忆以Markdown格式存储在 `~/.openclaw/deep-browser/` 目录：

```
patterns/
  example.com.md      # 网站模式
  INDEX.md            # 模式索引
plans/
  task-001.md         # 浏览计划
  INDEX.md            # 计划索引
```

### 网站模式示例

```markdown
# example.com

> 域名: example.com
> 学习时间: 2026-04-28T10:00:00Z
> 最后使用: 2026-04-28T10:30:00Z
> 成功次数: 5
> 失败次数: 0

## 页面类型

### listing

**识别特征**：
- 商品列表布局
- 分页控件存在

**数据区域**：

| 选择器 | 类型 | 说明 |
|--------|------|------|
| .product-list | product-list | 商品列表区域 |
| .pagination | pagination | 分页控件 |

**分页机制**：
- 类型: click
- 选择器: .next-page
```

## 初始化

首次使用时，运行初始化脚本：

```bash
python tools/init_environment.py
```

这将创建必要的目录结构和配置文件。

## 依赖

- Python 3.8+
- OpenCLI (用于浏览器操作)
- LLM API访问 (用于智能分析)

## 示例场景

查看 `examples/` 目录获取完整示例：

- `market_research.py` - 市场调研场景
- `price_monitoring.py` - 价格监控场景
- `content_extraction.py` - 内容提取场景

## 注意事项

1. **LLM调用缓存**：相似内容会使用缓存，减少API调用
2. **记忆积累**：多次访问同一网站会积累经验，提高效率
3. **错误恢复**：支持任务中断后的恢复
4. **隐私保护**：敏感信息不会保存到记忆中
