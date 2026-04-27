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
  | "collect";

export type DeepBrowserParams = {
  action: DeepBrowserAction;
  url?: string;
  selector?: string;
  text?: string;
  direction?: "up" | "down" | "top" | "bottom";
  timeout?: number;
  save_to?: string;
  selectors?: {
    title?: string;
    content?: string;
    metadata?: string;
    list_items?: string;
    pagination?: string;
  };
  operation_type?: "click" | "type" | "scroll" | "wait" | "navigate";
  expected_change?: string;
  site_pattern_id?: string;
};

type PageAnalysis = {
  page_type: string;
  layout_pattern: string;
  content_structure: string;
  interactive_elements: Array<{ selector: string; type: string; label: string }>;
  data_regions: Array<{ selector: string; type: string; description: string }>;
  pagination?: { type: string; selector: string };
};

type SitePattern = {
  id: string;
  domain: string;
  page_type: string;
  layout_pattern: string;
  selectors: Record<string, string>;
  pagination?: { type: string; selector: string };
  learned_at: string;
  success_count: number;
};

export class DeepBrowserTool {
  name = "deep_browser";
  description = "深度浏览器操作：理解页面结构、执行复杂交互、观察变化、积累记忆";

  definition = {
    name: this.name,
    description: this.description,
    input_schema: {
      type: "object",
      properties: {
        action: {
          type: "string",
          enum: ["understand", "operate", "observe", "remember", "collect"],
          description: "操作类型：understand(理解页面)、operate(执行操作)、observe(观察变化)、remember(记录记忆)、collect(采集内容)",
        },
        url: { type: "string", description: "URL（open/collect 时使用）" },
        selector: { type: "string", description: "CSS 选择器" },
        text: { type: "string", description: "输入文本（type 时使用）" },
        direction: {
          type: "string",
          enum: ["up", "down", "top", "bottom"],
          description: "滚动方向",
        },
        timeout: { type: "number", description: "超时时间（毫秒）" },
        save_to: { type: "string", description: "保存路径" },
        selectors: {
          type: "object",
          description: "内容提取选择器",
          properties: {
            title: { type: "string" },
            content: { type: "string" },
            metadata: { type: "string" },
            list_items: { type: "string" },
            pagination: { type: "string" },
          },
        },
        operation_type: {
          type: "string",
          enum: ["click", "type", "scroll", "wait", "navigate"],
          description: "操作类型（operate 时使用）",
        },
        expected_change: { type: "string", description: "预期变化（observe 时使用）" },
        site_pattern_id: { type: "string", description: "网站模式 ID" },
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

  private async understandPage(params: DeepBrowserParams): Promise<AgentToolResult<unknown>> {
    if (!params.url) {
      return { ok: false, error: "URL is required for understand action" };
    }

    const existingPattern = await this.findSitePattern(params.url);
    if (existingPattern) {
      return {
        ok: true,
        result: {
          source: "memory",
          page_analysis: existingPattern,
          message: "Loaded from cached site pattern",
        },
      };
    }

    const html = await this.fetchPageContent(params.url);
    const analysis = this.analyzePageStructure(html, params.url);

    return {
      ok: true,
      result: {
        source: "analysis",
        page_analysis: analysis,
        message: "Page structure analyzed",
      },
    };
  }

  private async executeOperation(params: DeepBrowserParams): Promise<AgentToolResult<unknown>> {
    const operationType = params.operation_type || "click";

    switch (operationType) {
      case "navigate":
        if (!params.url) return { ok: false, error: "URL required for navigate" };
        await this.runOpenCLI(["browser", "open", params.url]);
        return { ok: true, result: { action: "navigated", url: params.url } };

      case "click":
        if (!params.selector) return { ok: false, error: "Selector required for click" };
        await this.runOpenCLI(["browser", "click", params.selector]);
        return { ok: true, result: { action: "clicked", selector: params.selector } };

      case "type":
        if (!params.selector || !params.text) {
          return { ok: false, error: "Selector and text required for type" };
        }
        await this.runOpenCLI(["browser", "type", params.selector, params.text]);
        return { ok: true, result: { action: "typed", selector: params.selector } };

      case "scroll":
        const direction = params.direction || "down";
        await this.runOpenCLI(["browser", "scroll", `--${direction}`]);
        return { ok: true, result: { action: "scrolled", direction } };

      case "wait":
        if (!params.selector) return { ok: false, error: "Selector required for wait" };
        const timeout = params.timeout ? `--timeout ${params.timeout}` : "";
        await this.runOpenCLI(["browser", "wait", params.selector, timeout].filter(Boolean));
        return { ok: true, result: { action: "waited", selector: params.selector } };

      default:
        return { ok: false, error: `Unknown operation type: ${operationType}` };
    }
  }

  private async observeChanges(params: DeepBrowserParams): Promise<AgentToolResult<unknown>> {
    const content = await this.runOpenCLI(["browser", "content"]);
    const screenshot = await this.runOpenCLI(["browser", "screenshot", "--output", "temp.png"]);

    return {
      ok: true,
      result: {
        content_length: content.length,
        has_content: content.length > 0,
        screenshot_taken: screenshot.includes("saved") || screenshot.includes("success"),
        observed_at: new Date().toISOString(),
        expected_change: params.expected_change || null,
      },
    };
  }

  private async saveMemory(params: DeepBrowserParams): Promise<AgentToolResult<unknown>> {
    await fs.mkdir(MEMORY_BASE_DIR, { recursive: true });
    await fs.mkdir(path.join(MEMORY_BASE_DIR, "patterns"), { recursive: true });
    await fs.mkdir(path.join(MEMORY_BASE_DIR, "sessions"), { recursive: true });

    if (params.site_pattern_id && params.selectors) {
      const patternPath = path.join(MEMORY_BASE_DIR, "patterns", `${params.site_pattern_id}.json`);
      const pattern: SitePattern = {
        id: params.site_pattern_id,
        domain: params.url ? new URL(params.url).hostname : "unknown",
        page_type: "auto-detected",
        layout_pattern: "custom",
        selectors: params.selectors,
        learned_at: new Date().toISOString(),
        success_count: 1,
      };

      await fs.writeFile(patternPath, JSON.stringify(pattern, null, 2));
      return { ok: true, result: { saved: true, pattern_id: params.site_pattern_id } };
    }

    return { ok: false, error: "site_pattern_id and selectors required for remember action" };
  }

  private async collectContent(params: DeepBrowserParams): Promise<AgentToolResult<unknown>> {
    if (!params.url) {
      return { ok: false, error: "URL is required for collect action" };
    }

    const html = await this.fetchPageContent(params.url);
    const extracted = this.extractContent(html, params.selectors);

    if (params.save_to) {
      await fs.writeFile(params.save_to, JSON.stringify(extracted, null, 2));
    }

    return {
      ok: true,
      result: {
        extracted,
        saved_to: params.save_to || null,
        collected_at: new Date().toISOString(),
      },
    };
  }

  private async fetchPageContent(url: string): Promise<string> {
    try {
      const result = await this.runOpenCLI(["browser", "open", url, "--headless"]);
      const content = await this.runOpenCLI(["browser", "content"]);
      return content;
    } catch {
      const response = await fetch(url);
      return await response.text();
    }
  }

  private async runOpenCLI(args: string[]): Promise<string> {
    return new Promise((resolve, reject) => {
      const proc = spawn("opencli", args, { timeout: 30000 });
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

  private analyzePageStructure(html: string, url: string): PageAnalysis {
    const domain = new URL(url).hostname;
    const analysis: PageAnalysis = {
      page_type: this.detectPageType(html),
      layout_pattern: this.detectLayoutPattern(html),
      content_structure: this.detectContentStructure(html),
      interactive_elements: this.detectInteractiveElements(html),
      data_regions: this.detectDataRegions(html),
    };

    const pagination = this.detectPagination(html);
    if (pagination) {
      analysis.pagination = pagination;
    }

    return analysis;
  }

  private detectPageType(html: string): string {
    const lowerHtml = html.toLowerCase();
    if (lowerHtml.includes("product") && lowerHtml.includes("price")) return "ecommerce-product";
    if (lowerHtml.includes("search-result") || lowerHtml.includes("search result")) return "search-results";
    if (lowerHtml.includes("article") || lowerHtml.includes("blog")) return "article";
    if (lowerHtml.includes("documentation") || lowerHtml.includes("docs")) return "documentation";
    if (lowerHtml.includes("listing") || lowerHtml.includes("list")) return "listing";
    return "generic";
  }

  private detectLayoutPattern(html: string): string {
    if (html.includes("grid") || html.includes("flex")) return "grid";
    if (html.includes("sidebar")) return "sidebar";
    if (html.includes("hero")) return "hero";
    return "standard";
  }

  private detectContentStructure(html: string): string {
    if (html.includes("<table")) return "table";
    if (html.includes("<ul") || html.includes("<ol")) return "list";
    if (html.includes("<article")) return "article";
    return "mixed";
  }

  private detectInteractiveElements(html: string): Array<{ selector: string; type: string; label: string }> {
    const elements: Array<{ selector: string; type: string; label: string }> = [];
    const buttonMatches = html.matchAll(/<button[^>]*>([^<]*)<\/button>/gi);
    for (const match of buttonMatches) {
      elements.push({ selector: "button", type: "button", label: match[1].trim() });
    }
    const inputMatches = html.matchAll(/<input[^>]*type="([^"]*)"[^>]*placeholder="([^"]*)"/gi);
    for (const match of inputMatches) {
      elements.push({ selector: `input[type="${match[1]}"]`, type: match[1], label: match[2] });
    }
    return elements.slice(0, 10);
  }

  private detectDataRegions(html: string): Array<{ selector: string; type: string; description: string }> {
    const regions: Array<{ selector: string; type: string; description: string }> = [];
    if (html.includes("main")) regions.push({ selector: "main", type: "main-content", description: "Main content area" });
    if (html.includes("article")) regions.push({ selector: "article", type: "article", description: "Article content" });
    if (html.includes("aside")) regions.push({ selector: "aside", type: "sidebar", description: "Sidebar content" });
    return regions;
  }

  private detectPagination(html: string): { type: string; selector: string } | null {
    if (html.includes("pagination") || html.includes("page-next")) {
      return { type: "click", selector: ".pagination-next, .page-next, [rel='next']" };
    }
    if (html.includes("load-more") || html.includes("load more")) {
      return { type: "load-more", selector: ".load-more, [data-load-more]" };
    }
    if (html.includes("infinite-scroll") || html.includes("infinite scroll")) {
      return { type: "scroll", selector: "window" };
    }
    return null;
  }

  private extractContent(
    html: string,
    selectors?: { title?: string; content?: string; metadata?: string; list_items?: string },
  ): Record<string, unknown> {
    const result: Record<string, unknown> = {};

    if (selectors?.title) {
      const match = html.match(new RegExp(`<[^>]*${selectors.title}[^>]*>([^<]*)<`, "i"));
      result.title = match ? match[1].trim() : "";
    }

    if (selectors?.content) {
      const match = html.match(new RegExp(`<[^>]*${selectors.content}[^>]*>([\\s\\S]*?)<\\/`, "i"));
      result.content = match ? match[1].replace(/<[^>]*>/g, "").trim() : "";
    }

    if (selectors?.list_items) {
      const items = html.match(new RegExp(`<[^>]*${selectors.list_items}[^>]*>([\\s\\S]*?)<\\/`, "gi")) || [];
      result.list_items = items.map((item) => item.replace(/<[^>]*>/g, "").trim()).filter(Boolean);
    }

    result.raw_length = html.length;
    result.extracted_at = new Date().toISOString();

    return result;
  }

  private async findSitePattern(url: string): Promise<SitePattern | null> {
    try {
      const domain = new URL(url).hostname;
      const patternsDir = path.join(MEMORY_BASE_DIR, "patterns");
      const files = await fs.readdir(patternsDir).catch(() => []);

      for (const file of files) {
        if (file.endsWith(".json")) {
          const content = await fs.readFile(path.join(patternsDir, file), "utf-8");
          const pattern: SitePattern = JSON.parse(content);
          if (pattern.domain === domain) {
            return pattern;
          }
        }
      }
    } catch {}

    return null;
  }
}
