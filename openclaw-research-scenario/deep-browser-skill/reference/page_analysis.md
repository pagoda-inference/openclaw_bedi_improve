# 页面分析参考文档

本文档提供页面结构分析的方法论，帮助理解网页结构、发现导航入口、定位数据。

## 分析目标

1. **页面用途** — 这个页面是做什么的
2. **导航入口** — 从这里可以到达哪些其他页面
3. **数据位置** — 数据在页面上还是 API 里
4. **交互方式** — 哪些交互可以发现隐藏内容
5. **安全性** — 哪些交互是只读的

## 快速分析

```bash
# 一步完成站点分类
opencli browser analyze <url>

# 获取页面快照
opencli browser state

# 查看网络请求
opencli browser network
```

## Pattern 分类（决定探索策略）

| Pattern | 站点类型 | 数据位置 | 探索策略 |
|---------|---------|---------|---------|
| A | SPA / JSON XHR | API 端点 | network 优先 |
| B | SSR / inline data | HTML 全局变量 + API | state 抽取 + network |
| C | JSONP / script src | JSONP 接口 | bundle 搜索 |
| D | Token / CSRF | 需鉴权 API | token 排查 |
| E | 流式 | WebSocket/SSE | 找 HTTP 轮询 |

详见 [站点侦察参考](site_recon.md)。

## 页面类型识别

| 类型 | 特征 | 导航价值 | 示例 |
|------|------|---------|------|
| listing | 列表展示，有分页 | ⭐⭐⭐ | 商品列表、文章列表 |
| product | 单个实体详情 | ⭐⭐ | 商品详情、文章详情 |
| search | 搜索结果展示 | ⭐⭐⭐ | 搜索结果页 |
| dashboard | 数据概览 | ⭐⭐ | 用户中心、控制面板 |
| content | 信息展示 | ⭐ | 关于我们、帮助文档 |
| login | 用户认证 | ⭐（写入类） | 登录、注册页面 |
| form | 数据收集 | ⭐（写入类） | 联系表单、调查问卷 |
| checkout | 交易流程 | ❌（写入类） | 购物车、结算页 |

## 导航入口发现

每个页面的首要任务是发现所有导航入口。

| 入口类型 | 发现方式 | 导航价值 | 安全性 |
|---------|---------|---------|--------|
| 导航链接 | state 直接可见 | ⭐⭐⭐ | ✅ 只读 |
| 面包屑 | state 直接可见 | ⭐⭐⭐ | ✅ 只读 |
| 列表项链接 | state 直接可见 | ⭐⭐⭐ | ✅ 只读 |
| 分页链接 | state 直接可见 | ⭐⭐⭐ | ✅ 只读 |
| 折叠菜单中的链接 | 需展开 | ⭐⭐ | ✅ 只读 |
| 标签切换中的链接 | 需切换 | ⭐⭐ | ✅ 只读 |
| 搜索结果中的链接 | 需搜索 | ⭐⭐⭐ | ✅ 只读 |
| 滚动加载的条目 | 需滚动 | ⭐⭐ | ✅ 只读 |

**发现方法**：
1. `opencli browser state` → 扫描所有链接
2. 执行交互（展开、滚动）后重新 state
3. `opencli browser network` → 发现 API 端点
4. 记录每个入口的目标 URL

## 数据位置判断

### 数据在 API 里（Pattern A/D/E）

```bash
opencli browser network --filter "目标字段"
opencli browser network --detail <key>
```

优势：结构化、稳定、可程序化获取。

### 数据在页面里（Pattern B/C）

```bash
opencli browser extract --chunk-size 8000
opencli browser eval "JSON.stringify(window.__INITIAL_STATE__)"
```

需要 DOM 解析，不如 API 可靠。

### 数据需要交互才能出现

```bash
opencli browser click 3 && opencli browser state
opencli browser scroll down && opencli browser state
```

记录交互序列，供后续复用。

## 分页机制识别

| 类型 | 识别方法 | 安全性 |
|------|---------|--------|
| 点击分页 | state 中有页码按钮 | ✅ 只读 |
| 滚动加载 | state 提示 "has_more_below" | ✅ 只读 |
| 加载更多 | state 中有 "加载更多" 按钮 | ✅ 只读 |
| API 分页 | network 中有 page/offset 参数 | ✅ 只读 |

## 表单安全性分类

| 表单类型 | 提交目的 | 安全性 | 处理 |
|---------|---------|--------|------|
| 搜索表单 | 获取搜索结果 | ✅ 只读 | 允许输入和提交 |
| 筛选表单 | 改变展示方式 | ✅ 只读 | 允许选择和提交 |
| 登录表单 | 创建会话 | ❌ 写入 | 仅记录入口 |
| 注册表单 | 创建账号 | ❌ 写入 | 仅记录入口 |
| 联系表单 | 发送消息 | ❌ 写入 | 仅记录入口 |
| 订单表单 | 产生交易 | ❌ 写入 | 仅记录入口 |

**判断标准**：目的是获取/展示信息 → 只读；目的是创建/修改数据 → 写入。

## 分析输出

分析结果保存到状态文件和站点记忆：

- **状态文件** `states/state-{id}.md`：当前页面的分析快照
- **站点记忆** `~/.opencli/sites/<site>/`：跨会话持久化

详见 [页面状态模板](page_state_template.md) 和 [站点记忆](site_memory.md)。

## 相关参考

- [站点侦察](site_recon.md) — Pattern 分类详解
- [元素分析](element_analysis.md) — 元素交互性和安全性
- [网络分析](network_analysis.md) — API 发现
- [站点记忆](site_memory.md) — 记忆格式
