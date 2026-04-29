# Deep Browser Skill 使用指南

## 快速开始

### 1. 初始化环境

```bash
python .trae/skills/deep-browser/tools/init_environment.py
```

### 2. 基本使用

```python
from tools.browser_operations import DeepBrowser
from tools.llm_analyzer import LLMAnalyzer
from tools.memory_manager import MemoryManager

# 初始化
browser = DeepBrowser()
analyzer = LLMAnalyzer()
memory = MemoryManager()

# 打开页面
browser.open("https://example.com")

# 获取页面状态
state = browser.get_state()

# 分析页面
page_content = format_page_for_llm(state)
analysis = analyzer.analyze_page(page_content)

# 保存记忆
memory.save_site_pattern({
    "domain": "example.com",
    "page_types": {analysis['page_type']: {...}},
    ...
})
```

## 核心功能

### 1. 页面理解

使用LLM智能分析页面结构：

```python
# 分析页面
analysis = analyzer.analyze_page(page_content)

# 结果包含：
# - page_type: 页面类型
# - layout_pattern: 布局模式
# - data_regions: 数据区域
# - pagination: 分页机制
# - forms: 表单信息
# - suggested_actions: 建议操作
```

### 2. 元素交互性检测

智能识别可交互元素：

```python
# 分析元素
interactivity = analyzer.analyze_elements(element_list)

# 结果包含：
# - interactive_elements: 可交互元素列表
# - element_groups: 元素分组
```

### 3. 网络分析

识别API端点和数据源：

```python
# 获取网络请求
entries = browser.network()

# 分析网络请求
network_analysis = analyzer.analyze_network(entries)

# 结果包含：
# - api_endpoints: API端点列表
# - data_sources: 数据源模式
```

### 4. 记忆管理

保存和加载网站模式：

```python
# 保存模式
memory.save_site_pattern(pattern)

# 加载模式
pattern = memory.load_site_pattern("example.com")

# 列出所有模式
patterns = memory.list_patterns()
```

## 高级用法

### 多页面浏览

```python
# 创建浏览计划
plan = {
    "id": "task-001",
    "goal": "采集产品信息",
    "current_depth": 0,
    "max_depth": 3,
    "steps": [...]
}

# 保存计划
memory.save_browsing_plan(plan)

# 执行计划
for step in plan['steps']:
    if step['action'] == 'click':
        browser.click(step['params']['target'])
    elif step['action'] == 'collect':
        data = browser.get_text(step['params']['selector'])
```

### 缓存优化

LLM分析结果会自动缓存5分钟：

```python
# 第一次调用 - 会调用LLM
analysis1 = analyzer.analyze_page(content)

# 第二次调用相同内容 - 使用缓存
analysis2 = analyzer.analyze_page(content)  # 快速返回
```

## 示例场景

查看 `examples/` 目录：

- `market_research.py` - 市场调研场景
- `price_monitoring.py` - 价格监控场景（待创建）
- `content_extraction.py` - 内容提取场景（待创建）

## 配置

### 环境变量

```bash
# OpenCLI路径（如果不在PATH中）
export OPENCLI_PATH=/path/to/opencli

# LLM API配置
export LLM_API_KEY=your_api_key
export LLM_API_ENDPOINT=https://api.example.com
```

### 自定义配置

修改 `tools/` 目录中的Python脚本：

- `browser_operations.py` - 浏览器操作配置
- `llm_analyzer.py` - LLM分析配置
- `memory_manager.py` - 记忆管理配置

## 故障排除

### OpenCLI未找到

确保OpenCLI已安装并在PATH中：

```bash
which opencli
```

### LLM调用失败

检查LLM API配置：

```bash
opencli llm ask "test"
```

### 记忆目录权限

确保有权限访问 `~/.openclaw/deep-browser/`：

```bash
ls -la ~/.openclaw/deep-browser/
```

## 更多信息

查看 `SKILL.md` 获取完整文档。
