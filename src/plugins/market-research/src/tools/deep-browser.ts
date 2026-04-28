import type { AgentToolResult } from "@mariozechner/pi-agent-core";
import type { TSchema } from "typebox";
import fs from "node:fs/promises";
import path from "node:path";
import os from "os";
import { spawn } from "node:child_process";

const MEMORY_BASE_DIR = path.join(os.homedir(), ".openclaw", "deep-browser");

export type DeepBrowserAction =
  | "understand"
  | "operate"
  | "observe"
  | "remember"
  | "collect"
  | "plan"
  | "network";

export type DeepBrowserParams = {
  action: DeepBrowserAction;
  url?: string;
  target?: string | number;
  text?: string;
  option?: string;
  direction?: "up" | "down";
  amount?: number;
  timeout?: number;
  save_to?: string;
  selector?: string;
  css?: string;
  limit?: number;
  nth?: number;
  key?: string;
  js?: string;
  filter?: string;
  site_pattern_id?: string;
  task_context?: {
    task_id: string;
    sub_topic: string;
    depth: number;
    max_depth: number;
  };
};

type ElementInfo = {
  ref: number;
  tag: string;
  role?: string;
  text?: string;
  attrs?: Record<string, string>;
  visible: boolean;
};

type PageSnapshot = {
  url: string;
  title: string;
  elements: ElementInfo[];
  interactive_count: number;
  compounds: number[];
  scroll_position: { x: number; y: number };
  has_more_below: boolean;
};

type SitePattern = {
  id: string;
  domain: string;
  page_types: Record<string, PageTypePattern>;
  navigation_flows: NavigationFlow[];
  data_endpoints: DataEndpoint[];
  selectors: Record<string, string>;
  learned_at: string;
  last_used: string;
  success_count: number;
  failure_count: number;
};

type PageTypePattern = {
  type: string;
  indicators: string[];
  data_regions: Array<{ selector: string; type: string }>;
  pagination?: { type: string; selector: string };
};

type NavigationFlow = {
  name: string;
  steps: Array<{
    action: string;
    target: string;
    wait_for?: string;
    expected_change: string;
  }>;
  purpose: string;
};

type DataEndpoint = {
  url_pattern: string;
  method: string;
  shape: string;
  purpose: string;
};

type BrowsingPlan = {
  id: string;
  goal: string;
  current_depth: number;
  max_depth: number;
  steps: PlanStep[];
  completed_steps: string[];
  current_step: string | null;
  collected_data: Array<{ step: string; data: unknown }>;
  created_at: string;
  status: string;
};

type PlanStep = {
  id: string;
  description: string;
  action: string;
  params: Record<string, unknown>;
  dependencies: string[];
  status: "pending" | "in_progress" | "completed" | "failed";
  retry_count: number;
  max_retries: number;
  expected_outcome: string;
  executed_at?: string;
  result?: string;
};

export class DeepBrowserTool {
  name = "deep_browser";
  description = "深度浏览器：理解网站系统、规划浏览路径、执行多步交互、积累记忆（MD格式）";

  definition = {
    name: this.name,
    description: this.description,
    input_schema: {
      type: "object",
      properties: {
        action: {
          type: "string",
          enum: ["understand", "operate", "observe", "remember", "collect", "plan", "network"],
          description: "操作类型",
        },
        url: { type: "string", description: "URL" },
        target: { description: "目标元素（ref 数字或 CSS 选择器）" },
        text: { type: "string", description: "输入文本" },
        option: { type: "string", description: "选择选项" },
        direction: { type: "string", enum: ["up", "down"], description: "滚动方向" },
        amount: { type: "number", description: "滚动量（像素）" },
        timeout: { type: "number", description: "超时时间（毫秒）" },
        save_to: { type: "string", description: "保存路径" },
        selector: { type: "string", description: "CSS 选择器" },
        site_pattern_id: { type: "string", description: "网站模式 ID（域名）" },
        task_context: {
          type: "object",
          description: "任务上下文",
          properties: {
            task_id: { type: "string" },
            sub_topic: { type: "string" },
            depth: { type: "number" },
            max_depth: { type: "number" },
          },
        },
      },
      required: ["action"],
    } as unknown as TSchema,
  };

  async execute(
    _toolCallId: string,
    params: DeepBrowserParams,
    _signal?: AbortSignal,
  ): Promise<AgentToolResult<unknown>> {
    try {
      await this.ensureMemoryDirs();

      switch (params.action) {
        case "understand":
          return await this.understandPage(params);
        case "operate":
          return await this.executeOperation(params);
        case "observe":
          return await this.observeChanges(params);
        case "remember":
          return await this.saveMemory(params);
        case "collect":
          return await this.collectContent(params);
        case "plan":
          return await this.planBrowsing(params);
        case "network":
          return await this.captureNetwork(params);
        default:
          return { ok: false, error: "Unknown action" };
      }
    } catch (error) {
      return {
        ok: false,
        error: error instanceof Error ? error.message : "Unknown error",
      };
    }
  }

  private async ensureMemoryDirs(): Promise<void> {
    await fs.mkdir(MEMORY_BASE_DIR, { recursive: true });
    await fs.mkdir(path.join(MEMORY_BASE_DIR, "patterns"), { recursive: true });
    await fs.mkdir(path.join(MEMORY_BASE_DIR, "plans"), { recursive: true });
  }

  private async understandPage(params: DeepBrowserParams): Promise<AgentToolResult<unknown>> {
    if (params.url) {
      await this.runOpenCLI(["browser", "open", params.url]);
    }

    const stateResult = await this.runOpenCLI(["browser", "state"]);
    const state = this.parseStateOutput(stateResult);

    const urlResult = await this.runOpenCLI(["browser", "get", "url"]);
    const currentUrl = urlResult.trim();
    const domain = params.url ? new URL(params.url).hostname : 
                   currentUrl ? new URL(currentUrl).hostname : null;

    let existingPattern: SitePattern | null = null;
    if (domain) {
      existingPattern = await this.readSitePatternMD(domain);
    }

    const analysis = {
      page_type: this.detectPageType(state),
      layout_pattern: this.detectLayoutPattern(state),
      interactive_elements: state.elements.filter((e) => e.visible && this.isInteractive(e)),
      data_regions: this.detectDataRegions(state),
      pagination: this.detectPagination(state),
      form_purposes: this.detectFormPurposes(state),
    };

    if (existingPattern) {
      const pageType = analysis.page_type;
      const cachedPageType = existingPattern.page_types[pageType];
      
      return {
        ok: true,
        result: {
          source: "memory",
          cached_pattern: existingPattern,
          cached_page_type: cachedPageType,
          current_state: state,
          analysis,
          recommendation: cachedPageType 
            ? `使用缓存的选择器: ${JSON.stringify(cachedPageType.data_regions)}`
            : "发现新页面类型，建议探索后保存",
        },
      };
    }

    const networkResult = await this.runOpenCLI(["browser", "network"]);
    const network = this.parseNetworkOutput(networkResult);

    return {
      ok: true,
      result: {
        source: "analysis",
        state,
        analysis,
        network_summary: network.slice(0, 10),
        suggested_next_steps: this.suggestNextSteps(analysis),
        suggestion: "建议使用 remember 保存网站模式",
      },
    };
  }

  private async executeOperation(params: DeepBrowserParams): Promise<AgentToolResult<unknown>> {
    const target = params.target !== undefined ? String(params.target) : params.selector;
    if (!target) {
      return { ok: false, error: "target or selector is required" };
    }

    let result: string;

    if (params.text !== undefined) {
      result = await this.runOpenCLI(["browser", "type", target, params.text]);
    } else if (params.option !== undefined) {
      result = await this.runOpenCLI(["browser", "select", target, params.option]);
    } else if (params.direction) {
      const args = ["browser", "scroll", params.direction];
      if (params.amount) args.push("--amount", String(params.amount));
      result = await this.runOpenCLI(args);
    } else if (params.key) {
      result = await this.runOpenCLI(["browser", "keys", params.key]);
    } else {
      result = await this.runOpenCLI(["browser", "click", target]);
    }

    const parsed = this.parseActionResult(result);

    return {
      ok: true,
      result: {
        action_performed: true,
        target,
        result: parsed,
        timestamp: new Date().toISOString(),
      },
    };
  }

  private async observeChanges(params: DeepBrowserParams): Promise<AgentToolResult<unknown>> {
    const stateResult = await this.runOpenCLI(["browser", "state"]);
    const state = this.parseStateOutput(stateResult);

    const urlResult = await this.runOpenCLI(["browser", "get", "url"]);
    const titleResult = await this.runOpenCLI(["browser", "get", "title"]);

    let screenshot: string | null = null;
    if (params.save_to) {
      await this.runOpenCLI(["browser", "screenshot", params.save_to]);
      screenshot = params.save_to;
    }

    return {
      ok: true,
      result: {
        url: urlResult.trim(),
        title: titleResult.trim(),
        element_count: state.elements.length,
        interactive_count: state.interactive_count,
        scroll_position: state.scroll_position,
        has_more_below: state.has_more_below,
        screenshot,
        observed_at: new Date().toISOString(),
      },
    };
  }

  private async saveMemory(params: DeepBrowserParams): Promise<AgentToolResult<unknown>> {
    const urlResult = await this.runOpenCLI(["browser", "get", "url"]);
    const currentUrl = urlResult.trim();
    
    const domain = params.site_pattern_id || 
                   (currentUrl ? new URL(currentUrl).hostname : null);
    
    if (!domain) {
      return { ok: false, error: "无法确定域名，请提供 site_pattern_id" };
    }

    const stateResult = await this.runOpenCLI(["browser", "state"]);
    const state = this.parseStateOutput(stateResult);

    const pageType = this.detectPageType(state);
    const pagination = this.detectPagination(state);
    const dataRegions = this.detectDataRegions(state);

    let pattern = await this.readSitePatternMD(domain);

    if (!pattern) {
      pattern = {
        id: domain,
        domain,
        page_types: {},
        navigation_flows: [],
        data_endpoints: [],
        selectors: {},
        learned_at: new Date().toISOString(),
        last_used: new Date().toISOString(),
        success_count: 0,
        failure_count: 0,
      };
    }

    if (!pattern.page_types[pageType]) {
      pattern.page_types[pageType] = {
        type: pageType,
        indicators: this.extractIndicators(state),
        data_regions: dataRegions,
        pagination: pagination || undefined,
      };
    }

    if (params.selector) {
      const [name, value] = params.selector.split("=");
      if (name && value) {
        pattern.selectors[name.trim()] = value.trim();
      }
    }

    pattern.last_used = new Date().toISOString();
    pattern.success_count++;

    await this.writeSitePatternMD(pattern);

    return {
      ok: true,
      result: {
        saved: true,
        domain,
        page_type: pageType,
        file_path: path.join(MEMORY_BASE_DIR, "patterns", `${domain}.md`),
        pattern_summary: {
          page_types: Object.keys(pattern.page_types),
          selectors_count: Object.keys(pattern.selectors).length,
          success_count: pattern.success_count,
        },
      },
    };
  }

  private async collectContent(params: DeepBrowserParams): Promise<AgentToolResult<unknown>> {
    if (params.url) {
      await this.runOpenCLI(["browser", "open", params.url]);
    }

    let content: string;
    if (params.selector) {
      const textResult = await this.runOpenCLI(["browser", "get", "text", params.selector]);
      content = textResult;
    } else {
      const extractResult = await this.runOpenCLI(["browser", "extract"]);
      const parsed = JSON.parse(extractResult);
      content = parsed.content || "";
    }

    const urlResult = await this.runOpenCLI(["browser", "get", "url"]);
    const titleResult = await this.runOpenCLI(["browser", "get", "title"]);

    const extracted = {
      content,
      url: urlResult.trim(),
      title: titleResult.trim(),
      collected_at: new Date().toISOString(),
    };

    if (params.save_to) {
      await fs.writeFile(params.save_to, JSON.stringify(extracted, null, 2));
    }

    return {
      ok: true,
      result: {
        extracted,
        saved_to: params.save_to || null,
        content_length: content.length,
      },
    };
  }

  private async planBrowsing(params: DeepBrowserParams): Promise<AgentToolResult<unknown>> {
    if (!params.task_context) {
      return { ok: false, error: "task_context is required for plan action" };
    }

    const { task_id, sub_topic, depth, max_depth } = params.task_context;

    let plan = await this.readPlanMD(task_id);

    if (!plan) {
      plan = {
        id: task_id,
        goal: sub_topic,
        current_depth: depth,
        max_depth,
        steps: [],
        completed_steps: [],
        current_step: null,
        collected_data: [],
        created_at: new Date().toISOString(),
        status: "pending",
      };
    }

    const stateResult = await this.runOpenCLI(["browser", "state"]);
    const state = this.parseStateOutput(stateResult);

    const analysis = {
      page_type: this.detectPageType(state),
      interactive_elements: state.elements.filter((e) => e.visible && this.isInteractive(e)),
      pagination: this.detectPagination(state),
      data_regions: this.detectDataRegions(state),
    };

    const newSteps = this.generateBrowsingSteps(analysis, plan, depth, max_depth);

    for (const step of newSteps) {
      if (!plan.steps.find((s) => s.id === step.id)) {
        plan.steps.push(step);
      }
    }

    await this.writePlanMD(plan);

    return {
      ok: true,
      result: {
        plan,
        current_analysis: analysis,
        suggested_next_step: plan.steps.find((s) => s.status === "pending"),
        progress: {
          total_steps: plan.steps.length,
          completed: plan.steps.filter((s) => s.status === "completed").length,
          remaining: plan.steps.filter((s) => s.status === "pending").length,
        },
      },
    };
  }

  private async captureNetwork(params: DeepBrowserParams): Promise<AgentToolResult<unknown>> {
    if (params.key) {
      const detailResult = await this.runOpenCLI(["browser", "network", "--detail", params.key]);
      const detail = JSON.parse(detailResult);
      return {
        ok: true,
        result: {
          entry: detail,
          body: detail.body,
        },
      };
    }

    const args = ["browser", "network"];
    if (params.filter) args.push("--filter", params.filter);

    const result = await this.runOpenCLI(args);
    const entries = this.parseNetworkOutput(result);

    const apiEndpoints = entries.filter((e: Record<string, unknown>) =>
      String(e.content_type || "").includes("json") ||
      String(e.url || "").includes("/api/")
    );

    return {
      ok: true,
      result: {
        total_entries: entries.length,
        api_endpoints: apiEndpoints,
        all_entries: entries.slice(0, params.limit || 20),
      },
    };
  }

  private runOpenCLI(args: string[]): Promise<string> {
    return new Promise((resolve, reject) => {
      const proc = spawn("opencli", args, { timeout: 60000 });
      let stdout = "";
      let stderr = "";

      proc.stdout.on("data", (data) => { stdout += data; });
      proc.stderr.on("data", (data) => { stderr += data; });

      proc.on("close", (code) => {
        if (code === 0) resolve(stdout);
        else reject(new Error(stderr || `opencli exited with code ${code}`));
      });

      proc.on("error", (err) => reject(err));
    });
  }

  private parseStateOutput(output: string): PageSnapshot {
    const lines = output.split("\n");
    const elements: ElementInfo[] = [];
    const compounds: number[] = [];
    let interactiveCount = 0;

    for (const line of lines) {
      const match = line.match(/\[(\d+)\]\s*(\w+)(?:\[(.*?)\])?\s*(.*)?/);
      if (match) {
        const ref = parseInt(match[1], 10);
        const tag = match[2];
        const attrs = match[3] || "";
        const text = match[4] || "";

        const isInteractive = ["button", "a", "input", "select", "textarea"].includes(tag.toLowerCase()) ||
          attrs.includes("onclick") ||
          attrs.includes("role=");

        if (isInteractive) interactiveCount++;

        elements.push({
          ref,
          tag,
          text: text.trim(),
          visible: !line.includes("[hidden]"),
        });

        if (attrs.includes("select") || attrs.includes("date") || attrs.includes("file")) {
          compounds.push(ref);
        }
      }
    }

    return {
      url: "",
      title: "",
      elements,
      interactive_count: interactiveCount,
      compounds,
      scroll_position: { x: 0, y: 0 },
      has_more_below: output.includes("scroll-down"),
    };
  }

  private parseNetworkOutput(output: string): unknown[] {
    try {
      const parsed = JSON.parse(output);
      if (Array.isArray(parsed)) return parsed;
      if (parsed.entries) return parsed.entries;
      return [];
    } catch {
      return [];
    }
  }

  private parseActionResult(output: string): Record<string, unknown> {
    try {
      return JSON.parse(output);
    } catch {
      return { raw: output };
    }
  }

  private detectPageType(state: PageSnapshot): string {
    const tags = state.elements.map((e) => e.tag.toLowerCase());
    const texts = state.elements.map((e) => e.text?.toLowerCase() || "").join(" ");

    if (texts.includes("购物车") || texts.includes("cart") || texts.includes("checkout")) return "checkout";
    if (texts.includes("登录") || texts.includes("login") || texts.includes("sign in")) return "login";
    if (texts.includes("搜索") || texts.includes("search")) return "search";
    if (state.compounds.length > 3) return "form";
    if (tags.filter((t) => t === "article" || t === "section").length > 2) return "content";
    if (tags.filter((t) => t === "li" || t === "tr").length > 10) return "listing";
    if (texts.includes("价格") || texts.includes("price") || texts.includes("购买")) return "product";

    return "generic";
  }

  private detectLayoutPattern(state: PageSnapshot): string {
    const hasNav = state.elements.some((e) => e.tag === "nav");
    const hasAside = state.elements.some((e) => e.tag === "aside");
    const hasMain = state.elements.some((e) => e.tag === "main");

    if (hasNav && hasAside) return "three-column";
    if (hasNav || hasAside) return "two-column";
    if (hasMain) return "single-column";
    return "fluid";
  }

  private detectDataRegions(state: PageSnapshot): Array<{ selector: string; type: string }> {
    const regions: Array<{ selector: string; type: string }> = [];

    for (const el of state.elements) {
      if (el.tag === "main") regions.push({ selector: "main", type: "primary-content" });
      if (el.tag === "article") regions.push({ selector: "article", type: "article" });
      if (el.tag === "aside") regions.push({ selector: "aside", type: "sidebar" });
      if (el.tag === "table") regions.push({ selector: "table", type: "data-table" });
      if (el.tag === "ul" || el.tag === "ol") regions.push({ selector: el.tag, type: "list" });
    }

    return [...new Map(regions.map(r => [r.selector, r])).values()].slice(0, 5);
  }

  private detectPagination(state: PageSnapshot): { type: string; selector: string } | null {
    const paginationElements = state.elements.filter((e) =>
      e.text?.toLowerCase().includes("下一页") ||
      e.text?.toLowerCase().includes("next") ||
      e.text?.toLowerCase().includes("more")
    );

    if (paginationElements.length > 0) {
      const el = paginationElements[0];
      if (el.text?.includes("加载更多") || el.text?.includes("load more")) {
        return { type: "load-more", selector: `[${el.ref}]` };
      }
      return { type: "click", selector: `[${el.ref}]` };
    }

    if (state.has_more_below) {
      return { type: "scroll", selector: "window" };
    }

    return null;
  }

  private detectFormPurposes(state: PageSnapshot): Array<{ purpose: string; selectors: Record<string, string> }> {
    const forms: Array<{ purpose: string; selectors: Record<string, string> }> = [];
    const inputs = state.elements.filter((e) => e.tag === "input");

    if (inputs.length > 0) {
      forms.push({
        purpose: "input",
        selectors: {
          input: `[${inputs[0].ref}]`,
        },
      });
    }

    return forms;
  }

  private isInteractive(el: ElementInfo): boolean {
    return ["button", "a", "input", "select", "textarea"].includes(el.tag.toLowerCase());
  }

  private extractIndicators(state: PageSnapshot): string[] {
    const indicators: string[] = [];
    for (const el of state.elements.slice(0, 20)) {
      if (el.text && el.text.length < 50) {
        indicators.push(el.text.toLowerCase());
      }
    }
    return [...new Set(indicators)].slice(0, 10);
  }

  private suggestNextSteps(analysis: {
    page_type: string;
    pagination?: { type: string; selector: string } | null;
  }): string[] {
    const steps: string[] = [];

    if (analysis.page_type === "listing" && analysis.pagination) {
      steps.push(`处理分页: ${analysis.pagination.type} via ${analysis.pagination.selector}`);
    }
    if (analysis.page_type === "login") {
      steps.push("处理登录流程");
    }
    steps.push("捕获网络请求获取 API 端点");
    steps.push("保存网站模式供后续使用");

    return steps;
  }

  private generateBrowsingSteps(
    analysis: {
      page_type: string;
      pagination?: { type: string; selector: string } | null;
      data_regions: Array<{ selector: string; type: string }>;
    },
    plan: BrowsingPlan,
    depth: number,
    maxDepth: number,
  ): PlanStep[] {
    const steps: PlanStep[] = [];
    let stepId = plan.steps.length;

    if (analysis.page_type === "listing" && analysis.pagination && depth < maxDepth) {
      steps.push({
        id: `step-${++stepId}`,
        description: "采集当前页数据",
        action: "collect",
        params: { selector: analysis.data_regions[0]?.selector || "main" },
        dependencies: [],
        status: "pending",
        retry_count: 0,
        max_retries: 3,
        expected_outcome: "当前页数据已采集",
      });

      steps.push({
        id: `step-${++stepId}`,
        description: `翻页: ${analysis.pagination.type}`,
        action: "operate",
        params: { target: analysis.pagination.selector },
        dependencies: [`step-${stepId - 1}`],
        status: "pending",
        retry_count: 0,
        max_retries: 3,
        expected_outcome: "下一页已加载",
      });
    }

    for (const region of analysis.data_regions) {
      steps.push({
        id: `step-${++stepId}`,
        description: `提取 ${region.type} 数据`,
        action: "collect",
        params: { selector: region.selector },
        dependencies: [],
        status: "pending",
        retry_count: 0,
        max_retries: 2,
        expected_outcome: `${region.type} 数据已提取`,
      });
    }

    return steps;
  }

  private async readSitePatternMD(domain: string): Promise<SitePattern | null> {
    try {
      const filePath = path.join(MEMORY_BASE_DIR, "patterns", `${domain}.md`);
      const content = await fs.readFile(filePath, "utf-8");
      return this.parsePatternMD(content);
    } catch {
      return null;
    }
  }

  private parsePatternMD(content: string): SitePattern {
    const lines = content.split("\n");
    const pattern: SitePattern = {
      id: "",
      domain: "",
      page_types: {},
      navigation_flows: [],
      data_endpoints: [],
      selectors: {},
      learned_at: "",
      last_used: "",
      success_count: 0,
      failure_count: 0,
    };

    let currentSection = "";
    let currentPageType = "";

    for (const line of lines) {
      if (line.startsWith("# ")) {
        pattern.domain = line.slice(2).trim();
        pattern.id = pattern.domain;
      } else if (line.startsWith("> 域名:")) {
        pattern.domain = line.split(":")[1].trim();
      } else if (line.startsWith("> 学习时间:")) {
        pattern.learned_at = line.split(":")[1].trim();
      } else if (line.startsWith("> 最后使用:")) {
        pattern.last_used = line.split(":")[1].trim();
      } else if (line.startsWith("> 成功次数:")) {
        pattern.success_count = parseInt(line.split(":")[1].trim()) || 0;
      } else if (line.startsWith("> 失败次数:")) {
        pattern.failure_count = parseInt(line.split(":")[1].trim()) || 0;
      } else if (line.startsWith("### ")) {
        currentPageType = line.slice(4).split("（")[0].trim();
        currentSection = "page_type";
        pattern.page_types[currentPageType] = {
          type: currentPageType,
          indicators: [],
          data_regions: [],
        };
      } else if (line.startsWith("## ")) {
        currentSection = line.slice(3).toLowerCase().replace(/ /g, "_");
      } else if (line.startsWith("| ") && !line.includes("---")) {
        const cells = line.split("|").map(s => s.trim()).filter(Boolean);
        if (currentSection === "page_type" && currentPageType && cells.length >= 2) {
          if (cells[0] && cells[0] !== "选择器" && cells[0] !== "类型") {
            pattern.page_types[currentPageType].data_regions.push({
              selector: cells[0],
              type: cells[1] || "unknown",
            });
          }
        }
      }
    }

    return pattern;
  }

  private async writeSitePatternMD(pattern: SitePattern): Promise<void> {
    const filePath = path.join(MEMORY_BASE_DIR, "patterns", `${pattern.domain}.md`);
    
    let content = `# ${pattern.domain}

> 域名: ${pattern.domain}
> 学习时间: ${pattern.learned_at || new Date().toISOString()}
> 最后使用: ${pattern.last_used || new Date().toISOString()}
> 成功次数: ${pattern.success_count}
> 失败次数: ${pattern.failure_count}

`;

    content += `## 页面类型\n\n`;

    for (const [typeName, typeData] of Object.entries(pattern.page_types)) {
      content += `### ${typeName}\n\n`;
      
      if (typeData.indicators && typeData.indicators.length > 0) {
        content += `**识别特征**：\n`;
        typeData.indicators.forEach(i => {
          content += `- ${i}\n`;
        });
        content += "\n";
      }

      if (typeData.data_regions && typeData.data_regions.length > 0) {
        content += `**数据区域**：\n\n`;
        content += `| 选择器 | 类型 | 说明 |\n`;
        content += `|--------|------|------|\n`;
        typeData.data_regions.forEach(r => {
          content += `| ${r.selector} | ${r.type} | |\n`;
        });
        content += "\n";
      }

      if (typeData.pagination) {
        content += `**分页机制**：\n`;
        content += `- 类型: ${typeData.pagination.type}\n`;
        content += `- 选择器: ${typeData.pagination.selector}\n\n`;
      }
    }

    if (Object.keys(pattern.selectors).length > 0) {
      content += `## 选择器\n\n`;
      content += `| 名称 | 选择器 |\n`;
      content += `|------|--------|\n`;
      for (const [name, selector] of Object.entries(pattern.selectors)) {
        content += `| ${name} | ${selector} |\n`;
      }
      content += "\n";
    }

    await fs.writeFile(filePath, content);
    await this.updatePatternsIndex(pattern);
  }

  private async updatePatternsIndex(pattern: SitePattern): Promise<void> {
    const indexPath = path.join(MEMORY_BASE_DIR, "patterns", "INDEX.md");
    
    let indexContent = `# 网站模式索引

| 域名 | 文件 | 页面类型 | 最后使用 | 成功率 |
|------|------|---------|---------|--------|
`;

    const entries: Array<{ domain: string; file: string; pageTypes: string[]; lastUsed: string; successRate: string }> = [];
    
    try {
      const existing = await fs.readFile(indexPath, "utf-8");
      const lines = existing.split("\n").filter(l => l.startsWith("|") && !l.includes("---") && !l.includes("域名"));
      
      for (const line of lines) {
        const cells = line.split("|").map(s => s.trim()).filter(Boolean);
        if (cells.length >= 5) {
          entries.push({
            domain: cells[0],
            file: cells[1].replace(/\[([^\]]+)\].*/, "$1"),
            pageTypes: cells[2].split(", "),
            lastUsed: cells[3],
            successRate: cells[4],
          });
        }
      }
    } catch {}

    const existingIdx = entries.findIndex(e => e.domain === pattern.domain);
    const successRate = pattern.success_count + pattern.failure_count > 0
      ? Math.round(pattern.success_count / (pattern.success_count + pattern.failure_count) * 100) + "%"
      : "N/A";

    const newEntry = {
      domain: pattern.domain,
      file: `${pattern.domain}.md`,
      pageTypes: Object.keys(pattern.page_types),
      lastUsed: pattern.last_used.split("T")[0],
      successRate,
    };

    if (existingIdx >= 0) {
      entries[existingIdx] = newEntry;
    } else {
      entries.push(newEntry);
    }

    for (const e of entries) {
      indexContent += `| ${e.domain} | [${e.file}](./${e.file}) | ${e.pageTypes.join(", ")} | ${e.lastUsed} | ${e.successRate} |\n`;
    }

    await fs.writeFile(indexPath, indexContent);
  }

  private async readPlanMD(taskId: string): Promise<BrowsingPlan | null> {
    try {
      const filePath = path.join(MEMORY_BASE_DIR, "plans", `${taskId}.md`);
      const content = await fs.readFile(filePath, "utf-8");
      return this.parsePlanMD(content);
    } catch {
      return null;
    }
  }

  private parsePlanMD(content: string): BrowsingPlan {
    const lines = content.split("\n");
    const plan: BrowsingPlan = {
      id: "",
      goal: "",
      current_depth: 0,
      max_depth: 3,
      steps: [],
      completed_steps: [],
      current_step: null,
      collected_data: [],
      created_at: "",
      status: "pending",
    };

    let currentStep: PlanStep | null = null;

    for (const line of lines) {
      if (line.startsWith("> 任务ID:")) {
        plan.id = line.split(":")[1].trim();
      } else if (line.startsWith("> 目标:")) {
        plan.goal = line.split(":").slice(1).join(":").trim();
      } else if (line.startsWith("> 当前深度:")) {
        plan.current_depth = parseInt(line.split(":")[1].trim()) || 0;
      } else if (line.startsWith("> 最大深度:")) {
        plan.max_depth = parseInt(line.split(":")[1].trim()) || 3;
      } else if (line.startsWith("> 状态:")) {
        plan.status = line.split(":")[1].trim();
      } else if (line.startsWith("> 创建时间:")) {
        plan.created_at = line.split(":").slice(1).join(":").trim();
      } else if (line.startsWith("### Step ")) {
        if (currentStep) {
          plan.steps.push(currentStep);
        }
        const match = line.match(/Step (\d+): (.+?)(?:\s*(✅|🔄|⏳|❌))?$/);
        if (match) {
          currentStep = {
            id: `step-${match[1]}`,
            description: match[2].trim(),
            action: "",
            params: {},
            dependencies: [],
            status: match[3] === "✅" ? "completed" : match[3] === "🔄" ? "in_progress" : match[3] === "❌" ? "failed" : "pending",
            retry_count: 0,
            max_retries: 3,
            expected_outcome: "",
          };
        }
      } else if (currentStep) {
        if (line.startsWith("- 操作:")) {
          currentStep.action = line.split(":")[1].trim();
        } else if (line.startsWith("- 参数:")) {
          try {
            currentStep.params = JSON.parse(line.split(":").slice(1).join(":").trim());
          } catch {}
        } else if (line.startsWith("- 依赖:")) {
          currentStep.dependencies = line.split(":")[1].trim().split(", ").filter(Boolean);
        } else if (line.startsWith("- 状态:")) {
          const status = line.split(":")[1].trim();
          currentStep.status = status === "已完成" ? "completed" : status === "进行中" ? "in_progress" : status === "失败" ? "failed" : "pending";
        }
      }
    }

    if (currentStep) {
      plan.steps.push(currentStep);
    }

    plan.completed_steps = plan.steps.filter(s => s.status === "completed").map(s => s.id);
    plan.current_step = plan.steps.find(s => s.status === "in_progress")?.id || null;

    return plan;
  }

  private async writePlanMD(plan: BrowsingPlan): Promise<void> {
    const filePath = path.join(MEMORY_BASE_DIR, "plans", `${plan.id}.md`);
    
    let content = `# 浏览计划: ${plan.goal}

> 任务ID: ${plan.id}
> 目标: ${plan.goal}
> 当前深度: ${plan.current_depth}
> 最大深度: ${plan.max_depth}
> 状态: ${plan.status}
> 创建时间: ${plan.created_at}

## 进度概览

- 总步骤: ${plan.steps.length}
- 已完成: ${plan.steps.filter(s => s.status === "completed").length}
- 进行中: ${plan.steps.filter(s => s.status === "in_progress").length}
- 待执行: ${plan.steps.filter(s => s.status === "pending").length}

## 执行步骤

`;

    for (const step of plan.steps) {
      const statusIcon = step.status === "completed" ? "✅" : 
                         step.status === "in_progress" ? "🔄" : 
                         step.status === "failed" ? "❌" : "⏳";
      const statusText = step.status === "completed" ? "已完成" :
                         step.status === "in_progress" ? "进行中" :
                         step.status === "failed" ? "失败" : "待执行";

      content += `### ${step.id.replace("step-", "Step ")}: ${step.description} ${statusIcon}\n\n`;
      content += `- 状态: ${statusText}\n`;
      content += `- 操作: ${step.action}\n`;
      content += `- 参数: ${JSON.stringify(step.params)}\n`;
      if (step.dependencies.length > 0) {
        content += `- 依赖: ${step.dependencies.join(", ")}\n`;
      }
      content += `- 预期: ${step.expected_outcome}\n`;
      if (step.executed_at) {
        content += `- 执行时间: ${step.executed_at}\n`;
      }
      content += "\n";
    }

    await fs.writeFile(filePath, content);
    await this.updatePlansIndex(plan);
  }

  private async updatePlansIndex(plan: BrowsingPlan): Promise<void> {
    const indexPath = path.join(MEMORY_BASE_DIR, "plans", "INDEX.md");
    
    let indexContent = `# 浏览计划索引

| 任务ID | 目标 | 状态 | 文件 | 创建时间 |
|--------|------|------|------|---------|
`;

    const entries: Array<{ id: string; goal: string; status: string; created: string }> = [];
    
    try {
      const existing = await fs.readFile(indexPath, "utf-8");
      const lines = existing.split("\n").filter(l => l.startsWith("|") && !l.includes("---") && !l.includes("任务ID"));
      
      for (const line of lines) {
        const cells = line.split("|").map(s => s.trim()).filter(Boolean);
        if (cells.length >= 5) {
          entries.push({
            id: cells[0],
            goal: cells[1],
            status: cells[2],
            created: cells[4].replace(/\[([^\]]+)\].*/, "$1"),
          });
        }
      }
    } catch {}

    const existingIdx = entries.findIndex(e => e.id === plan.id);
    const newEntry = {
      id: plan.id,
      goal: plan.goal.slice(0, 30) + (plan.goal.length > 30 ? "..." : ""),
      status: plan.status,
      created: plan.created_at.split("T")[0],
    };

    if (existingIdx >= 0) {
      entries[existingIdx] = newEntry;
    } else {
      entries.push(newEntry);
    }

    for (const e of entries) {
      indexContent += `| ${e.id} | ${e.goal} | ${e.status} | [${e.id}.md](./${e.id}.md) | ${e.created} |\n`;
    }

    await fs.writeFile(indexPath, indexContent);
  }
}
