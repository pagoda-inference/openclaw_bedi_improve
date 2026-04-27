import type { OpenClawPluginApi } from "../../types.js";
import { TaskManagerTool } from "./tools/task-manager.js";
import { ReportRendererTool } from "./tools/report-renderer.js";
import { DeepBrowserTool } from "./tools/deep-browser.js";

export function register(api: OpenClawPluginApi): void {
  api.registerTool(new TaskManagerTool());
  api.registerTool(new ReportRendererTool());
  api.registerTool(new DeepBrowserTool());
}

export function activate(api: OpenClawPluginApi): void {
  api.logger.info("Market Research plugin activated");
}
