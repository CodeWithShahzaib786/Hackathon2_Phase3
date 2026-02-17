---
description: "Implementation tasks for Todo Console App (Phase I)"
---

# Tasks: Todo Console App (Phase I)

**Input**: Design documents from `/specs/001-todo-console-app/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/cli-commands.md

**Tests**: TDD approach is mandatory per constitution. All test tasks must be completed BEFORE implementation tasks.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `- [ ] [ID] [P?] [Story?] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- All paths are relative to project root: `todo-console-app/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Initialize Python 3.13 project with UV package manager (create pyproject.toml, .python-version)
- [ ] T002 Create project directory structure: src/{models,services,cli}, tests/{unit,integration}
- [ ] T003 [P] Install development dependencies: pytest, pytest-cov, ruff, mypy via UV
- [ ] T004 [P] Configure ruff in pyproject.toml (line-length=100, target-version=py313)
- [ ] T005 [P] Configure mypy in pyproject.toml (strict mode, python_version=3.13)
- [ ] T006 [P] Configure pytest in pyproject.toml (testpaths, coverage settings, fail_under=80)
- [ ] T007 Create __init__.py files in all src/ and tests/ directories
- [ ] T008 Create tests/conftest.py with pytest configuration

**Checkpoint**: Project structure ready, tools configured

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T009 Create custom exception classes in src/models/exceptions.py (TodoError, TaskNotFoundError, ValidationError)
- [ ] T010 [P] Write unit tests for Task model validation in tests/unit/test_task_model.py (RED phase)
- [ ] T011 Create Task dataclass in src/models/task.py with validation (__post_init__, _validate_title, _validate_description)
- [ ] T012 Run tests for Task model - verify they pass (GREEN phase)
- [ ] T013 [P] Write unit tests for TaskRepository in tests/unit/test_task_repository.py (RED phase)
- [ ] T014 Create TaskRepository class in src/services/task_repository.py (in-memory dict storage, add/get/get_all/update/delete/exists methods)
- [ ] T015 Run tests for TaskRepository - verify they pass (GREEN phase)

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Create and View Tasks (Priority: P1) 🎯 MVP

**Goal**: Users can add new tasks with titles and descriptions, and view all tasks in a list

**Independent Test**: Add multiple tasks and view the list. Delivers immediate value by allowing users to capture and review their todos.

**Acceptance Criteria**:
- ✓ Add task with title and description → task created with unique ID
- ✓ View task list → all tasks displayed with IDs, titles, completion status
- ✓ Empty list → "No tasks found" message
- ✓ Empty title → validation error

### Tests for User Story 1 (TDD - Write FIRST)

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T016 [P] [US1] Write unit tests for TaskService.create_task in tests/unit/test_task_service.py (RED phase)
- [ ] T017 [P] [US1] Write unit tests for TaskService.get_all_tasks in tests/unit/test_task_service.py (RED phase)
- [ ] T018 [P] [US1] Write integration tests for 'add' command in tests/integration/test_cli_commands.py (RED phase)
- [ ] T019 [P] [US1] Write integration tests for 'list' command in tests/integration/test_cli_commands.py (RED phase)

### Implementation for User Story 1

- [ ] T020 [US1] Create TaskService class in src/services/task_service.py with create_task method
- [ ] T021 [US1] Add get_all_tasks method to TaskService in src/services/task_service.py
- [ ] T022 [US1] Run unit tests for TaskService - verify they pass (GREEN phase)
- [ ] T023 [US1] Create CLI argument parser setup in src/main.py with argparse
- [ ] T024 [US1] Implement 'add' command handler in src/cli/commands.py (calls TaskService.create_task)
- [ ] T025 [US1] Implement 'list' command handler in src/cli/commands.py (calls TaskService.get_all_tasks)
- [ ] T026 [US1] Create output formatter in src/cli/formatter.py (format_task_list, format_task_created)
- [ ] T027 [US1] Wire up 'add' and 'list' commands in src/main.py main() function
- [ ] T028 [US1] Run integration tests for US1 - verify they pass (GREEN phase)
- [ ] T029 [US1] Add error handling for validation errors in CLI commands
- [ ] T030 [US1] Run full test suite and verify 80% coverage for US1 code

**Checkpoint**: MVP complete - users can create and view tasks. This is a fully functional, independently testable increment.

---

## Phase 4: User Story 2 - Mark Tasks Complete (Priority: P2)

**Goal**: Users can mark tasks as complete or incomplete to track progress

**Independent Test**: Create tasks and toggle their completion status. Delivers value by enabling progress tracking.

**Acceptance Criteria**:
- ✓ Mark incomplete task as complete → status changes, confirmation displayed
- ✓ Mark complete task as complete → toggles to incomplete
- ✓ Invalid task ID → "Task not found" error
- ✓ List view → completed tasks visually distinguished (checkmarks)

### Tests for User Story 2 (TDD - Write FIRST)

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T031 [P] [US2] Write unit tests for Task.toggle_completion in tests/unit/test_task_model.py (RED phase)
- [ ] T032 [P] [US2] Write unit tests for TaskService.toggle_completion in tests/unit/test_task_service.py (RED phase)
- [ ] T033 [P] [US2] Write integration tests for 'complete' command in tests/integration/test_cli_commands.py (RED phase)

### Implementation for User Story 2

- [ ] T034 [US2] Add toggle_completion method to Task model in src/models/task.py
- [ ] T035 [US2] Add toggle_completion method to TaskService in src/services/task_service.py
- [ ] T036 [US2] Run unit tests for US2 - verify they pass (GREEN phase)
- [ ] T037 [US2] Implement 'complete' command handler in src/cli/commands.py
- [ ] T038 [US2] Add format_task_completed to formatter in src/cli/formatter.py
- [ ] T039 [US2] Update format_task_list to show completion status ([ ] vs [✓]) in src/cli/formatter.py
- [ ] T040 [US2] Wire up 'complete' command in src/main.py
- [ ] T041 [US2] Run integration tests for US2 - verify they pass (GREEN phase)
- [ ] T042 [US2] Add error handling for TaskNotFoundError in 'complete' command
- [ ] T043 [US2] Run full test suite and verify 80% coverage maintained

**Checkpoint**: Status tracking complete - users can mark tasks as done. Independently testable with US1.

---

## Phase 5: User Story 3 - Update Task Details (Priority: P3)

**Goal**: Users can update task titles and descriptions to correct mistakes or add information

**Independent Test**: Create a task and modify its details. Delivers value by allowing task refinement without recreation.

**Acceptance Criteria**:
- ✓ Update title → task title changed, confirmation displayed
- ✓ Update description → task description changed
- ✓ Update both → both fields changed
- ✓ Invalid task ID → "Task not found" error
- ✓ Empty title → "Title cannot be empty" error

### Tests for User Story 3 (TDD - Write FIRST)

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T044 [P] [US3] Write unit tests for Task.update_title in tests/unit/test_task_model.py (RED phase)
- [ ] T045 [P] [US3] Write unit tests for Task.update_description in tests/unit/test_task_model.py (RED phase)
- [ ] T046 [P] [US3] Write unit tests for TaskService.update_task in tests/unit/test_task_service.py (RED phase)
- [ ] T047 [P] [US3] Write integration tests for 'update' command in tests/integration/test_cli_commands.py (RED phase)

### Implementation for User Story 3

- [ ] T048 [US3] Add update_title method to Task model in src/models/task.py
- [ ] T049 [US3] Add update_description method to Task model in src/models/task.py
- [ ] T050 [US3] Add update_task method to TaskService in src/services/task_service.py
- [ ] T051 [US3] Run unit tests for US3 - verify they pass (GREEN phase)
- [ ] T052 [US3] Implement 'update' command handler in src/cli/commands.py (supports --title and --description flags)
- [ ] T053 [US3] Add format_task_updated to formatter in src/cli/formatter.py
- [ ] T054 [US3] Wire up 'update' command in src/main.py
- [ ] T055 [US3] Run integration tests for US3 - verify they pass (GREEN phase)
- [ ] T056 [US3] Add validation for "at least one field required" in 'update' command
- [ ] T057 [US3] Add error handling for ValidationError and TaskNotFoundError
- [ ] T058 [US3] Run full test suite and verify 80% coverage maintained

**Checkpoint**: Task editing complete - users can modify task details. Independently testable with US1.

---

## Phase 6: User Story 4 - Delete Tasks (Priority: P3)

**Goal**: Users can delete tasks they no longer need to keep their list clean

**Independent Test**: Create and delete tasks. Delivers value by enabling list management.

**Acceptance Criteria**:
- ✓ Delete existing task → task removed, confirmation displayed
- ✓ Invalid task ID → "Task not found" error
- ✓ Delete from list of 5 → only 4 remain
- ✓ Delete last task → "No tasks found" message on list

### Tests for User Story 4 (TDD - Write FIRST)

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T059 [P] [US4] Write unit tests for TaskService.delete_task in tests/unit/test_task_service.py (RED phase)
- [ ] T060 [P] [US4] Write integration tests for 'delete' command in tests/integration/test_cli_commands.py (RED phase)

### Implementation for User Story 4

- [ ] T061 [US4] Add delete_task method to TaskService in src/services/task_service.py
- [ ] T062 [US4] Run unit tests for US4 - verify they pass (GREEN phase)
- [ ] T063 [US4] Implement 'delete' command handler in src/cli/commands.py
- [ ] T064 [US4] Add format_task_deleted to formatter in src/cli/formatter.py
- [ ] T065 [US4] Wire up 'delete' command in src/main.py
- [ ] T066 [US4] Run integration tests for US4 - verify they pass (GREEN phase)
- [ ] T067 [US4] Add error handling for TaskNotFoundError in 'delete' command
- [ ] T068 [US4] Run full test suite and verify 80% coverage maintained

**Checkpoint**: Task deletion complete - users can remove tasks. All 5 basic features now functional.

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Final touches, help command, comprehensive error handling, documentation

- [ ] T069 [P] Implement 'help' command handler in src/cli/commands.py (display all commands and usage)
- [ ] T070 [P] Add comprehensive docstrings to all public functions and classes (Google style)
- [ ] T071 [P] Add type hints validation - run mypy and fix any issues
- [ ] T072 [P] Add edge case tests for long titles (>200 chars) in tests/unit/test_task_model.py
- [ ] T073 [P] Add edge case tests for long descriptions (>1000 chars) in tests/unit/test_task_model.py
- [ ] T074 [P] Add edge case tests for special characters (unicode, newlines) in tests/integration/test_cli_commands.py
- [ ] T075 [P] Add edge case tests for invalid task IDs (non-numeric, negative) in tests/integration/test_cli_commands.py
- [ ] T076 [P] Create README.md with setup instructions, usage examples, and feature list
- [ ] T077 Run final test suite with coverage report - verify ≥80% coverage
- [ ] T078 Run ruff check and format - ensure PEP 8 compliance
- [ ] T079 Run mypy - ensure all type hints are correct
- [ ] T080 Manual testing: Execute all 5 commands and verify output matches contracts/cli-commands.md

**Checkpoint**: Phase I complete - all features implemented, tested, and polished

---

## Dependencies & Execution Strategy

### User Story Dependencies

```
Phase 1 (Setup) → Phase 2 (Foundation) → Phase 3 (US1 - MVP)
                                        ↓
                                        Phase 4 (US2) [can run in parallel with US3, US4]
                                        Phase 5 (US3) [can run in parallel with US2, US4]
                                        Phase 6 (US4) [can run in parallel with US2, US3]
                                        ↓
                                        Phase 7 (Polish)
```

**Critical Path**: Phase 1 → Phase 2 → Phase 3 (US1) → Phase 7

**Parallel Opportunities**:
- After Phase 2: US2, US3, US4 can be implemented in parallel (different commands, no shared code)
- Within each phase: Test tasks marked [P] can run in parallel
- Within each phase: Model tasks marked [P] can run in parallel

### Independent Testing Per Story

Each user story can be tested independently:

**US1 (MVP)**:
```bash
# Test independently
uv run python -m src.main add "Test task"
uv run python -m src.main list
# Expected: Task appears in list
```

**US2 (with US1)**:
```bash
# Requires US1 for task creation
uv run python -m src.main add "Test task"
uv run python -m src.main complete 1
uv run python -m src.main list
# Expected: Task shows as complete
```

**US3 (with US1)**:
```bash
# Requires US1 for task creation
uv run python -m src.main add "Test task"
uv run python -m src.main update 1 --title "Updated"
uv run python -m src.main list
# Expected: Task title changed
```

**US4 (with US1)**:
```bash
# Requires US1 for task creation
uv run python -m src.main add "Test task"
uv run python -m src.main delete 1
uv run python -m src.main list
# Expected: No tasks found
```

### Suggested MVP Scope

**Minimum Viable Product**: Phase 1 + Phase 2 + Phase 3 (US1 only)

This delivers:
- ✅ Add tasks with title and description
- ✅ View all tasks in a list
- ✅ Validation and error handling
- ✅ 80% test coverage
- ✅ Fully functional todo app (create and view)

**Incremental Delivery**:
1. **Week 1**: MVP (US1) - Can create and view tasks
2. **Week 2**: Add US2 (Mark Complete) - Can track progress
3. **Week 3**: Add US3 + US4 (Update + Delete) - Full CRUD operations
4. **Week 4**: Polish and submit

---

## Implementation Strategy

### TDD Workflow (Red-Green-Refactor)

For each user story:

1. **RED**: Write failing tests first (T016-T019 for US1)
   ```bash
   uv run pytest tests/unit/test_task_service.py::test_create_task
   # Expected: FAIL (function doesn't exist yet)
   ```

2. **GREEN**: Implement minimal code to pass tests (T020-T022 for US1)
   ```bash
   uv run pytest tests/unit/test_task_service.py::test_create_task
   # Expected: PASS
   ```

3. **REFACTOR**: Improve code while keeping tests green (T029-T030 for US1)
   ```bash
   uv run pytest  # All tests still pass
   uv run pytest --cov=src --cov-report=term-missing  # Check coverage
   ```

### Parallel Execution Examples

**Phase 2 (Foundation) - Parallel Tasks**:
```bash
# Terminal 1: Work on Task model tests
uv run pytest tests/unit/test_task_model.py

# Terminal 2: Work on TaskRepository tests (different file)
uv run pytest tests/unit/test_task_repository.py
```

**Phase 3 (US1) - Parallel Test Writing**:
```bash
# Terminal 1: Write TaskService tests
vim tests/unit/test_task_service.py

# Terminal 2: Write CLI integration tests (different file)
vim tests/integration/test_cli_commands.py
```

**After Phase 3 - Parallel User Stories**:
```bash
# Terminal 1: Implement US2 (Mark Complete)
# Work on T031-T043

# Terminal 2: Implement US3 (Update Tasks)
# Work on T044-T058

# Terminal 3: Implement US4 (Delete Tasks)
# Work on T059-T068
```

---

## Task Summary

**Total Tasks**: 80 tasks

**Tasks by Phase**:
- Phase 1 (Setup): 8 tasks
- Phase 2 (Foundation): 7 tasks
- Phase 3 (US1 - MVP): 15 tasks
- Phase 4 (US2): 13 tasks
- Phase 5 (US3): 15 tasks
- Phase 6 (US4): 10 tasks
- Phase 7 (Polish): 12 tasks

**Tasks by User Story**:
- US1 (Create/View): 15 tasks
- US2 (Mark Complete): 13 tasks
- US3 (Update): 15 tasks
- US4 (Delete): 10 tasks
- Infrastructure: 27 tasks

**Parallel Opportunities**: 35 tasks marked [P] can run in parallel

**Test Tasks**: 24 test tasks (30% of total) - TDD approach

**Coverage Target**: ≥80% code coverage (verified in T030, T043, T058, T068, T077)

---

## Format Validation

✅ All tasks follow checklist format: `- [ ] [ID] [P?] [Story?] Description with file path`
✅ All user story tasks have [Story] labels (US1, US2, US3, US4)
✅ All parallelizable tasks marked with [P]
✅ All tasks include specific file paths
✅ Sequential task IDs (T001-T080)

**Ready for**: `/sp.implement` - Execute implementation tasks via Claude Code
