---
name: deep-browser
description: "深度网页浏览能力，具备智能页面理解和系统化导航功能。当需要深度探索网站、理解页面结构、导航复杂流程或积累浏览知识以供复用时调用。"
user-invocable: false
---

# Deep Browser Skill

高级浏览器自动化，结合LLM智能实现复杂网页交互。

## 何时使用

✅ **使用此技能当：**

- **数据需要页面交互**
  - 登录表单后的信息
  - 通过用户操作加载的数据（点击、滚动、输入）
  - 需要多步工作流的内容
  - 由交互触发的动态内容

- **需要深度页面交互**
  - 多步表单提交
  - 复杂导航流程
  - 动态内容加载（无限滚动、加载更多）
  - 需要认证的页面

- **全面数据采集**
  - 从多个页面提取结构化数据
  - 跨分页收集数据
  - 需要多次交互的数据采集
  - 从网站构建完整数据集

- **复杂页面分析**
  - 具有动态内容或反爬措施的页面
  - 需要在操作前理解页面结构
  - 识别数据区域和提取模式
  - 发现API端点和数据源

- **构建可复用模式**
  - 创建网站交互模板
  - 积累知识以供未来访问
  - 跨任务共享模式

## 何时不使用

❌ **不使用此技能当：**

- 简单单页检查 → 使用标准浏览器工具
- 静态内容提取 → 使用web-fetch
- 可用API访问数据 → 直接使用API
- 用户已登录只需导航 → 使用browser-automation skill
- 快速搜索或简单获取 → 直接使用web-search或web-fetch

## 前置要求

### 必需依赖

**主要模式：**
- **OpenCLI** - 浏览器自动化工具
  - 安装：`pip install opencli` 或遵循OpenCLI安装指南
  - 验证：`opencli --version`
- **LLM访问** - 用于智能页面分析
  - OpenAI API密钥或兼容的LLM端点
  - 验证：`opencli llm ask "test"`

**降级模式：**
- **web-fetch工具** - 用于静态内容获取
- **web-search工具** - 用于查找相关页面

### 环境设置

```bash
# 初始化环境
python scripts/init_environment.py

# 验证依赖
python scripts/init_environment.py --check-deps
```

## 核心能力

### 1. LLM驱动的分析

使用 `reference/` 目录中的结构化参考文档：

- **页面分析** (`reference/page_analysis.md`)
  - 页面类型识别
  - 布局模式检测
  - 数据区域映射
  - 分页发现

- **元素分析** (`reference/element_analysis.md`)
  - 交互性检测
  - 目的推断
  - 重要性排序
  - 元素分组

- **网络分析** (`reference/network_analysis.md`)
  - API端点发现
  - 数据源识别
  - 直接API潜力评估

### 2. 降级机制

当浏览器工具（OpenCLI, browser-automation）不可用时，自动降级到：

- **web-fetch** - 获取静态页面内容
- **web-search** - 查找相关页面和信息

**降级工作流：**
1. 检测浏览器工具可用性
2. 如果不可用 → 使用web-fetch获取页面内容
3. 使用web-search查找相关页面
4. 对获取的内容应用相同的分析参考
5. 将结果存储到模式文件

**降级限制：**
- 无法与动态内容交互
- 无法提交表单或点击按钮
- 无法处理认证
- 仅限于公开可访问的页面

### 3. 记忆系统

基于Markdown的模式存储在 `browser-patterns/` 目录：

```
browser-patterns/
├── sites/
│   ├── example.com.md    # 网站模式
│   └── INDEX.md          # 模式索引
└── plans/
    ├── task-001.md       # 浏览计划
    └── INDEX.md          # 计划索引
```

### 4. Python脚本

`scripts/` 目录中的辅助脚本：

- `browser_operations.py` - 浏览器导航和交互操作
- `file_operations.py` - 简单的文件操作工具
- `memory_manager.py` - 长期模式文件管理
- `init_environment.py` - 环境设置

## 使用方法

### 1. 初始化环境

```bash
python scripts/init_environment.py
```

创建：
- `browser-patterns/sites/` 目录
- `browser-patterns/plans/` 目录
- `states/` 目录（用于上下文隔离）
- 索引文件

### 2. 使用状态文件进行上下文隔离

**核心概念**：将页面状态写入文件而不是保存在内存中，以实现更好的隔离。

```python
from scripts.file_operations import FileOps

# 简单的文件操作
FileOps.write("states/state-001.md", page_state_content)
content = FileOps.read("states/state-001.md")

# 替换部分
FileOps.replace_section(
    "states/state-001.md",
    start_marker="## 页面元素",
    end_marker="## 分析结果",
    new_content=elements_table
)

# 按行号替换
FileOps.replace_lines(
    "states/state-001.md",
    start_line=10,
    end_line=15,
    new_lines=["新行 1", "新行 2"]
)
```

**优势**：
- 智能体不需要记住所有上下文
- 状态跨会话持久化
- 可以手动审查/编辑
- 支持多页面并行处理

### 3. 使用参考文档进行分析

智能体读取参考文件并创建结构化的状态文件：

**步骤1：读取分析参考**
```markdown
读取 reference/page_analysis.md
```

**步骤2：应用到页面内容**
- 使用参考框架分析页面结构
- 识别页面类型、布局、数据区域
- 生成结构化JSON分析

**步骤3：创建状态文件**
```markdown
使用 reference/page_state_template.md
创建 states/state-{id}.md 包含分析结果
```

**步骤4：更新状态文件**
```python
FileOps.replace_section(
    "states/state-001.md",
    "## 页面元素",
    "## 分析结果",
    elements_table
)
```

### 4. 保存到记忆

```python
from scripts.memory_manager import MemoryManager

manager = MemoryManager()

# 创建模式文件
pattern_content = """# example.com

> 域名: example.com
> 创建时间: 2026-04-28

## 页面类型

### listing

- 商品网格布局
- 分页控件

## 选择器

- search_box: #search
"""

manager.create_site_pattern("example.com", pattern_content)

# 读取模式
content = manager.read_site_pattern("example.com")

# 搜索模式
results = manager.search_patterns("product")

# 列出所有模式
patterns = manager.list_site_patterns()
```

### 5. 浏览器操作

**参考**：详见 `reference/browser_operations_reference.md` 获取详细操作指南。

**核心操作：**
- **导航**: open(), get_url(), get_title()
- **状态**: get_state(), extract()
- **交互**: click(), type_text(), scroll()
- **数据**: get_text(), screenshot()
- **网络**: network()

**代码示例：**
```python
from scripts.browser_operations import DeepBrowser

browser = DeepBrowser()

# 打开页面
browser.open("https://example.com")

# 获取状态
state = browser.get_state()

# 交互
browser.click(target=123)
browser.type_text(target=456, text="query")

# 提取
data = browser.extract()
```

### 6. 降级使用（当浏览器不可用时）

当浏览器工具不可用时，使用web-fetch和web-search：

```markdown
# 降级工作流
1. 尝试 browser.open() → 失败
2. 检测浏览器不可用
3. 使用web-fetch获取页面内容
4. 使用web-search查找相关页面
5. 对获取的内容应用分析参考
6. 将结果存储到模式文件
```

**示例：**
```markdown
# 代替浏览器交互
web-fetch url="https://example.com"
→ 返回静态HTML内容

# 搜索相关页面
web-search query="example.com products"
→ 返回相关URL列表

# 分析获取的内容
读取 reference/page_analysis.md
应用到获取的HTML
→ 返回结构化分析
```

**注意**：降级有限制 - 无法与动态内容、表单或需要认证的页面交互。

## 分析工作流

### 步骤1：创建状态文件

1. 生成唯一状态ID
2. 在 `states/` 目录创建状态文件
3. 用基本结构初始化

### 步骤2：捕获页面状态

1. 打开目标URL
2. 获取页面状态
3. 用以下内容更新状态文件：
   - 基本信息（URL、标题）
   - 页面元素（表格格式）
   - 网络请求

### 步骤3：应用分析参考

1. 读取 `reference/page_analysis.md`
2. 应用到页面内容
3. 用分析结果更新状态文件

### 步骤4：生成行动计划

1. 读取 `reference/element_analysis.md`
2. 识别可交互元素
3. 用建议操作更新状态文件

### 步骤5：执行和更新

1. 智能体读取状态文件
2. 执行建议操作
3. 用结果更新状态文件
4. 添加观察备注

### 步骤6：保存到长期记忆

1. 从状态中提取模式
2. 保存到模式文件
3. 更新统计

## 记忆格式

### 状态文件结构

```markdown
# 页面状态: state-001

> 状态ID: state-001
> 创建时间: 2026-04-28T10:00:00Z
> 更新时间: 2026-04-28T10:30:00Z

## 基本信息

- **URL**: https://example.com/products
- **标题**: 商品列表
- **状态**: analyzed

## 页面元素

| 引用 | 标签 | 文本 | 可见 | 角色 |
|------|------|------|------|------|
| 1 | button | 搜索 | ✓ | button |
| 2 | input | | ✓ | textbox |
| 3 | a | 下一页 | ✓ | link |

## 分析结果

**页面类型**: listing (置信度: 0.95)

**布局模式**: two-column

### 数据区域

- `.product-grid`: 主商品列表
- `.sidebar`: 筛选选项

### 分页机制

- 类型: click
- 选择器: `.next-page`
- 描述: 点击加载下一页

### 内容摘要

- 主题: 商品目录
- 语言: en
- 实体: products, categories

## 建议操作

1. 🔴 **click**
   - 目标: `.search-button`
   - 目的: 提交搜索查询
   - 优先级: high

2. 🟡 **type**
   - 目标: `#search-input`
   - 目的: 输入搜索词
   - 优先级: medium

## 网络请求

总计: 15 个请求

| 方法 | URL | 类型 |
|------|-----|------|
| GET | /api/products | application/json |
| POST | /api/search | application/json |

## 备注

- 初始页面加载成功 (10:00:05)
- 第一页发现50个商品 (10:00:10)
```

### 模式文件结构

```markdown
# example.com

> 域名: example.com
> 学习时间: 2026-04-28T10:00:00Z
> 最后使用: 2026-04-28T10:30:00Z
> 成功: 5 | 失败: 0

## 页面类型

<!-- 记录发现的页面类型 -->

### listing

**识别特征：**
- 商品网格布局
- 分页控件

**数据区域：**
| 选择器 | 类型 | 描述 |
|--------|------|------|
| .product-grid | product-list | 主列表 |

**分页：**
- 类型: click
- 选择器: .next-page

## 选择器

| 名称 | 选择器 |
|------|--------|
| search_box | #search |
| submit_btn | .search-btn |

## 备注

<!-- 添加观察 -->
```

### 计划文件结构

```markdown
# 浏览计划: 收集商品数据

> 任务ID: task-001
> 目标: 收集商品数据
> 深度: 0/3
> 状态: pending
> 创建时间: 2026-04-28T10:00:00Z

## 进度

- 总步骤: 5
- 已完成: 2
- 进行中: 1
- 待执行: 2

## 步骤

### 步骤1: 导航到列表 ✅

- 操作: open
- 参数: {"url": "https://example.com/products"}
- 预期: 商品列表页加载完成

### 步骤2: 提取商品 ✅

- 操作: extract
- 参数: {"selector": ".product-item"}
- 预期: 商品数据已收集

## 已收集数据

<!-- 添加收集的数据 -->
```

## 与智能体集成

智能体通过以下方式使用此技能：

1. **读取参考** 从 `reference/` 目录
2. **应用参考** 到当前上下文
3. **执行操作** 通过浏览器操作
4. **存储结果** 到模式文件
5. **学习模式** 以供未来使用

## 最佳实践

1. **始终先初始化** 环境
2. **分析前读取参考**
3. **成功交互后保存模式**
4. **更新统计** 以跟踪成功率
5. **发现时使用直接API**
6. **简单情况结合标准工具**

## 限制

### 主要模式（浏览器工具）
- 需要OpenCLI或browser-automation工具
- 需要LLM进行基于参考的分析
- 模式存储随网站多样性增长
- 初始分析比关键词匹配慢

### 降级模式（web-fetch + web-search）
- 无法与动态内容交互
- 无法提交表单或点击按钮
- 无法处理认证
- 仅限于公开可访问的页面
- 无实时页面状态监控
- 无法捕获网络请求

## 相关技能

### 主要工具
- `browser-automation` - 标准浏览器控制
- `web-fetch` - 简单内容提取
- `web-search` - 搜索和查找信息

### 降级工具
- `web-fetch` + `web-search` - 浏览器不可用时的替代方案

### 领域技能
- `market-research-collector` - 数据采集工作流
