import type { AgentToolResult } from "@mariozechner/pi-agent-core";
import type { TSchema } from "typebox";
import fs from "node:fs/promises";
import path from "node:path";
import { randomUUID } from "crypto";
import os from "os";

const TASK_BASE_DIR = path.join(os.homedir(), ".openclaw", "tasks");

export type TaskManagerParams = {
  action: "create" | "get" | "update" | "list" | "recover";
  task_id?: string;
  user_input?: string;
  config?: Record<string, unknown>;
  status?: string;
  data?: Record<string, unknown>;
};

export class TaskManagerTool {
  name = "task_manager";
  description = "创建和管理市场调研任务";

  definition = {
    name: this.name,
    description: this.description,
    input_schema: {
      type: "object",
      properties: {
        action: {
          type: "string",
          enum: ["create", "get", "update", "list", "recover"],
          description: "操作类型",
        },
        task_id: { type: "string", description: "任务 ID" },
        user_input: { type: "string", description: "用户原始需求" },
        config: {
          type: "object",
          properties: {
            research_depth: { type: "string", enum: ["quick", "standard", "deep"] },
            output_formats: { type: "array", items: { type: "string" } },
            time_limit_minutes: { type: "number" },
            max_pages: { type: "number" },
            language: { type: "string" },
          },
        },
        status: { type: "string", description: "新状态" },
        data: { type: "object", description: "要更新的数据" },
      },
      required: ["action"],
    } as unknown as TSchema,
  };

  async execute(
    _toolCallId: string,
    params: TaskManagerParams,
    _signal?: AbortSignal,
  ): Promise<AgentToolResult<unknown>> {
    try {
      switch (params.action) {
        case "create":
          return await this.createTask(params.user_input!, params.config);
        case "get":
          return await this.getTask(params.task_id!);
        case "update":
          return await this.updateTask(params.task_id!, params.status, params.data);
        case "list":
          return await this.listTasks();
        case "recover":
          return await this.recoverTask(params.task_id!);
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

  private async createTask(
    userInput: string,
    config?: Record<string, unknown>,
  ): Promise<AgentToolResult<unknown>> {
    const taskId = `task-${new Date().toISOString().slice(0, 10).replace(/-/g, "")}-${randomUUID().slice(0, 6)}`;
    const taskDir = path.join(TASK_BASE_DIR, taskId);

    await fs.mkdir(taskDir, { recursive: true });
    await fs.mkdir(path.join(taskDir, "data", "raw"), { recursive: true });
    await fs.mkdir(path.join(taskDir, "data", "processed"), { recursive: true });
    await fs.mkdir(path.join(taskDir, "data", "analysis"), { recursive: true });
    await fs.mkdir(path.join(taskDir, "memory"), { recursive: true });
    await fs.mkdir(path.join(taskDir, "output"), { recursive: true });
    await fs.mkdir(path.join(taskDir, "logs"), { recursive: true });

    const task = {
      task_id: taskId,
      task_type: "market_research",
      status: "pending",
      user_input: userInput,
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
      progress: { phase: "created", percentage: 0 },
    };

    await fs.writeFile(path.join(taskDir, "task.json"), JSON.stringify(task, null, 2));
    await fs.writeFile(
      path.join(taskDir, "config.json"),
      JSON.stringify(config || {}, null, 2),
    );

    return { ok: true, result: { task_id: taskId, task_dir: taskDir } };
  }

  private async getTask(taskId: string): Promise<AgentToolResult<unknown>> {
    const content = await fs.readFile(
      path.join(TASK_BASE_DIR, taskId, "task.json"),
      "utf-8",
    );
    return { ok: true, result: JSON.parse(content) };
  }

  private async updateTask(
    taskId: string,
    status?: string,
    data?: Record<string, unknown>,
  ): Promise<AgentToolResult<unknown>> {
    const taskPath = path.join(TASK_BASE_DIR, taskId, "task.json");
    const task = JSON.parse(await fs.readFile(taskPath, "utf-8"));

    if (status) task.status = status;
    task.updated_at = new Date().toISOString();
    if (data) Object.assign(task, data);

    await fs.writeFile(taskPath, JSON.stringify(task, null, 2));
    return { ok: true, result: task };
  }

  private async listTasks(): Promise<AgentToolResult<unknown>> {
    const entries = await fs.readdir(TASK_BASE_DIR);
    const tasks = await Promise.all(
      entries
        .filter((e) => e.startsWith("task-"))
        .map(async (e) => {
          try {
            const content = await fs.readFile(
              path.join(TASK_BASE_DIR, e, "task.json"),
              "utf-8",
            );
            return JSON.parse(content);
          } catch {
            return null;
          }
        }),
    );
    return { ok: true, result: { tasks: tasks.filter(Boolean), count: tasks.length } };
  }

  private async recoverTask(taskId: string): Promise<AgentToolResult<unknown>> {
    const taskPath = path.join(TASK_BASE_DIR, taskId, "task.json");
    const task = JSON.parse(await fs.readFile(taskPath, "utf-8"));
    const memoryDir = path.join(TASK_BASE_DIR, taskId, "memory");

    const memoryFiles = await fs.readdir(memoryDir).catch(() => []);
    const memory: Record<string, unknown> = {};
    for (const file of memoryFiles.filter((f) => f.endsWith(".json"))) {
      const content = await fs.readFile(path.join(memoryDir, file), "utf-8");
      memory[file.replace(".json", "")] = JSON.parse(content);
    }

    return { ok: true, result: { task, recovered_memory: memory } };
  }
}
