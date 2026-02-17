# Tasks: AI-Powered Todo Chatbot

**Input**: Design documents from `/specs/003-ai-chatbot/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

**Tests**: Not explicitly requested in specification - focusing on implementation tasks only

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app monorepo**: `backend/src/`, `frontend/src/`
- Backend: Python 3.13+ with FastAPI
- Frontend: TypeScript with Next.js 16+ and React 19+

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and dependency installation

- [X] T001 Install OpenAI Python SDK in backend using `uv pip install openai`
- [X] T002 [P] Install react-markdown in frontend using `npm install react-markdown`
- [X] T003 [P] Add OPENAI_API_KEY and OPENAI_MODEL to .env.example file
- [X] T004 Update backend/src/core/config.py to include OpenAI configuration settings

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T005 [P] Create ChatMessage model in backend/src/models/chat.py with role, content, timestamp, tool_calls fields
- [X] T006 [P] Create Conversation model in backend/src/models/chat.py with session_id, user_id, messages, created_at, last_activity, is_active fields
- [X] T007 [P] Create ChatRequest and ChatResponse schemas in backend/src/models/chat.py
- [X] T008 [P] Create ToolCall model in backend/src/models/chat.py with tool_name, arguments, result, error fields
- [X] T009 Create in-memory session store in backend/src/services/chat_service.py with dict[UUID, Conversation]
- [X] T010 Create OpenAI client initialization in backend/src/services/chat_service.py with API key from config
- [X] T011 [P] Create MCP tools package structure: backend/src/mcp/__init__.py
- [X] T012 Create system prompt template in backend/src/mcp/tools.py with task management assistant instructions
- [X] T013 Setup JWT authentication dependency for chat endpoints in backend/src/api/chat.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Basic Conversational Task Creation and Viewing (Priority: P1) 🎯 MVP

**Goal**: Users can create and view tasks using natural language commands through a chat interface

**Independent Test**: User opens chat, types "Add a task to buy groceries", sees confirmation, then types "Show me all my tasks" and sees the newly created task

### Implementation for User Story 1

- [X] T014 [P] [US1] Define create_task MCP tool in backend/src/mcp/tools.py with title and description parameters
- [X] T015 [P] [US1] Define list_tasks MCP tool in backend/src/mcp/tools.py with optional completed filter parameter
- [X] T016 [P] [US1] Implement handle_create_task handler in backend/src/mcp/handlers.py that calls existing TaskService
- [X] T017 [P] [US1] Implement handle_list_tasks handler in backend/src/mcp/handlers.py that calls existing TaskService
- [X] T018 [US1] Create ChatService class in backend/src/services/chat_service.py with process_message method
- [X] T019 [US1] Implement OpenAI API integration in ChatService.process_message with tool calling support
- [X] T020 [US1] Implement tool execution logic in ChatService that routes tool calls to appropriate handlers
- [X] T021 [US1] Create POST /api/chat endpoint in backend/src/api/chat.py with JWT authentication
- [X] T022 [US1] Implement conversation context management (get or create session) in chat endpoint
- [X] T023 [US1] Add chat router to backend/src/main.py
- [X] T024 [P] [US1] Create ChatMessage component in frontend/src/components/chat/ChatMessage.tsx for rendering individual messages
- [X] T025 [P] [US1] Create ChatInput component in frontend/src/components/chat/ChatInput.tsx with text input and send button
- [X] T026 [P] [US1] Create ChatWindow component in frontend/src/components/chat/ChatWindow.tsx for scrollable message list
- [X] T027 [US1] Create ChatInterface component in frontend/src/components/chat/ChatInterface.tsx that manages chat state
- [X] T028 [US1] Implement sendMessage function in ChatInterface that calls POST /api/chat with JWT token
- [X] T029 [US1] Add chat API client functions in frontend/src/lib/chat.ts for sending messages
- [X] T030 [US1] Integrate ChatInterface into dashboard page at frontend/src/app/dashboard/page.tsx
- [X] T031 [US1] Style chat components with Tailwind CSS for consistent design with Phase II

**Checkpoint**: At this point, User Story 1 should be fully functional - users can create and view tasks conversationally

---

## Phase 4: User Story 2 - Conversational Task Updates and Completion (Priority: P2)

**Goal**: Users can update task details and mark tasks as complete using natural language

**Independent Test**: User creates task via chat, says "Mark my first task as complete", sees confirmation, then says "Show completed tasks" and sees the marked task

### Implementation for User Story 2

- [X] T032 [P] [US2] Define update_task MCP tool in backend/src/mcp/tools.py with task_id, title, description parameters
- [X] T033 [P] [US2] Define mark_complete MCP tool in backend/src/mcp/tools.py with task_id and completed parameters
- [X] T034 [P] [US2] Implement handle_update_task handler in backend/src/mcp/handlers.py that calls existing TaskService
- [X] T035 [P] [US2] Implement handle_mark_complete handler in backend/src/mcp/handlers.py that calls existing TaskService
- [X] T036 [US2] Register update_task and mark_complete tools with OpenAI client in ChatService
- [X] T037 [US2] Update ChatMessage component to display tool call results (task updated, marked complete)
- [X] T038 [US2] Add visual indicators in ChatMessage for successful task operations (checkmarks, status badges)

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently - full CRUD except delete

---

## Phase 5: User Story 3 - Conversational Task Deletion (Priority: P3)

**Goal**: Users can delete tasks using natural language commands with appropriate safeguards

**Independent Test**: User creates task, says "Delete my last task", confirms when prompted, and verifies task is removed

### Implementation for User Story 3

- [X] T039 [US3] Define delete_task MCP tool in backend/src/mcp/tools.py with task_id parameter
- [X] T040 [US3] Implement handle_delete_task handler in backend/src/mcp/handlers.py that calls existing TaskService
- [X] T041 [US3] Add confirmation logic in ChatService for delete operations (detect delete intent, ask for confirmation)
- [X] T042 [US3] Implement confirmation state tracking in Conversation model (pending_action field)
- [X] T043 [US3] Update ChatService to handle confirmation responses ("yes", "no", "cancel")
- [X] T044 [US3] Register delete_task tool with OpenAI client in ChatService
- [X] T045 [US3] Add confirmation UI in ChatMessage component for destructive actions

**Checkpoint**: All basic CRUD operations now available conversationally with safety measures

---

## Phase 6: User Story 4 - Context-Aware Conversations (Priority: P4)

**Goal**: Chatbot remembers previous messages and handles follow-up questions with context

**Independent Test**: User asks "Show my tasks", then follows up with "Mark the second one as complete" without re-specifying which list

### Implementation for User Story 4

- [X] T046 [US4] Implement sliding window context management in ChatService (keep last 15 messages)
- [X] T047 [US4] Add context pruning logic in add_message method to maintain message limit
- [X] T048 [US4] Implement session timeout logic (30 minutes of inactivity) in ChatService
- [X] T049 [US4] Create cleanup_inactive_sessions background task in backend/src/services/chat_service.py
- [X] T050 [US4] Add session cleanup scheduler using FastAPI background tasks in backend/src/main.py
- [X] T051 [US4] Implement context reset on timeout with user notification
- [X] T052 [US4] Add DELETE /api/chat/session/{session_id} endpoint in backend/src/api/chat.py for manual context clearing
- [X] T053 [US4] Add "Clear conversation" button in ChatInterface component

**Checkpoint**: Conversations now feel natural with context awareness and proper cleanup

---

## Phase 7: User Story 5 - Seamless Dashboard Integration (Priority: P5)

**Goal**: Chat interface integrates smoothly with existing Phase II dashboard UI

**Independent Test**: User creates task via chat, switches to traditional task list, sees task there, edits via UI, switches back to chat, asks about task, sees updated info

### Implementation for User Story 5

- [ ] T054 [US5] Implement real-time task list refresh in frontend when chat creates/updates tasks
- [ ] T055 [US5] Add event emitter or state management for cross-component task synchronization
- [ ] T056 [US5] Update traditional task list component to listen for chat-triggered changes
- [X] T057 [US5] Add responsive design for chat interface (mobile, tablet, desktop) using Tailwind breakpoints
- [X] T058 [US5] Implement chat interface toggle/minimize functionality in dashboard
- [X] T059 [US5] Add smooth transitions and animations for chat interface show/hide
- [X] T060 [US5] Ensure chat interface doesn't block traditional UI interactions
- [X] T061 [US5] Add accessibility features: ARIA labels, keyboard navigation, focus management

**Checkpoint**: All user stories complete - chat and traditional UI work seamlessly together

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories and overall quality

- [X] T062 [P] Add comprehensive error handling in ChatService for OpenAI API failures
- [X] T063 [P] Add rate limiting middleware in backend/src/api/chat.py (20 requests per minute per user)
- [X] T064 [P] Add input validation in chat endpoint (max 1000 characters, non-empty message)
- [X] T065 [P] Implement HTML escaping for user messages to prevent XSS attacks
- [X] T066 [P] Add loading states and typing indicators in ChatInterface component
- [X] T067 [P] Add error message display in ChatMessage component for failed operations
- [X] T068 [P] Add retry logic for transient OpenAI API errors in ChatService
- [X] T069 Update README.md with Phase III features and chat interface usage instructions
- [X] T070 Update quickstart.md with actual implementation details and troubleshooting
- [X] T071 Add logging for all tool calls and AI responses in ChatService for debugging
- [ ] T072 Verify all 18 functional requirements (FR-001 to FR-018) are satisfied
- [ ] T073 Verify all 10 success criteria (SC-001 to SC-010) are met
- [ ] T074 Run manual testing of all 5 user stories end-to-end
- [ ] T075 Verify no regression in Phase II functionality (traditional UI still works)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-7)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3 → P4 → P5)
- **Polish (Phase 8)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Extends US1 tools but independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Adds delete with confirmation, independently testable
- **User Story 4 (P4)**: Can start after Foundational (Phase 2) - Enhances context management, independently testable
- **User Story 5 (P5)**: Depends on US1 completion (needs basic chat working) - Adds integration polish

### Within Each User Story

- MCP tool definitions before handlers
- Handlers before ChatService integration
- Backend API before frontend components
- Individual components before integration
- Core functionality before polish

### Parallel Opportunities

- **Phase 1**: All tasks can run in parallel (T002, T003)
- **Phase 2**: Models (T005-T008) and MCP setup (T011-T012) can run in parallel
- **Phase 3 (US1)**:
  - MCP tools (T014, T015) in parallel
  - Handlers (T016, T017) in parallel after tools
  - Frontend components (T024, T025, T026) in parallel
- **Phase 4 (US2)**: Tools (T032, T033) and handlers (T034, T035) in parallel
- **Phase 8**: Most polish tasks (T062-T068) can run in parallel

---

## Parallel Example: User Story 1

```bash
# Launch MCP tool definitions together:
Task: "Define create_task MCP tool in backend/src/mcp/tools.py"
Task: "Define list_tasks MCP tool in backend/src/mcp/tools.py"

# Launch handlers together (after tools complete):
Task: "Implement handle_create_task handler in backend/src/mcp/handlers.py"
Task: "Implement handle_list_tasks handler in backend/src/mcp/handlers.py"

# Launch frontend components together:
Task: "Create ChatMessage component in frontend/src/components/chat/ChatMessage.tsx"
Task: "Create ChatInput component in frontend/src/components/chat/ChatInput.tsx"
Task: "Create ChatWindow component in frontend/src/components/chat/ChatWindow.tsx"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T004)
2. Complete Phase 2: Foundational (T005-T013) - CRITICAL
3. Complete Phase 3: User Story 1 (T014-T031)
4. **STOP and VALIDATE**: Test User Story 1 independently
   - Can create tasks via chat?
   - Can view tasks via chat?
   - Does traditional UI still work?
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready (13 tasks)
2. Add User Story 1 → Test independently → Deploy/Demo (MVP! - 18 tasks)
3. Add User Story 2 → Test independently → Deploy/Demo (7 tasks)
4. Add User Story 3 → Test independently → Deploy/Demo (7 tasks)
5. Add User Story 4 → Test independently → Deploy/Demo (8 tasks)
6. Add User Story 5 → Test independently → Deploy/Demo (8 tasks)
7. Add Polish → Final release (14 tasks)
8. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together (T001-T013)
2. Once Foundational is done:
   - Developer A: User Story 1 (T014-T031)
   - Developer B: User Story 2 (T032-T038) - can start in parallel
   - Developer C: User Story 3 (T039-T045) - can start in parallel
3. After US1-3 complete:
   - Developer A: User Story 4 (T046-T053)
   - Developer B: User Story 5 (T054-T061) - depends on US1
4. All developers: Polish (T062-T075) in parallel

---

## Task Summary

**Total Tasks**: 75

**By Phase**:
- Phase 1 (Setup): 4 tasks
- Phase 2 (Foundational): 9 tasks
- Phase 3 (US1 - MVP): 18 tasks
- Phase 4 (US2): 7 tasks
- Phase 5 (US3): 7 tasks
- Phase 6 (US4): 8 tasks
- Phase 7 (US5): 8 tasks
- Phase 8 (Polish): 14 tasks

**Parallel Opportunities**: 28 tasks marked [P] can run in parallel within their phase

**MVP Scope**: Phases 1-3 (31 tasks) delivers basic conversational task creation and viewing

**Full Feature**: All 75 tasks delivers complete AI-powered chatbot with all 5 user stories

---

## Notes

- [P] tasks = different files, no dependencies within phase
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Tests not included as not explicitly requested in specification
- All tasks reference exact file paths for clarity
- Backend uses existing Phase II TaskService - no duplication
- Frontend integrates with existing Phase II dashboard
- No database schema changes - all chat data is transient
