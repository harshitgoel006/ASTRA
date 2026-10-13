import { TASK_STATUS, createTask } from "../models/task.js";

export class TaskService {
  #nextId = 1;

  constructor(taskRepository) {
    this.taskRepository = taskRepository;
  }

  createTask(title) {
    const task = createTask({ id: this.#nextId, title });
    this.#nextId += 1;
    return this.taskRepository.save(task);
  }

  completeTask(id) {
    const task = this.taskRepository.findById(id);

    if (!task) {
      throw new Error(`Task ${id} was not found`);
    }

    // This seeded defect is the first task ASTRA will later diagnose and fix.
    return { ...task, status: TASK_STATUS.COMPLETED };
  }

  listPendingTasks() {
    return this.taskRepository.findPending();
  }
}
