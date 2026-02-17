"""Output formatting for CLI display."""

from datetime import datetime
from src.models.task import Task


def format_task_created(task: Task) -> str:
    """Format output for task creation.

    Args:
        task: The created task.

    Returns:
        Formatted success message.
    """
    return f"""✓ Task created successfully
  ID: {task.id}
  Title: {task.title}
  Description: {task.description if task.description else "(none)"}
  Status: {"Complete" if task.completed else "Incomplete"}
  Created: {task.created_at.strftime("%Y-%m-%d %H:%M:%S")}"""


def format_task_list(tasks: list[Task]) -> str:
    """Format output for task list display.

    Args:
        tasks: List of tasks to display.

    Returns:
        Formatted task list or empty message.
    """
    if not tasks:
        return "No tasks found.\n\nUse 'todo add <title>' to create your first task."

    # Build table header
    output = "Your Tasks:\n\n"
    output += "ID | Status | Title              | Description          | Created\n"
    output += "---+--------+--------------------+----------------------+-------------------\n"

    # Add each task row
    for task in tasks:
        status = "[✓]" if task.completed else "[ ]"
        title = task.title[:18] + ".." if len(task.title) > 20 else task.title.ljust(18)
        desc = task.description[:18] + ".." if len(task.description) > 20 else task.description.ljust(20)
        created = task.created_at.strftime("%Y-%m-%d %H:%M")

        output += f"{task.id:<2} | {status:6} | {title} | {desc} | {created}\n"

    # Add summary
    total = len(tasks)
    completed = sum(1 for t in tasks if t.completed)
    incomplete = total - completed
    output += f"\nTotal: {total} tasks ({completed} completed, {incomplete} incomplete)"

    return output


def format_task_completed(task: Task) -> str:
    """Format output for task completion toggle.

    Args:
        task: The toggled task.

    Returns:
        Formatted success message.
    """
    status = "complete" if task.completed else "incomplete"
    return f"""✓ Task marked as {status}
  ID: {task.id}
  Title: {task.title}
  Status: {"Complete" if task.completed else "Incomplete"}"""


def format_task_updated(task: Task) -> str:
    """Format output for task update.

    Args:
        task: The updated task.

    Returns:
        Formatted success message.
    """
    return f"""✓ Task updated successfully
  ID: {task.id}
  Title: {task.title}
  Description: {task.description if task.description else "(none)"}
  Status: {"Complete" if task.completed else "Incomplete"}"""


def format_task_deleted(task: Task) -> str:
    """Format output for task deletion.

    Args:
        task: The deleted task.

    Returns:
        Formatted success message.
    """
    return f"""✓ Task deleted successfully
  ID: {task.id}
  Title: {task.title}"""


def format_error(message: str) -> str:
    """Format error message.

    Args:
        message: The error message.

    Returns:
        Formatted error message.
    """
    return f"Error: {message}"
