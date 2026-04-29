# Deep Browser Skill

深度浏览器技能：用于复杂网页交互、深度页面分析和全面数据采集。

## 📁 目录结构

```
deep-browser-skill/
├── SKILL.md                              # Skill定义文件
├── reference/                            # 参考文档
│   ├── page_analysis.md                  # 页面分析框架
│   ├── element_analysis.md               # 元素分析框架
│   ├── network_analysis.md               # 网络分析框架
│   ├── page_state_template.md            # 页面状态模板
│   └── browser_operations_reference.md   # 浏览器操作参考
└── scripts/                              # Python工具脚本
    ├── browser_operations.py             # 浏览器操作封装
    ├── file_operations.py                # 文件操作工具
    ├── memory_manager.py                 # 记忆管理工具
    └── init_environment.py               # 环境初始化
```

## 🎯 核心功能

### 1. 深度页面交互
- 多步表单提交
- 复杂导航流程
- 动态内容加载
- 认证页面处理

### 2. 智能页面理解
- 页面类型识别
- 布局模式检测
- 数据区域映射
- 分页机制发现

### 3. 全面数据采集
- 跨页数据提取
- 分页数据收集
- 多步交互数据
- 完整数据集构建

### 4. 可复用模式
- 网站交互模板
- 浏览知识积累
- 模式共享复用

## 🚀 快速开始

### 1. 初始化环境

```bash
cd openclaw-research-scenario/deep-browser-skill
python scripts/init_environment.py
```

### 2. 基本使用

```python
from scripts.browser_operations import DeepBrowser
from scripts.file_operations import FileOps
from scripts.memory_manager import MemoryManager

# 浏览器操作
browser = DeepBrowser()
browser.open("https://example.com")
state = browser.get_state()

# 文件操作
FileOps.write("states/state-001.md", page_content)
content = FileOps.read("states/state-001.md")

# 记忆管理
manager = MemoryManager()
manager.create_site_pattern("example.com", pattern_content)
```

## 📖 参考文档

- [页面分析框架](reference/page_analysis.md) - 如何分析页面结构
- [元素分析框架](reference/element_analysis.md) - 如何识别可交互元素
- [网络分析框架](reference/network_analysis.md) - 如何发现API端点
- [页面状态模板](reference/page_state_template.md) - 标准化状态文件格式
- [浏览器操作参考](reference/browser_operations_reference.md) - 详细的操作说明

## 🔧 依赖

### Primary Mode
- **OpenCLI** - 浏览器自动化工具
- **LLM Access** - 智能页面分析

### Fallback Mode
- **web-fetch** - 静态内容获取
- **web-search** - 页面搜索

## 📝 使用场景

详见 [SKILL.md](SKILL.md) 中的 "When to Use" 章节。

## 🔄 后续工作

这个skill目前作为设计原型存放在openclaw-research-scenario目录下。后续需要：

1. **集成到OpenClaw Plugin系统**
   - 遵循plugin规范
   - 与其他工具集成
   - 完善测试

2. **优化和完善**
   - 增强错误处理
   - 添加更多参考框架
   - 优化性能

3. **文档完善**
   - 添加更多使用示例
   - 创建教程文档
   - 编写API文档

## 📄 相关文档

- [场景描述](../场景描述.md)
- [智能体能力需求](../智能体能力需求.md)
- [Deep Browser 能力设计](../Deep Browser 能力设计.md)
- [思考与讨论总结](../思考与讨论总结.md)
