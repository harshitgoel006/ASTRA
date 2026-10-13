import assert from "node:assert/strict";
import { test } from "node:test";
import { TaskController } from "../server/controllers/taskController.js";
import { TaskRepository } from "../server/repositories/taskRepository.js";
import { TaskService } from "../server/services/taskService.js";

test("completed tasks are removed from the pending task list", () => {
  const repository = new TaskRepository();
  const service = new TaskService(repository);
  const controller = new TaskController(service);

  const task = controller.create({ title: "Prepare ASTRA milestone report" });
  controller.complete({ id: task.id });

  assert.deepEqual(controller.pending(), []);
});
