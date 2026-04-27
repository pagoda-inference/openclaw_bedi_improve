import type { AgentToolResult } from "@mariozechner/pi-agent-core";
import type { TSchema } from "typebox";

export type ReportRendererParams = {
  template: string;
  title: string;
  sections: Array<{
    id: string;
    title: string;
    content: unknown;
    content_type: string;
  }>;
  metadata?: {
    generated_at?: string;
    data_source_count?: number;
    topic?: string;
  };
};

export class ReportRendererTool {
  name = "report_renderer";
  description = "将报告内容渲染为 HTML";

  definition = {
    name: this.name,
    description: this.description,
    input_schema: {
      type: "object",
      properties: {
        template: { type: "string", description: "模板名称" },
        title: { type: "string", description: "报告标题" },
        sections: {
          type: "array",
          items: {
            type: "object",
            properties: {
              id: { type: "string" },
              title: { type: "string" },
              content: { type: "string" },
              content_type: { type: "string" },
            },
          },
        },
        metadata: {
          type: "object",
          properties: {
            generated_at: { type: "string" },
            data_source_count: { type: "number" },
            topic: { type: "string" },
          },
        },
      },
      required: ["template", "title", "sections"],
    } as unknown as TSchema,
  };

  async execute(
    _toolCallId: string,
    params: ReportRendererParams,
    _signal?: AbortSignal,
  ): Promise<AgentToolResult<unknown>> {
    try {
      const html = this.generateHtml(params);
      return {
        ok: true,
        result: {
          html,
          file_path: "output/report.html",
          preview: html.substring(0, 500) + "...",
        },
      };
    } catch (error) {
      return {
        ok: false,
        error: error instanceof Error ? error.message : "Unknown error",
      };
    }
  }

  private generateHtml(params: ReportRendererParams): string {
    const { title, sections, metadata } = params;
    const sectionsHtml = sections
      .map(
        (s) => `
    <div class="section">
      <h2>${this.escapeHtml(s.title)}</h2>
      <div class="section-content">
        ${typeof s.content === "string" ? this.escapeHtml(s.content) : JSON.stringify(s.content, null, 2)}
      </div>
    </div>`,
      )
      .join("\n");

    return `<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>${this.escapeHtml(title)}</title>
  <style>
    body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; line-height: 1.6; max-width: 900px; margin: 0 auto; padding: 40px 20px; }
    h1 { font-size: 2em; margin-bottom: 0.5em; }
    .metadata { color: #666; font-size: 0.9em; margin-bottom: 2em; padding-bottom: 1em; border-bottom: 1px solid #eee; }
    h2 { font-size: 1.4em; margin: 1.5em 0 0.8em; }
    .section-content { background: #fafafa; padding: 1.2em; border-radius: 8px; white-space: pre-wrap; }
    table { width: 100%; border-collapse: collapse; margin: 1em 0; }
    th, td { padding: 0.75em; text-align: left; border-bottom: 1px solid #eee; }
    th { background: #f5f5f5; font-weight: 600; }
    footer { margin-top: 3em; padding-top: 1em; border-top: 1px solid #eee; color: #666; font-size: 0.85em; }
  </style>
</head>
<body>
  <h1>${this.escapeHtml(title)}</h1>
  <div class="metadata">
    <p>生成时间：${metadata?.generated_at || new Date().toISOString()}</p>
    ${metadata?.data_source_count ? `<p>数据来源：${metadata.data_source_count} 个来源</p>` : ""}
  </div>
  ${sectionsHtml}
  <footer><p>由 OpenClaw Market Research 能力生成</p></footer>
</body>
</html>`;
  }

  private escapeHtml(text: string): string {
    return text
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }
}
