# Research & Technical Decisions: Todo Console App (Phase I)

**Date**: 2026-02-17
**Feature**: 001-todo-console-app
**Phase**: 0 (Research & Design Decisions)

## Overview

This document captures all technical research and design decisions made during the planning phase for the Phase I Todo Console App. All decisions align with the project constitution and hackathon requirements.

## Technical Decisions

### 1. CLI Framework Selection

**Decision**: Use Python's built-in `argparse` module

**Rationale**:
- Zero external dependencies (constitution requirement: use standard library)
- Sufficient for the 5 basic commands required
- Well-documented and stable
- Supports both command-line arguments and interactive mode
- Built-in help text generation

**Alternatives Considered**:
- **Click**: Popular and user-friendly, but adds external dependency
- **Typer**: Modern with type hints, but adds external dependency and complexity
- **Fire**: Minimal code, but less control over help text and validation

**Trade-offs**: argparse is more verbose than Click/Typer, but meets the "no external dependencies for core functionality" constraint.

---

### 2. Data Storage Pattern

**Decision**: In-memory dictionary with auto-incrementing integer keys

**Rationale**:
- Simple and fast for Phase I requirements
- Dictionary provides O(1) lookup by task ID
- Auto-incrementing counter ensures unique IDs
- Easy to iterate for list operations
- No persistence required (per Phase I spec)

**Implementation**:
```python
class TaskRepository:
    def __init__(self):
        self._tasks: dict[int, Task] = {}
        self._next_id: int = 1
```

**Alternatives Considered**:
- **List-based storage**: Simpler but O(n) lookup by ID
- **SQLite in-memory**: Overkill for Phase I, violates simplicity principle
- **Dataclass with slots**: Considered but dictionary is more flexible

**Trade-offs**: Dictionary uses slightly more memory than a list, but provides better performance for ID-based operations.

---

### 3. Task Entity Design

**Decision**: Use Python `dataclass` with validation

**Rationale**:
- Dataclasses provide clean syntax with type hints
- Built-in `__init__`, `__repr__`, `__eq__` methods
- Supports field validation via `__post_init__`
- Immutable fields (ID) via `field(init=False)`
- Aligns with Python Excellence principle

**Implementation**:
```python
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class Task:
    title: str
    description: str = ""
    completed: bool = False
    id: int = field(init=False, default=0)
    created_at: datetime = field(default_factory=datetime.now)
```

**Alternatives Considered**:
- **Plain class**: More verbose, no automatic methods
- **NamedTuple**: Immutable, but we need mutable completion status
- **Pydantic**: Excellent validation, but external dependency

**Trade-offs**: Dataclasses don't have built-in validation like Pydantic, so we'll add custom validation in `__post_init__`.

---

### 4. Testing Strategy

**Decision**: TDD with pytest, separate unit and integration tests

**Rationale**:
- pytest is the industry standard for Python testing
- Fixtures provide clean test setup/teardown
- Parametrized tests reduce code duplication
- Coverage plugin (pytest-cov) for 80% requirement
- Supports both unit and integration testing

**Test Structure**:
- **Unit tests**: Test models, repository, service in isolation
- **Integration tests**: Test CLI commands end-to-end
- **Fixtures**: Provide pre-populated repositories for tests

**Coverage Target**: 80% minimum (constitutional requirement)

**Alternatives Considered**:
- **unittest**: Built-in but more verbose, less features
- **nose2**: Less popular, smaller ecosystem

**Trade-offs**: pytest adds a dependency, but it's explicitly allowed for testing.

---

### 5. Error Handling Strategy

**Decision**: Custom exception hierarchy with user-friendly messages

**Rationale**:
- Clear error types for different failure modes
- User-friendly messages (not stack traces)
- Easy to test error conditions
- Supports graceful degradation

**Exception Hierarchy**:
```python
class TodoError(Exception):
    """Base exception for todo app"""
    pass

class TaskNotFoundError(TodoError):
    """Raised when task ID doesn't exist"""
    pass

class ValidationError(TodoError):
    """Raised when input validation fails"""
    pass
```

**Error Display**: CLI layer catches exceptions and displays user-friendly messages without stack traces.

---

### 6. CLI Interface Design

**Decision**: Subcommand-based interface with argparse

**Rationale**:
- Intuitive command structure: `todo add "title"`, `todo list`, etc.
- Each operation is a subcommand
- Built-in help for each command
- Supports optional arguments (e.g., `--description`)

**Command Structure**:
```bash
todo add "Buy groceries" --description "Milk, eggs, bread"
todo list
todo complete 1
todo update 1 --title "New title" --description "New desc"
todo delete 1
todo help
```

**Alternatives Considered**:
- **Interactive REPL**: More complex, not required for Phase I
- **Single command with flags**: Less intuitive (e.g., `todo --add --title "..."`)

**Trade-offs**: Subcommands require more argparse setup, but provide better UX.

---

### 7. Output Formatting

**Decision**: Simple text-based table format with status indicators

**Rationale**:
- Clear visual distinction between complete/incomplete tasks
- Works in any terminal
- No external dependencies (no rich/tabulate)
- Easy to test output

**Format Example**:
```
ID | Status | Title              | Description
---+--------+--------------------+------------------
1  | [ ]    | Buy groceries      | Milk, eggs, bread
2  | [✓]    | Call mom           |
3  | [ ]    | Finish homework    | Math and science
```

**Alternatives Considered**:
- **Rich library**: Beautiful output, but external dependency
- **JSON output**: Machine-readable, but not user-friendly
- **Tabulate**: Nice tables, but external dependency

**Trade-offs**: Manual formatting is more code, but maintains zero external dependencies.

---

### 8. Type Checking Strategy

**Decision**: Use mypy for static type checking

**Rationale**:
- Enforces type hints (constitutional requirement)
- Catches type errors before runtime
- Integrates with CI/CD pipelines
- Industry standard for Python type checking

**Configuration**: Strict mode enabled in `pyproject.toml`

---

### 9. Code Quality Tools

**Decision**: Use ruff for linting and formatting

**Rationale**:
- Fast (written in Rust)
- Combines multiple tools (flake8, black, isort, etc.)
- Single configuration file
- Constitutional requirement

**Configuration**: PEP 8 compliance with line length 100

---

### 10. Project Setup

**Decision**: Use UV for package management

**Rationale**:
- Hackathon requirement (specified in Phase I spec)
- Fast dependency resolution
- Modern Python packaging
- Replaces pip, poetry, virtualenv

**Setup**:
```bash
uv init todo-console-app
uv add --dev pytest pytest-cov ruff mypy
```

---

## Architecture Decisions

### Layered Architecture

**Layers**:
1. **Models Layer** (`src/models/`): Data structures and validation
2. **Services Layer** (`src/services/`): Business logic and storage
3. **CLI Layer** (`src/cli/`): User interface and command handling

**Benefits**:
- Clear separation of concerns
- Easy to test each layer independently
- Prepares for Phase II (web API can reuse service layer)
- Follows Clean Architecture principle (constitutional requirement)

**Dependencies**: CLI → Services → Models (unidirectional)

---

## Performance Considerations

### Expected Performance

- **Add Task**: O(1) - dictionary insert
- **Get Task**: O(1) - dictionary lookup
- **List Tasks**: O(n) - iterate all tasks
- **Update Task**: O(1) - dictionary lookup + update
- **Delete Task**: O(1) - dictionary delete

### Memory Usage

- **Per Task**: ~200 bytes (dataclass overhead + strings)
- **1000 Tasks**: ~200 KB (well within constraints)

---

## Testing Approach

### Test Coverage Strategy

1. **Unit Tests** (60% of test code):
   - Task model validation
   - Repository CRUD operations
   - Service business logic
   - Error handling

2. **Integration Tests** (40% of test code):
   - CLI command execution
   - End-to-end workflows
   - Error message display

### Test Data Strategy

- Use pytest fixtures for common test data
- Parametrized tests for edge cases
- Mock time-dependent operations (created_at timestamps)

---

## Risk Mitigation

### Identified Risks

1. **Risk**: Type hints may be verbose for simple operations
   - **Mitigation**: Use type aliases for complex types

2. **Risk**: Manual output formatting may be error-prone
   - **Mitigation**: Comprehensive integration tests for display

3. **Risk**: argparse setup may be verbose
   - **Mitigation**: Extract command setup to separate functions

---

## Future Considerations (Phase II/III)

### Extensibility Points

1. **Storage Layer**: Repository pattern allows easy swap to database
2. **Service Layer**: Can be reused by web API in Phase II
3. **Task Model**: Can be extended with priorities, tags, due dates
4. **CLI Commands**: Can be wrapped by AI chatbot in Phase III

### Migration Path

- Phase II: Add FastAPI layer, keep service layer unchanged
- Phase III: Add MCP server, expose service operations as tools

---

## Summary

All technical decisions align with:
- ✅ Constitutional principles (simplicity, clean architecture, Python excellence)
- ✅ Hackathon requirements (UV, pytest, TDD, no external dependencies for core)
- ✅ Phase I scope (5 basic features, in-memory storage, CLI only)

**Next Steps**: Proceed to Phase 1 (data-model.md, contracts/, quickstart.md)
