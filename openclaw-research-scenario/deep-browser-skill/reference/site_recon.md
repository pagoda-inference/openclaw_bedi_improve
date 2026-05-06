# 站点侦察参考文档

本文档提供站点分类方法论，帮助快速判断网站类型并选择对应探索策略。

## 一步诊断（推荐）

```bash
opencli browser analyze <url>
```

返回结构化分析结果：

```json
{
  "pattern": { "pattern": "A", "reason": "3 JSON XHR responses observed" },
  "anti_bot": { "detected": false, "vendor": null, "evidence": [] },
  "initial_state": { "__INITIAL_STATE__": false, "__NUXT__": false, "__NEXT_DATA__": false },
  "nearest_adapter": { "site": "xueqiu", "example_commands": ["xueqiu search"] },
  "recommended_next_step": "Pick the most specific JSON endpoint from network"
}
```

## 手动三步诊断

当 `analyze` 结论模糊时：

```bash
opencli browser open <url>
opencli browser wait time 2
opencli browser network
```

根据 `network` 输出判断 Pattern。

## Pattern 分类

### Pattern A — SPA / JSON XHR

**特征**：大量 `/api/...` JSON 请求，包含目标数据

**代表**：xueqiu、linear、notion、大多数现代 SaaS

**信号**：
- URL 一访问就是 `/`，后续数据在 network tab
- `window.React / window.Vue` 存在
- `document.querySelector('main').childElementCount` 一开始为 0

**探索策略**：
1. `opencli browser network` → 找 JSON API
2. `opencli browser network --filter "目标字段"` → 精确过滤
3. `opencli browser network --detail <key>` → 拉完整 body
4. 验证 endpoint 是否可直接 fetch

### Pattern B — SSR / inline data

**特征**：首屏数据在 HTML 里，深层再走 API

**代表**：bilibili、小红书、微博、部分 Next.js/Nuxt 页

**信号**：
- `window.__INITIAL_STATE__` / `window.__NEXT_DATA__` / `window.__NUXT__` 存在
- 关 JS 仍能看到首屏数据

**探索策略**：
1. `opencli browser eval "Object.keys(window).filter(k=>k.startsWith('__'))"` → 检测全局变量
2. `opencli browser eval "JSON.stringify(window.__INITIAL_STATE__).slice(0,3000)"` → 抽取 SSR 数据
3. `opencli browser network` → 找深层 API（分页/评论等）

### Pattern C — JSONP / script src 驱动

**特征**：network 空或只有静态资源，数据通过 JSONP 加载

**代表**：eastmoney、tonghuashun、老一代金融站

**信号**：
- `network` 空或只有 css/font
- 页面有数据但看不到 API 请求
- `script[src]` 指向 `push/api/data` 域名

**探索策略**：
1. `opencli browser eval "[...document.querySelectorAll('script[src]')].map(s=>s.src)"` → 扫描 script src
2. 搜索 bundle 里的 baseURL
3. 尝试已知的经验 endpoint
4. URL 加 `.json` 试探

### Pattern D — Token / CSRF / Bearer

**特征**：有 API 但需要鉴权

**代表**：Twitter/X、部分企业 SaaS

**信号**：
- 已经是 Pattern A，但 fetch 返回 401/403
- 请求头有 `X-Csrf-Token / Authorization: Bearer` 等自定义字段

**探索策略**：
1. `opencli browser eval "document.cookie"` → 找 token cookie
2. `opencli browser eval "Object.keys(localStorage)"` → 找 localStorage token
3. 搜索 bundle 里的硬编码 Bearer
4. 降级到 intercept 方式

### Pattern E — 流式

**特征**：WebSocket / SSE 推送

**代表**：行情 tick、LLM chat

**信号**：
- `network` 里有 `101 Switching Protocols`
- `Content-Type: text/event-stream`

**探索策略**：
1. 先找同数据的 HTTP 轮询接口（90% 概率有）
2. 没有则放弃或用 intercept 收 N 条

## 反爬检测

| 信号 | 厂商 | 影响 | 策略 |
|------|------|------|------|
| `acw_sc__v2` / `acw_tc` | 阿里云 WAF | 返回滑块 HTML | 先浏览器上下文验证 |
| `__cf_bm` / `cf_clearance` | Cloudflare | TLS 指纹被标记 | 先浏览器上下文验证 |
| `_abck` / `bm_sz` | Akamai | 即使带 cookie 也常被挡 | 先浏览器上下文验证 |
| `geetest` / `gt_captcha` | Geetest | 滑块/拼图 | 超出能力范围 |

**规则**：检测到反爬时，不要用裸 Node fetch 验证 endpoint，先用浏览器上下文确认接口可用。

## 识别失败时

按优先级硬走：

```
1. 先当 A → network 精读
2. 不行当 B → state 抽取
3. 还不行当 C → bundle 搜索
4. 401 出现切 D → token 排查
5. 所有手段都试过 → intercept
```

不要纠结分类。分类是帮忙定第一步，没命中就按顺序降级。
