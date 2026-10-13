export class TaskRepository {
  #tasks = new Map();

  save(task) {
    this.#tasks.set(task.id, task);
    return task;
  }

  findById(id) {
    return this.#tasks.get(id);
  }

  findPending() {
    return [...this.#tasks.values()].filter((task) => task.status === "pending");
  }
}
