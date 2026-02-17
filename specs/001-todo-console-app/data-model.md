# Data Model: Todo Console App (Phase I)

**Date**: 2026-02-17
**Feature**: 001-todo-console-app
**Phase**: 1 (Data Model Design)

## Overview

This document defines the data structures and validation rules for the Phase I Todo Console App. The model is designed to be simple, type-safe, and extensible for future phases.

---

## Entities

### Task

**Purpose**: Represents a single todo item with title, description, completion status, and metadata.

**Attributes**:

| Attribute | Type | Required | Default | Constraints | Description |
|-----------|------|----------|---------|-------------|-------------|
| `id` | `int` | Yes (auto) | Auto-increment | Unique, immutable, > 0 | Unique identifier assigned by repository |
| `title` | `str` | Yes | - | 1-200 characters, non-empty | Short description of the task |
| `description` | `str` | No | `""` | Max 1000 characters | Detailed information about the task |
| `completed` | `bool` | No | `False` | - | Whether the task is done |
| `created_at` | `datetime` | Yes (auto) | `datetime.now()` | - | Timestamp when task was created |

**Validation Rules**:

1. **Title Validation**:
   - MUST NOT be empty or whitespace-only
   - MUST be between 1 and 200 characters (after stripping whitespace)
   - Leading/trailing whitespace is automatically stripped
   - Error: `ValidationError("Title is required and must be 1-200 characters")`

2. **Description Validation**:
   - MAY be empty (optional field)
   - MUST NOT exceed 1000 characters
   - Leading/trailing whitespace is automatically stripped
   - Error: `ValidationError("Description must not exceed 1000 characters")`

3. **ID Validation**:
   - Assigned by repository, not user-provided
   - MUST be unique across all tasks in a session
   - MUST be positive integer
   - Immutable after creation

4. **Completed Validation**:
   - MUST be boolean (True/False)
   - Defaults to False for new tasks

**State Transitions**:

```
[Created] ---> [Incomplete] <---> [Complete]
                    |
                    v
                [Deleted]
```

- **Created → Incomplete**: Task is created with `completed=False`
- **Incomplete ↔ Complete**: User can toggle completion status
- **Any State → Deleted**: Task can be deleted from any state

**Invariants**:

1. Task ID never changes after creation
2. Task created_at never changes after creation
3. Task title is never empty
4. Task description never exceeds 1000 characters

---

## Data Structures

### TaskRepository (In-Memory Storage)

**Purpose**: Manages the collection of tasks in memory using a dictionary.

**Internal Structure**:

```python
{
    "tasks": {
        1: Task(id=1, title="Buy groceries", ...),
        2: Task(id=2, title="Call mom", ...),
        3: Task(id=3, title="Finish homework", ...)
    },
    "next_id": 4
}
```

**Operations**:

| Operation | Time Complexity | Description |
|-----------|----------------|-------------|
| `add(task)` | O(1) | Add new task, assign ID |
| `get(id)` | O(1) | Retrieve task by ID |
| `get_all()` | O(n) | Retrieve all tasks |
| `update(id, updates)` | O(1) | Update task fields |
| `delete(id)` | O(1) | Remove task |
| `exists(id)` | O(1) | Check if task exists |

**Constraints**:

- Maximum 1000 tasks per session (soft limit, not enforced)
- All data lost when application exits (no persistence)
- Single-threaded access (no concurrency control needed)

---

## Type Definitions

### Python Type Hints

```python
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

@dataclass
class Task:
    """Represents a todo task with validation."""

    title: str
    description: str = ""
    completed: bool = False
    id: int = field(init=False, default=0)
    created_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self) -> None:
        """Validate task fields after initialization."""
        self._validate_title()
        self._validate_description()

    def _validate_title(self) -> None:
        """Validate title field."""
        self.title = self.title.strip()
        if not self.title or len(self.title) > 200:
            raise ValidationError(
                "Title is required and must be 1-200 characters"
            )

    def _validate_description(self) -> None:
        """Validate description field."""
        self.description = self.description.strip()
        if len(self.description) > 1000:
            raise ValidationError(
                "Description must not exceed 1000 characters"
            )

    def toggle_completion(self) -> None:
        """Toggle the completion status of the task."""
        self.completed = not self.completed

    def update_title(self, new_title: str) -> None:
        """Update task title with validation."""
        old_title = self.title
        self.title = new_title
        try:
            self._validate_title()
        except ValidationError:
            self.title = old_title
            raise

    def update_description(self, new_description: str) -> None:
        """Update task description with validation."""
        old_description = self.description
        self.description = new_description
        try:
            self._validate_description()
        except ValidationError:
            self.description = old_description
            raise
```

### Custom Exceptions

```python
class TodoError(Exception):
    """Base exception for todo application."""
    pass

class TaskNotFoundError(TodoError):
    """Raised when a task with the given ID does not exist."""

    def __init__(self, task_id: int):
        self.task_id = task_id
        super().__init__(f"Task with ID {task_id} not found")

class ValidationError(TodoError):
    """Raised when input validation fails."""
    pass
```

---

## Relationships

### Entity Relationship Diagram

```
┌─────────────────────────────────────┐
│            TaskRepository            │
│  (In-Memory Dictionary Storage)     │
│                                      │
│  - tasks: dict[int, Task]           │
│  - next_id: int                     │
│                                      │
│  + add(task: Task) -> Task          │
│  + get(id: int) -> Task             │
│  + get_all() -> list[Task]          │
│  + update(id: int, **kwargs) -> Task│
│  + delete(id: int) -> None          │
│  + exists(id: int) -> bool          │
└──────────────┬──────────────────────┘
               │ manages
               │ 1:N
               ▼
┌─────────────────────────────────────┐
│              Task                    │
│  (Dataclass with Validation)        │
│                                      │
│  - id: int                          │
│  - title: str                       │
│  - description: str                 │
│  - completed: bool                  │
│  - created_at: datetime             │
│                                      │
│  + toggle_completion() -> None      │
│  + update_title(str) -> None        │
│  + update_description(str) -> None  │
└─────────────────────────────────────┘
```

**Relationship**: TaskRepository has a one-to-many relationship with Task entities. Each Task is uniquely identified by its ID within the repository.

---

## Data Flow

### Task Creation Flow

```
User Input (title, description)
    ↓
Validation (Task.__post_init__)
    ↓
Task Object Created
    ↓
Repository.add(task)
    ↓
ID Assignment (next_id++)
    ↓
Store in Dictionary
    ↓
Return Task with ID
```

### Task Update Flow

```
User Input (id, new_title?, new_description?)
    ↓
Repository.get(id)
    ↓
Task.update_title() or Task.update_description()
    ↓
Validation
    ↓
Update Task Object
    ↓
Return Updated Task
```

### Task Completion Toggle Flow

```
User Input (id)
    ↓
Repository.get(id)
    ↓
Task.toggle_completion()
    ↓
Update completed field
    ↓
Return Updated Task
```

---

## Validation Examples

### Valid Task Creation

```python
# Valid: Normal task
task = Task(title="Buy groceries", description="Milk, eggs, bread")
# ✓ title: 14 characters
# ✓ description: 18 characters

# Valid: Minimal task
task = Task(title="Call mom")
# ✓ title: 8 characters
# ✓ description: "" (default)

# Valid: Maximum length title
task = Task(title="A" * 200)
# ✓ title: exactly 200 characters

# Valid: Long description
task = Task(title="Research", description="X" * 1000)
# ✓ description: exactly 1000 characters
```

### Invalid Task Creation

```python
# Invalid: Empty title
task = Task(title="")
# ✗ ValidationError: "Title is required and must be 1-200 characters"

# Invalid: Whitespace-only title
task = Task(title="   ")
# ✗ ValidationError: "Title is required and must be 1-200 characters"

# Invalid: Title too long
task = Task(title="A" * 201)
# ✗ ValidationError: "Title is required and must be 1-200 characters"

# Invalid: Description too long
task = Task(title="Valid", description="X" * 1001)
# ✗ ValidationError: "Description must not exceed 1000 characters"
```

---

## Edge Cases

### Whitespace Handling

- Leading/trailing whitespace is automatically stripped from title and description
- Internal whitespace is preserved
- Empty string after stripping is invalid for title

**Examples**:
```python
Task(title="  Buy groceries  ")  # Stored as "Buy groceries"
Task(title="Buy  groceries")     # Stored as "Buy  groceries" (internal spaces preserved)
Task(title="   ")                 # ValidationError (empty after strip)
```

### Special Characters

- All Unicode characters are allowed in title and description
- Newlines, tabs, and other control characters are preserved
- No escaping or sanitization is performed (CLI layer handles display)

**Examples**:
```python
Task(title="Buy 🛒 groceries")           # ✓ Unicode emoji
Task(title="Task #1: Review PR")         # ✓ Special characters
Task(title="Multi\nline\ntitle")         # ✓ Newlines (though unusual)
Task(description="Line 1\nLine 2\nLine 3")  # ✓ Multiline description
```

### ID Assignment

- IDs start at 1 and increment sequentially
- Deleted task IDs are not reused within a session
- ID counter never resets during application lifetime

**Example**:
```python
repo.add(Task(title="Task 1"))  # ID: 1
repo.add(Task(title="Task 2"))  # ID: 2
repo.delete(1)                   # Delete task 1
repo.add(Task(title="Task 3"))  # ID: 3 (not 1)
```

---

## Future Extensions (Phase II/III)

### Planned Additions

1. **User Association**: Add `user_id` field for multi-user support
2. **Priorities**: Add `priority` field (high/medium/low)
3. **Tags**: Add `tags` field (list of strings)
4. **Due Dates**: Add `due_date` field (datetime)
5. **Timestamps**: Add `updated_at` field (datetime)

### Migration Strategy

- Current model is forward-compatible
- New fields can be added with defaults
- Existing code will continue to work

---

## Summary

The data model is designed to be:
- ✅ **Simple**: Single entity (Task) with clear validation
- ✅ **Type-Safe**: Full type hints for all fields and methods
- ✅ **Validated**: Automatic validation on creation and updates
- ✅ **Extensible**: Easy to add fields for future phases
- ✅ **Testable**: Clear validation rules and error messages

**Next Steps**: Define CLI command contracts in `contracts/` directory
