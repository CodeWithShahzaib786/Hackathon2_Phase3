# CLI Command Contracts: Todo Console App (Phase I)

**Date**: 2026-02-17
**Feature**: 001-todo-console-app
**Phase**: 1 (Command Interface Contracts)

## Overview

This document defines the command-line interface contracts for all 5 basic operations. Each command specifies its syntax, arguments, outputs, and error conditions.

---

## Command: `add`

**Purpose**: Create a new task with title and optional description

**Syntax**:
```bash
todo add <title> [--description <text>]
todo add <title> [-d <text>]
```

**Arguments**:

| Argument | Type | Required | Constraints | Description |
|----------|------|----------|-------------|-------------|
| `title` | string | Yes | 1-200 chars, non-empty | Task title |
| `--description`, `-d` | string | No | Max 1000 chars | Task description |

**Success Output**:
```
✓ Task created successfully
  ID: 1
  Title: Buy groceries
  Description: Milk, eggs, bread
  Status: Incomplete
  Created: 2026-02-17 10:30:45
```

**Error Conditions**:

| Error | Exit Code | Output |
|-------|-----------|--------|
| Empty title | 1 | `Error: Title is required and must be 1-200 characters` |
| Title too long (>200) | 1 | `Error: Title is required and must be 1-200 characters` |
| Description too long (>1000) | 1 | `Error: Description must not exceed 1000 characters` |

**Examples**:
```bash
# Minimal task
todo add "Buy groceries"

# Task with description
todo add "Buy groceries" --description "Milk, eggs, bread"

# Short form
todo add "Call mom" -d "Discuss weekend plans"

# Error: empty title
todo add ""
# Output: Error: Title is required and must be 1-200 characters
```

---

## Command: `list`

**Purpose**: Display all tasks with their details

**Syntax**:
```bash
todo list
```

**Arguments**: None

**Success Output** (with tasks):
```
Your Tasks:

ID | Status | Title              | Description          | Created
---+--------+--------------------+----------------------+-------------------
1  | [ ]    | Buy groceries      | Milk, eggs, bread    | 2026-02-17 10:30
2  | [✓]    | Call mom           |                      | 2026-02-17 09:15
3  | [ ]    | Finish homework    | Math and science     | 2026-02-17 11:00

Total: 3 tasks (1 completed, 2 incomplete)
```

**Success Output** (no tasks):
```
No tasks found.

Use 'todo add <title>' to create your first task.
```

**Error Conditions**: None (always succeeds)

**Display Rules**:
- Tasks ordered by ID (ascending)
- Status: `[✓]` for completed, `[ ]` for incomplete
- Description truncated to 20 chars if longer (with `...`)
- Created timestamp in `YYYY-MM-DD HH:MM` format
- Summary line shows total, completed, and incomplete counts

**Examples**:
```bash
# List all tasks
todo list

# Empty list
todo list
# Output: No tasks found.
```

---

## Command: `complete`

**Purpose**: Toggle task completion status (incomplete ↔ complete)

**Syntax**:
```bash
todo complete <task_id>
```

**Arguments**:

| Argument | Type | Required | Constraints | Description |
|----------|------|----------|-------------|-------------|
| `task_id` | integer | Yes | Must exist | ID of task to toggle |

**Success Output** (marking complete):
```
✓ Task marked as complete
  ID: 1
  Title: Buy groceries
  Status: Complete
```

**Success Output** (marking incomplete):
```
✓ Task marked as incomplete
  ID: 1
  Title: Buy groceries
  Status: Incomplete
```

**Error Conditions**:

| Error | Exit Code | Output |
|-------|-----------|--------|
| Task not found | 1 | `Error: Task with ID {id} not found` |
| Invalid ID (non-numeric) | 1 | `Error: Task ID must be a number` |
| Invalid ID (negative/zero) | 1 | `Error: Task ID must be a positive number` |

**Examples**:
```bash
# Mark task 1 as complete
todo complete 1

# Toggle back to incomplete
todo complete 1

# Error: task not found
todo complete 999
# Output: Error: Task with ID 999 not found

# Error: invalid ID
todo complete abc
# Output: Error: Task ID must be a number
```

---

## Command: `update`

**Purpose**: Modify task title and/or description

**Syntax**:
```bash
todo update <task_id> [--title <text>] [--description <text>]
todo update <task_id> [-t <text>] [-d <text>]
```

**Arguments**:

| Argument | Type | Required | Constraints | Description |
|----------|------|----------|-------------|-------------|
| `task_id` | integer | Yes | Must exist | ID of task to update |
| `--title`, `-t` | string | No | 1-200 chars | New task title |
| `--description`, `-d` | string | No | Max 1000 chars | New task description |

**Constraints**:
- At least one of `--title` or `--description` must be provided
- If only `--title` provided, description unchanged
- If only `--description` provided, title unchanged

**Success Output**:
```
✓ Task updated successfully
  ID: 1
  Title: Buy groceries and fruits
  Description: Milk, eggs, bread, bananas, apples
  Status: Incomplete
```

**Error Conditions**:

| Error | Exit Code | Output |
|-------|-----------|--------|
| Task not found | 1 | `Error: Task with ID {id} not found` |
| No updates provided | 1 | `Error: Provide at least --title or --description to update` |
| Empty title | 1 | `Error: Title cannot be empty` |
| Title too long | 1 | `Error: Title is required and must be 1-200 characters` |
| Description too long | 1 | `Error: Description must not exceed 1000 characters` |
| Invalid ID | 1 | `Error: Task ID must be a number` |

**Examples**:
```bash
# Update title only
todo update 1 --title "Buy groceries and fruits"

# Update description only
todo update 1 --description "Milk, eggs, bread, bananas"

# Update both
todo update 1 -t "Buy groceries" -d "Updated list"

# Error: no updates
todo update 1
# Output: Error: Provide at least --title or --description to update

# Error: empty title
todo update 1 --title ""
# Output: Error: Title cannot be empty
```

---

## Command: `delete`

**Purpose**: Remove a task from the list

**Syntax**:
```bash
todo delete <task_id>
```

**Arguments**:

| Argument | Type | Required | Constraints | Description |
|----------|------|----------|-------------|-------------|
| `task_id` | integer | Yes | Must exist | ID of task to delete |

**Success Output**:
```
✓ Task deleted successfully
  ID: 1
  Title: Buy groceries
```

**Error Conditions**:

| Error | Exit Code | Output |
|-------|-----------|--------|
| Task not found | 1 | `Error: Task with ID {id} not found` |
| Invalid ID (non-numeric) | 1 | `Error: Task ID must be a number` |
| Invalid ID (negative/zero) | 1 | `Error: Task ID must be a positive number` |

**Examples**:
```bash
# Delete task 1
todo delete 1

# Error: task not found
todo delete 999
# Output: Error: Task with ID 999 not found

# Error: invalid ID
todo delete -5
# Output: Error: Task ID must be a positive number
```

---

## Command: `help`

**Purpose**: Display help information for all commands

**Syntax**:
```bash
todo help
todo --help
todo -h
```

**Arguments**: None

**Success Output**:
```
Todo Console App - Phase I

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
```

**Error Conditions**: None (always succeeds)

---

## Global Behavior

### Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | User error (invalid input, task not found, validation failure) |
| 2 | System error (unexpected exception) |

### Error Message Format

All error messages follow this format:
```
Error: <clear, actionable message>
```

No stack traces are displayed to users. Stack traces are logged for debugging but not shown in CLI output.

### Output Format

- **Success messages**: Start with `✓` (checkmark)
- **Error messages**: Start with `Error:`
- **Info messages**: Plain text
- **Tables**: ASCII table format with borders

### Color Support

Phase I uses plain text only (no colors). Color support may be added in future phases if time permits.

---

## Command Parsing

### Argument Parsing Rules

1. **Positional arguments**: Must come before optional arguments
2. **Optional arguments**: Can be in any order after positional arguments
3. **Quoted strings**: Required for titles/descriptions with spaces
4. **Short vs long flags**: Both supported (`-d` and `--description`)

### Examples of Valid Syntax

```bash
todo add "Title with spaces"
todo add "Title" --description "Description with spaces"
todo add "Title" -d "Description"
todo update 1 --title "New" --description "New desc"
todo update 1 -t "New" -d "New desc"
todo update 1 -d "New desc" -t "New"  # Order doesn't matter
```

### Examples of Invalid Syntax

```bash
todo add Title with spaces  # Missing quotes
todo add --description "Desc" "Title"  # Wrong order
todo update --title "New" 1  # ID must come first
```

---

## Integration with Service Layer

### Command → Service Mapping

| Command | Service Method | Parameters |
|---------|---------------|------------|
| `add` | `task_service.create_task(title, description)` | title: str, description: str |
| `list` | `task_service.get_all_tasks()` | None |
| `complete` | `task_service.toggle_completion(task_id)` | task_id: int |
| `update` | `task_service.update_task(task_id, title?, description?)` | task_id: int, title: str \| None, description: str \| None |
| `delete` | `task_service.delete_task(task_id)` | task_id: int |

### Error Handling Flow

```
CLI Command
    ↓
Parse Arguments (argparse)
    ↓
Validate Input (basic checks)
    ↓
Call Service Method
    ↓
Service validates and executes
    ↓
[Success] → Format and display result
[Error] → Catch exception, format error message, exit with code 1
```

---

## Testing Contracts

### Unit Test Coverage

Each command must have tests for:
1. ✅ Success case with minimal input
2. ✅ Success case with all optional arguments
3. ✅ Error case: invalid input
4. ✅ Error case: task not found (where applicable)
5. ✅ Error case: validation failure

### Integration Test Coverage

Each command must have end-to-end tests:
1. ✅ Execute command via CLI
2. ✅ Verify output format
3. ✅ Verify exit code
4. ✅ Verify state changes (for add/update/delete/complete)

---

## Summary

All CLI commands follow consistent patterns:
- ✅ Clear, predictable syntax
- ✅ Helpful error messages
- ✅ Consistent output formatting
- ✅ Proper exit codes
- ✅ Comprehensive validation

**Next Steps**: Create quickstart.md with setup and usage instructions
