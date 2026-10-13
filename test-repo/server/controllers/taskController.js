export class TaskController {
  constructor(taskService) {
    this.taskService = taskService;
  }

  create({ title }) {
    return this.taskService.createTask(title);
  }

  complete({ id }) {
    return this.taskService.completeTask(id);
  }

  pending() {
    return this.taskService.listPendingTasks();
  }
}
