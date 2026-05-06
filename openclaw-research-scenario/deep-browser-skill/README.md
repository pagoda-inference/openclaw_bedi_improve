# Deep Browser Skill

网站探索器：给定需求，在网站中寻找数据所在位置、获取数据、形成记忆。

## 核心诉求

给定一个相对抽象模糊的需求（或精细的需求），在一个网站中：

1. **找到数据在哪里** — 数据在哪些页面？通过什么交互才能到达？
2. **获取数据** — 数据是 API 返回的还是页面渲染的？怎么提取？
3. **形成记忆** — 网站结构、数据分布、交互模式，供后续复用

## 在整体流程中的位置

```
用户粗糙需求
    ↓
web_search / deep research → 找到相关网站列表
    ↓
deep_browser → 探索网站结构，发现所有数据页面  ← 本 Skill
    ↓
opencli → 把探索结果沉淀为可复用 CLI 脚本
    ↓
CLI 提取数据 → 高效、确定性、可重复
    ↓
数据治理与分析 → 生成报告
```

Deep Browser 专注**探索阶段**，不直接调用 opencli。两者通过 Agent 协调。

## 📁 目录结构

```
deep-browser-skill/
├── SKILL.md                              # Skill 定义文件（智能体读取的入口）
├── README.md                             # 项目说明文档
├── reference/                            # 参考文档
│   ├── site_recon.md                     # 站点分类（Pattern A/B/C/D/E）
│   ├── site_memory.md                    # 站点记忆格式
│   ├── browser_operations_reference.md   # OpenCLI 命令参考
│   ├── cloud_setup.md                    # 云端 OpenCLI 配置
│   ├── page_analysis.md                  # 页面分析框架
│   ├── element_analysis.md               # 元素分析框架
│   ├── network_analysis.md               # 网络分析框架
│   └── page_state_template.md            # 页面状态模板
├── scripts/                              # Python 辅助脚本
│   ├── file_operations.py                # 文件操作工具
│   ├── memory_manager.py                 # 站点记忆管理
│   └── init_environment.py               # 环境初始化
└── cloud/                                # 云端部署配置
    ├── Dockerfile                        # Docker 镜像定义
    ├── docker-compose.yml                # Docker Compose 配置
    ├── start.sh                          # 启动脚本
    └── deploy.sh                         # 部署脚本
```

## 🎯 核心功能

### 1. 站点分类（Pattern A/B/C/D/E）

| Pattern | 站点类型 | 数据位置 | 探索策略 |
|---------|---------|---------|---------|
| A | SPA / JSON XHR | API 端点 | network 优先 |
| B | SSR / inline data | HTML 全局变量 + API | state 抽取 + network |
| C | JSONP / script src | JSONP 接口 | bundle 搜索 |
| D | Token / CSRF | 需鉴权 API | token 排查 |
| E | 流式 | WebSocket/SSE | 找 HTTP 轮询 |

一步诊断：`opencli browser analyze <url>`

### 2. 逐层探索

通过交互发现网站完整结构：

```
入口页面
├── 导航链接 → 子页面1
│   ├── API: GET /api/products
│   └── 更多链接 → 孙页面1-1
├── 折叠区域 → 展开后内容
└── 分页控件 → 第2页、第3页...
```

### 3. API 发现

```bash
opencli browser network              # 列出请求（带 shape 预览）
opencli browser network --filter "title,price"  # 按字段过滤
opencli browser network --detail r3  # 获取完整响应
```

### 4. 站点记忆

两层结构：公共种子 + 本地累积

```
~/.opencli/sites/<site>/
  endpoints.json     — 发现的 API 端点
  field-map.json     — 字段代号 → 含义
  notes.md           — 探索笔记
  structure.md       — 网站结构
```

### 5. 只读约束

- ✅ 允许：导航、展开、搜索、筛选、分页
- ❌ 禁止：表单提交、数据修改、购买操作

## 🚀 快速开始

### 方式一：本地开发（BrowserBridge 模式）

复用用户已登录的 Chrome 浏览器。

```bash
# 1. 安装 OpenCLI
npm install -g @jackwener/opencli

# 2. 安装 Browser Bridge 扩展
# 在 Chrome Web Store 搜索 "OpenCLI" 安装扩展

# 3. 验证环境
opencli doctor

# 4. 初始化
cd openclaw-research-scenario/deep-browser-skill
python scripts/init_environment.py
```

### 方式二：云端/容器（CDPBridge 模式）

无需 Chrome 扩展，直接连接 CDP WebSocket。

```bash
# 1. 启动 Chromium（headless + CDP）
chromium --headless --no-sandbox --remote-debugging-port=9222 &

# 2. 设置环境变量
export OPENCLI_CDP_ENDPOINT="http://localhost:9222"

# 3. 使用 OpenCLI
opencli browser open "https://example.com"
```

**Docker 部署**：

```bash
# 使用 Docker Compose
cd openclaw-research-scenario/deep-browser-skill/cloud
docker-compose up -d

# 测试
docker exec opencli-browser opencli browser open "https://example.com"
```

详见 [云端 OpenCLI 配置](reference/cloud_setup.md)。

## 📖 参考文档

| 文档 | 用途 |
|------|------|
| [站点侦察](reference/site_recon.md) | Pattern A/B/C/D/E 分类和对应策略 |
| [站点记忆](reference/site_memory.md) | 记忆格式和读写时机 |
| [浏览器操作参考](reference/browser_operations_reference.md) | OpenCLI 命令详细说明 |
| [云端 OpenCLI 配置](reference/cloud_setup.md) | Docker/Kubernetes 部署方案 |
| [页面分析](reference/page_analysis.md) | 页面结构分析方法 |
| [元素分析](reference/element_analysis.md) | 元素交互性和安全性判断 |
| [网络分析](reference/network_analysis.md) | API 发现和数据源识别 |
| [页面状态模板](reference/page_state_template.md) | 状态文件标准格式 |

## 🔧 依赖

### OpenCLI 连接模式

| 模式 | 环境变量 | 需要扩展 | 适用场景 |
|------|---------|---------|---------|
| BrowserBridge | 默认 | ✅ 需要 | 本地开发，复用用户浏览器 |
| CDPBridge | `OPENCLI_CDP_ENDPOINT` | ❌ 不需要 | 云端/容器，无头模式 |

### 降级方案

| 优先级 | 工具 | 能力 |
|--------|------|------|
| 1 | OpenCLI | 完整：交互 + 网络分析 + 登录态 + 反检测 |
| 2 | OpenClaw browser tool | 部分：交互可用，无登录态 |
| 3 | web-fetch + web-search | 受限：仅静态内容 |

## 🧪 测试

```bash
cd openclaw-research-scenario
python tests/test_deep_browser_skill.py
```

详见测试方案章节。

## 📝 设计决策

### 为什么用 OpenCLI 而不是 OpenClaw browser tool？

| 维度 | OpenCLI | OpenClaw browser tool |
|------|---------|----------------------|
| 登录态 | 复用用户 Chrome | 需单独管理 |
| 反检测 | 内置 stealth | 无 |
| 网络分析 | network + shape + filter | 无 |
| 站点分析 | analyze 一步分类 | 无 |
| 与 opencli 沉淀 | 同一浏览器，无缝衔接 | 不同浏览器 |

### 为什么 Deep Browser 不直接调用 opencli？

职责分离：
- Deep Browser 专注**探索**（发现结构、记录模式）
- opencli 专注**沉淀**（生成可复用 CLI）
- 两者通过 Agent 协调，不直接互调

### 为什么删除 browser_operations.py？

浏览器操作由 OpenCLI 命令提供，Agent 通过 Bash 直接调用，不需要 Python 包装。
