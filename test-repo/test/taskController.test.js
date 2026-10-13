import assert from "node:assert/strict";
import { test } from "node:test";
import { TaskController } from "../server/controllers/taskController.js";
import { TaskRepository } from "../server/repositories/taskRepository.js";
import { TaskService } from "../server/services/taskService.js";

test("TaskController.complete removes a task from pending tasks", () => {
  console.log("[target test] files under test:");
  console.log("[target test] - server/controllers/taskController.js");
  console.log("[target test] - server/services/taskService.js");
  console.log("[target test] - server/repositories/taskRepository.js");
  console.log("[target test] - server/models/task.js");

  const repository = new TaskRepository();
  const service = new TaskService(repository);
  const controller = new TaskController(service);

  const task = controller.create({ title: "Prepare ASTRA milestone report" });
  console.log(`[target test] created task: ${JSON.stringify(task)}`);

  controller.complete({ id: task.id });
  const pendingTasks = controller.pending();
  console.log(
    `[target test] pending tasks after completion: ${JSON.stringify(pendingTasks)}`,
  );

  assert.deepEqual(
    pendingTasks,
    [],
    "taskController.pending() should not return a task after completion",
  );
});
