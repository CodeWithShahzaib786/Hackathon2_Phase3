"""CLI command handlers for the todo console application."""

import sys
from typing import Optional

from src.services.task_service import TaskService
from src.models.exceptions import TaskNotFoundError, ValidationError
from src.cli.formatter import (
    format_task_created,
    format_task_list,
    format_task_completed,
    format_task_updated,
    format_task_deleted,
    format_error,
)

# Global task service instance
task_service = TaskService()


def handle_add(title: str, description: str = "") -> None:
    """Handle the 'add' command to create a new task.

    Args:
        title: The task title.
        description: The task description (optional).
    """
    try:
        task = task_service.create_task(title, description)
        print(format_task_created(task))
    except ValidationError as e:
        print(format_error(str(e)))
        sys.exit(1)


def handle_list() -> None:
    """Handle the 'list' command to display all tasks."""
    tasks = task_service.get_all_tasks()
    print(format_task_list(tasks))


def handle_complete(task_id: int) -> None:
    """Handle the 'complete' command to toggle task completion.

    Args:
        task_id: The ID of the task to toggle.
    """
    try:
        task = task_service.toggle_completion(task_id)
        print(format_task_completed(task))
    except TaskNotFoundError as e:
        print(format_error(str(e)))
        sys.exit(1)


def handle_update(task_id: int, title: Optional[str] = None, description: Optional[str] = None) -> None:
    """Handle the 'update' command to modify task details.

    Args:
        task_id: The ID of the task to update.
        title: The new title (if provided).
        description: The new description (if provided).
    """
    if title is None and description is None:
        print(format_error("Provide at least --title or --description to update"))
        sys.exit(1)

    try:
        task = task_service.update_task(task_id, title=title, description=description)
        print(format_task_updated(task))
    except (TaskNotFoundError, ValidationError) as e:
        print(format_error(str(e)))
        sys.exit(1)


def handle_delete(task_id: int) -> None:
    """Handle the 'delete' command to remove a task.

    Args:
        task_id: The ID of the task to delete.
    """
    try:
        task = task_service.delete_task(task_id)
        print(format_task_deleted(task))
    except TaskNotFoundError as e:
        print(format_error(str(e)))
        sys.exit(1)


def handle_help() -> None:
    """Handle the 'help' command to display usage information."""
    help_text = """Todo Console App - Phase I

Usage: todo <command> [arguments]

Commands:
  add <title> [-d <description>]     Create a new task
  list                                Display all tasks
  complete <id>                       Toggle task completion status
  update <id> [-t <title>] [-d <desc>] Update task details
  delete <id>                         Delete a task
  help                                Show this help message

Examples:
  todo add "Buy groceries" -d "Milk, eggs, bread"
  todo list
  todo complete 1
  todo update 1 -t "New title"
  todo delete 1

For more information, see README.md
"""
    print(help_text)
