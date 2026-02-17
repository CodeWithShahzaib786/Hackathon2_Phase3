"""Main entry point for the todo console application."""

import argparse
import sys
from typing import Optional

from src.cli.commands import (
    handle_add,
    handle_list,
    handle_complete,
    handle_update,
    handle_delete,
    handle_help,
)


def create_parser() -> argparse.ArgumentParser:
    """Create and configure the argument parser.

    Returns:
        Configured ArgumentParser instance.
    """
    parser = argparse.ArgumentParser(
        prog="todo",
        description="Todo Console App - Phase I",
        add_help=False,
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Add command
    add_parser = subparsers.add_parser("add", help="Create a new task")
    add_parser.add_argument("title", type=str, help="Task title")
    add_parser.add_argument(
        "-d", "--description", type=str, default="", help="Task description (optional)"
    )

    # List command
    subparsers.add_parser("list", help="Display all tasks")

    # Complete command
    complete_parser = subparsers.add_parser("complete", help="Toggle task completion status")
    complete_parser.add_argument("id", type=int, help="Task ID")

    # Update command
    update_parser = subparsers.add_parser("update", help="Update task details")
    update_parser.add_argument("id", type=int, help="Task ID")
    update_parser.add_argument("-t", "--title", type=str, help="New task title")
    update_parser.add_argument("-d", "--description", type=str, help="New task description")

    # Delete command
    delete_parser = subparsers.add_parser("delete", help="Delete a task")
    delete_parser.add_argument("id", type=int, help="Task ID")

    # Help command
    subparsers.add_parser("help", help="Show help message")

    return parser


def main() -> None:
    """Main entry point for the application."""
    parser = create_parser()

    # Handle no arguments or --help
    if len(sys.argv) == 1 or (len(sys.argv) == 2 and sys.argv[1] in ["-h", "--help"]):
        handle_help()
        return

    args = parser.parse_args()

    # Route to appropriate command handler
    if args.command == "add":
        handle_add(args.title, args.description)
    elif args.command == "list":
        handle_list()
    elif args.command == "complete":
        handle_complete(args.id)
    elif args.command == "update":
        handle_update(args.id, title=args.title, description=args.description)
    elif args.command == "delete":
        handle_delete(args.id)
    elif args.command == "help":
        handle_help()
    else:
        handle_help()


if __name__ == "__main__":
    main()
