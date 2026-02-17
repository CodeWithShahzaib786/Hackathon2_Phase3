# Tasks: Todo Full-Stack Web Application (Phase II)

**Input**: Design documents from `/specs/002-fullstack-web-app/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

**Tests**: TDD approach required - tests written FIRST before implementation

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app monorepo**: `backend/src/`, `frontend/src/`
- Backend tests: `backend/tests/`
- Frontend tests: `frontend/tests/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create monorepo directory structure (frontend/ and backend/ at repository root)
- [X] T002 Initialize backend Python project with UV in backend/pyproject.toml
- [X] T003 Initialize frontend Next.js project with TypeScript in frontend/package.json
- [X] T004 [P] Configure backend linting and formatting (ruff) in backend/pyproject.toml
- [X] T005 [P] Configure frontend linting (ESLint) and formatting (Prettier) in frontend/.eslintrc.json
- [X] T006 [P] Create environment variables template in .env.example
- [X] T007 [P] Configure Tailwind CSS in frontend/tailwind.config.ts
- [X] T008 [P] Setup Git ignore files for both frontend and backend

**Checkpoint**: Project structure ready for development

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

### Database & ORM Setup

- [X] T009 Configure Neon PostgreSQL connection in backend/src/core/database.py
- [X] T010 Setup Alembic for database migrations in backend/alembic/
- [X] T011 Create initial database migration for users and tasks tables in backend/alembic/versions/

### Authentication Infrastructure

- [X] T012 Implement JWT utilities (sign, verify) in backend/src/core/security.py
- [X] T013 Implement password hashing utilities (bcrypt) in backend/src/core/security.py
- [X] T014 Create authentication dependency (get_current_user) in backend/src/api/deps.py
- [X] T015 Configure Better Auth in frontend/src/lib/auth.ts

### API Infrastructure

- [X] T016 Create FastAPI application with CORS middleware in backend/src/main.py
- [X] T017 Setup API router structure in backend/src/api/__init__.py
- [X] T018 Create base Pydantic schemas for requests/responses in backend/src/models/__init__.py

### Frontend Infrastructure

- [X] T019 Create API client with JWT token handling in frontend/src/lib/api.ts
- [X] T020 Setup Next.js App Router layout in frontend/src/app/layout.tsx
- [X] T021 [P] Create reusable UI components (Button, Input, Modal) in frontend/src/components/ui/

### Configuration & Environment

- [X] T022 Create settings/config management in backend/src/core/config.py
- [X] T023 Setup environment variable validation in backend/src/core/config.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - User Authentication and Account Management (Priority: P1) 🎯 BLOCKING

**Goal**: Enable users to create accounts, sign in securely, and manage their sessions

**Independent Test**: Create account, sign out, sign back in, verify session persistence

**⚠️ CRITICAL**: This story BLOCKS all other stories - authentication is required for task management

### Tests for User Story 1 (TDD - Write FIRST)

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [X] T024 [P] [US1] Unit test for User model validation in backend/tests/unit/test_user_model.py
- [X] T025 [P] [US1] Unit test for password hashing in backend/tests/unit/test_security.py
- [X] T026 [P] [US1] Unit test for JWT token generation/verification in backend/tests/unit/test_security.py
- [X] T027 [P] [US1] Integration test for signup endpoint in backend/tests/integration/test_auth_api.py
- [X] T028 [P] [US1] Integration test for signin endpoint in backend/tests/integration/test_auth_api.py
- [X] T029 [P] [US1] Integration test for signout endpoint in backend/tests/integration/test_auth_api.py
- [X] T030 [P] [US1] Integration test for JWT authentication middleware in backend/tests/integration/test_auth_api.py

### Backend Implementation for User Story 1

- [X] T031 [US1] Create User SQLModel in backend/src/models/user.py
- [X] T032 [US1] Implement AuthService (signup, signin, verify) in backend/src/services/auth_service.py
- [X] T033 [US1] Implement POST /api/auth/signup endpoint in backend/src/api/auth.py
- [X] T034 [US1] Implement POST /api/auth/signin endpoint in backend/src/api/auth.py
- [X] T035 [US1] Implement POST /api/auth/signout endpoint in backend/src/api/auth.py
- [X] T036 [US1] Add email validation and password strength checks in backend/src/services/auth_service.py
- [X] T037 [US1] Add error handling for duplicate emails and invalid credentials in backend/src/api/auth.py

### Frontend Implementation for User Story 1

- [X] T038 [P] [US1] Create SignUpForm component in frontend/src/components/auth/SignUpForm.tsx
- [X] T039 [P] [US1] Create SignInForm component in frontend/src/components/auth/SignInForm.tsx
- [X] T040 [US1] Create signup page in frontend/src/app/(auth)/signup/page.tsx
- [X] T041 [US1] Create signin page in frontend/src/app/(auth)/signin/page.tsx
- [X] T042 [US1] Implement authentication state management in frontend/src/lib/auth.ts
- [X] T043 [US1] Add form validation and error display in auth forms
- [X] T044 [US1] Implement protected route middleware in frontend/src/middleware.ts

### Frontend Tests for User Story 1

- [X] T045 [P] [US1] Component test for SignUpForm in frontend/tests/components/SignUpForm.test.tsx
- [X] T046 [P] [US1] Component test for SignInForm in frontend/tests/components/SignInForm.test.tsx

**Checkpoint**: Authentication complete - users can create accounts and sign in. Task management can now proceed.

---

## Phase 4: User Story 2 - Create and View Tasks via Web Interface (Priority: P2) 🎯 MVP

**Goal**: Enable authenticated users to create tasks and view their task list

**Independent Test**: Sign in, create multiple tasks, view task list, verify only own tasks visible

### Tests for User Story 2 (TDD - Write FIRST)

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [X] T047 [P] [US2] Unit test for Task model validation in backend/tests/unit/test_task_model.py
- [X] T048 [P] [US2] Unit test for TaskService.create_task in backend/tests/unit/test_task_service.py
- [X] T049 [P] [US2] Unit test for TaskService.get_all_tasks in backend/tests/unit/test_task_service.py
- [X] T050 [P] [US2] Integration test for POST /api/{user_id}/tasks in backend/tests/integration/test_tasks_api.py
- [X] T051 [P] [US2] Integration test for GET /api/{user_id}/tasks in backend/tests/integration/test_tasks_api.py
- [X] T052 [P] [US2] Integration test for user isolation (cannot see other users' tasks) in backend/tests/integration/test_tasks_api.py

### Backend Implementation for User Story 2

- [X] T053 [US2] Create Task SQLModel in backend/src/models/task.py
- [X] T054 [US2] Implement TaskService (create, get_all) in backend/src/services/task_service.py
- [X] T055 [US2] Implement POST /api/{user_id}/tasks endpoint in backend/src/api/tasks.py
- [X] T056 [US2] Implement GET /api/{user_id}/tasks endpoint with status filtering in backend/src/api/tasks.py
- [X] T057 [US2] Add user_id verification middleware in backend/src/api/tasks.py
- [X] T058 [US2] Add title/description validation in backend/src/services/task_service.py

### Frontend Implementation for User Story 2

- [X] T059 [P] [US2] Create TaskList component in frontend/src/components/tasks/TaskList.tsx
- [X] T060 [P] [US2] Create TaskItem component in frontend/src/components/tasks/TaskItem.tsx
- [X] T061 [P] [US2] Create TaskForm component (for creating tasks) in frontend/src/components/tasks/TaskForm.tsx
- [X] T062 [US2] Create dashboard page in frontend/src/app/dashboard/page.tsx
- [X] T063 [US2] Implement task creation API calls in frontend/src/lib/api.ts
- [X] T064 [US2] Implement task list fetching API calls in frontend/src/lib/api.ts
- [X] T065 [US2] Add empty state UI for no tasks in frontend/src/components/tasks/TaskList.tsx
- [X] T066 [US2] Add loading states and error handling in dashboard page

### Frontend Tests for User Story 2

- [X] T067 [P] [US2] Component test for TaskList in frontend/tests/components/TaskList.test.tsx
- [X] T068 [P] [US2] Component test for TaskForm in frontend/tests/components/TaskForm.test.tsx

**Checkpoint**: MVP complete - users can create and view tasks. This is a fully functional todo app!

---

## Phase 5: User Story 3 - Mark Tasks Complete via Web Interface (Priority: P3)

**Goal**: Enable users to toggle task completion status

**Independent Test**: Sign in, create task, mark as complete, verify visual change, mark as incomplete

### Tests for User Story 3 (TDD - Write FIRST)

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [X] T069 [P] [US3] Unit test for TaskService.toggle_completion in backend/tests/unit/test_task_service.py
- [X] T070 [P] [US3] Integration test for PATCH /api/{user_id}/tasks/{id}/complete in backend/tests/integration/test_tasks_api.py

### Backend Implementation for User Story 3

- [X] T071 [US3] Implement TaskService.toggle_completion in backend/src/services/task_service.py
- [X] T072 [US3] Implement PATCH /api/{user_id}/tasks/{id}/complete endpoint in backend/src/api/tasks.py

### Frontend Implementation for User Story 3

- [X] T073 [US3] Add completion toggle UI to TaskItem component in frontend/src/components/tasks/TaskItem.tsx
- [X] T074 [US3] Implement toggle completion API call in frontend/src/lib/api.ts
- [X] T075 [US3] Add visual styling for completed tasks (strikethrough, checkmark) in frontend/src/components/tasks/TaskItem.tsx
- [X] T076 [US3] Add optimistic UI updates for completion toggle

### Frontend Tests for User Story 3

- [X] T077 [US3] Component test for completion toggle in frontend/tests/components/TaskItem.test.tsx

**Checkpoint**: Task completion tracking works - users can mark tasks as done

---

## Phase 6: User Story 4 - Update Task Details via Web Interface (Priority: P4)

**Goal**: Enable users to edit task titles and descriptions

**Independent Test**: Sign in, create task, edit title and description, verify changes persist

### Tests for User Story 4 (TDD - Write FIRST)

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [X] T078 [P] [US4] Unit test for TaskService.update_task in backend/tests/unit/test_task_service.py
- [X] T079 [P] [US4] Integration test for PUT /api/{user_id}/tasks/{id} in backend/tests/integration/test_tasks_api.py

### Backend Implementation for User Story 4

- [X] T080 [US4] Implement TaskService.update_task in backend/src/services/task_service.py
- [X] T081 [US4] Implement PUT /api/{user_id}/tasks/{id} endpoint in backend/src/api/tasks.py
- [X] T082 [US4] Add validation for empty title in update operation

### Frontend Implementation for User Story 4

- [X] T083 [US4] Create TaskEditForm component in frontend/src/components/tasks/TaskEditForm.tsx
- [X] T084 [US4] Add edit button and modal to TaskItem component in frontend/src/components/tasks/TaskItem.tsx
- [X] T085 [US4] Implement update task API call in frontend/src/lib/api.ts
- [X] T086 [US4] Add form validation for edit form

### Frontend Tests for User Story 4

- [X] T087 [US4] Component test for TaskEditForm in frontend/tests/components/TaskEditForm.test.tsx

**Checkpoint**: Task editing works - users can update task details

---

## Phase 7: User Story 5 - Delete Tasks via Web Interface (Priority: P4)

**Goal**: Enable users to delete tasks they no longer need

**Independent Test**: Sign in, create task, delete task, verify it's removed from list

### Tests for User Story 5 (TDD - Write FIRST)

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [X] T088 [P] [US5] Unit test for TaskService.delete_task in backend/tests/unit/test_task_service.py
- [X] T089 [P] [US5] Integration test for DELETE /api/{user_id}/tasks/{id} in backend/tests/integration/test_tasks_api.py

### Backend Implementation for User Story 5

- [X] T090 [US5] Implement TaskService.delete_task in backend/src/services/task_service.py
- [X] T091 [US5] Implement DELETE /api/{user_id}/tasks/{id} endpoint in backend/src/api/tasks.py

### Frontend Implementation for User Story 5

- [X] T092 [US5] Add delete button to TaskItem component in frontend/src/components/tasks/TaskItem.tsx
- [X] T093 [US5] Add confirmation dialog for delete action in frontend/src/components/tasks/TaskItem.tsx
- [X] T094 [US5] Implement delete task API call in frontend/src/lib/api.ts
- [X] T095 [US5] Add optimistic UI updates for task deletion

### Frontend Tests for User Story 5

- [X] T096 [US5] Component test for delete confirmation in frontend/tests/components/TaskItem.test.tsx

**Checkpoint**: All 5 Basic Level features complete - full CRUD functionality

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T097 [P] Add comprehensive API documentation in backend/src/main.py (OpenAPI/Swagger)
- [X] T098 [P] Create README.md with Phase II setup instructions
- [X] T099 [P] Add responsive design improvements for mobile devices
- [X] T100 [P] Add loading spinners and skeleton screens across frontend
- [X] T101 [P] Implement error boundaries in frontend/src/app/error.tsx
- [X] T102 [P] Add input sanitization for XSS prevention
- [X] T103 [P] Run security audit (check for SQL injection, XSS, CSRF)
- [X] T104 [P] Add rate limiting to authentication endpoints (optional)
- [X] T105 [P] Optimize database queries with proper indexing
- [X] T106 [P] Add frontend build optimization (code splitting, lazy loading)
- [X] T107 Run quickstart.md validation and update if needed
- [X] T108 Create deployment guide for Vercel (frontend) and Railway/Render (backend)
- [X] T109 Run full test suite and verify 80% coverage target
- [ ] T110 Create demo video (max 90 seconds) for hackathon submission

**Checkpoint**: All 5 Basic Level features complete with production-ready polish!

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Story 1 (Phase 3)**: Depends on Foundational - BLOCKS all other user stories (authentication required)
- **User Stories 2-5 (Phases 4-7)**: All depend on US1 completion (need authentication)
  - US2, US3, US4, US5 can proceed in parallel after US1 (if staffed)
  - Or sequentially in priority order (P2 → P3 → P4)
- **Polish (Phase 8)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: BLOCKING - Must complete before any other story
- **User Story 2 (P2)**: Depends on US1 (authentication) - Can start after US1 complete
- **User Story 3 (P3)**: Depends on US1 + US2 (need tasks to mark complete) - Can start after US2
- **User Story 4 (P4)**: Depends on US1 + US2 (need tasks to update) - Can start after US2
- **User Story 5 (P4)**: Depends on US1 + US2 (need tasks to delete) - Can start after US2

**Note**: US3, US4, US5 can run in parallel after US2 is complete

### Within Each User Story

- Tests MUST be written and FAIL before implementation
- Backend models before services
- Backend services before API endpoints
- Backend API before frontend integration
- Frontend components before pages
- Story complete before moving to next priority

### Parallel Opportunities

**Phase 1 (Setup)**: T004, T005, T006, T007, T008 can run in parallel

**Phase 2 (Foundational)**: T021 can run in parallel with other foundational tasks

**Phase 3 (US1 Tests)**: T024, T025, T026, T027, T028, T029, T030 can run in parallel

**Phase 3 (US1 Frontend)**: T038, T039 can run in parallel; T045, T046 can run in parallel

**Phase 4 (US2 Tests)**: T047, T048, T049, T050, T051, T052 can run in parallel

**Phase 4 (US2 Frontend)**: T059, T060, T061 can run in parallel; T067, T068 can run in parallel

**Phase 5-7**: Tests within each story can run in parallel

**Phase 8 (Polish)**: T097, T098, T099, T100, T101, T102, T103, T104, T105, T106 can run in parallel

**After US2 Complete**: US3, US4, US5 can be worked on in parallel by different team members

---

## Parallel Example: User Story 2

```bash
# Launch all tests for User Story 2 together:
Task: "Unit test for Task model validation in backend/tests/unit/test_task_model.py"
Task: "Unit test for TaskService.create_task in backend/tests/unit/test_task_service.py"
Task: "Unit test for TaskService.get_all_tasks in backend/tests/unit/test_task_service.py"
Task: "Integration test for POST /api/{user_id}/tasks in backend/tests/integration/test_tasks_api.py"
Task: "Integration test for GET /api/{user_id}/tasks in backend/tests/integration/test_tasks_api.py"
Task: "Integration test for user isolation in backend/tests/integration/test_tasks_api.py"

# Launch all frontend components for User Story 2 together:
Task: "Create TaskList component in frontend/src/components/tasks/TaskList.tsx"
Task: "Create TaskItem component in frontend/src/components/tasks/TaskItem.tsx"
Task: "Create TaskForm component in frontend/src/components/tasks/TaskForm.tsx"
```

---

## Implementation Strategy

### MVP First (User Stories 1 + 2 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1 (Authentication - BLOCKING)
4. Complete Phase 4: User Story 2 (Create and View Tasks)
5. **STOP and VALIDATE**: Test authentication and task creation independently
6. Deploy/demo if ready - **This is a fully functional MVP!**

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 (Auth) → Test independently → Deploy/Demo
3. Add User Story 2 (Create/View) → Test independently → Deploy/Demo (MVP!)
4. Add User Story 3 (Complete) → Test independently → Deploy/Demo
5. Add User Story 4 (Update) → Test independently → Deploy/Demo
6. Add User Story 5 (Delete) → Test independently → Deploy/Demo
7. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Team completes User Story 1 (Authentication) together - BLOCKING
3. Once US1 is done:
   - Developer A: User Story 2 (Create/View)
   - Wait for US2 to complete, then:
   - Developer A: User Story 3 (Complete)
   - Developer B: User Story 4 (Update)
   - Developer C: User Story 5 (Delete)
4. Stories complete and integrate independently

---

## Task Summary

**Total Tasks**: 110 tasks

**Tasks by Phase**:
- Phase 1 (Setup): 8 tasks
- Phase 2 (Foundational): 15 tasks
- Phase 3 (US1 - Authentication): 23 tasks (7 backend tests + 7 backend impl + 7 frontend impl + 2 frontend tests)
- Phase 4 (US2 - Create/View): 22 tasks (6 backend tests + 6 backend impl + 8 frontend impl + 2 frontend tests)
- Phase 5 (US3 - Complete): 9 tasks (2 backend tests + 2 backend impl + 4 frontend impl + 1 frontend test)
- Phase 6 (US4 - Update): 10 tasks (2 backend tests + 3 backend impl + 4 frontend impl + 1 frontend test)
- Phase 7 (US5 - Delete): 9 tasks (2 backend tests + 2 backend impl + 4 frontend impl + 1 frontend test)
- Phase 8 (Polish): 14 tasks

**Parallel Opportunities**: 35+ tasks can run in parallel (marked with [P])

**Independent Test Criteria**:
- US1: Create account, sign out, sign in, verify session
- US2: Sign in, create tasks, view list, verify isolation
- US3: Sign in, create task, toggle completion, verify visual change
- US4: Sign in, create task, edit details, verify persistence
- US5: Sign in, create task, delete task, verify removal

**MVP Scope**: Phases 1-4 (Setup + Foundational + US1 + US2) = 68 tasks

**Format Validation**: ✅ All tasks follow checklist format (checkbox, ID, [P] marker where applicable, [Story] label for user story tasks, file paths included)

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- TDD approach: Write tests FIRST, ensure they FAIL, then implement
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- US1 (Authentication) is BLOCKING - must complete before other stories
- US2 (Create/View) is MVP - delivers core value
- US3, US4, US5 can run in parallel after US2 complete
