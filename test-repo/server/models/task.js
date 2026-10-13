export const TASK_STATUS = Object.freeze({
  PENDING: "pending",
  COMPLETED: "completed",
});

export function createTask({ id, title, status = TASK_STATUS.PENDING }) {
  return { id, title, status };
}
