# Implementation Plan: AI-Powered Todo Chatbot

**Branch**: `003-ai-chatbot` | **Date**: 2026-02-17 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/003-ai-chatbot/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Add conversational AI interface to the existing Phase II full-stack todo application, enabling users to manage tasks through natural language commands. Users can create, view, update, delete, and mark tasks complete using conversational commands like "Add a task to buy groceries" or "Show me all my incomplete tasks". The chatbot integrates with existing authentication and task management systems while maintaining user isolation and data security.

**Technical Approach**: Integrate OpenAI Agents SDK for natural language processing, create MCP tools that wrap existing Phase II task API endpoints, add chat interface component to Next.js dashboard, implement backend chat API endpoint that handles conversation context and routes commands to appropriate MCP tools, maintain JWT authentication for all chat operations.

## Technical Context

**Language/Version**:
- Backend: Python 3.13+ (existing from Phase II)
- Frontend: TypeScript with Next.js 16+ (existing from Phase II)
- AI SDK: OpenAI Agents SDK (latest stable version)

**Primary Dependencies**:
- Backend: FastAPI, SQLModel, OpenAI Python SDK, Official MCP SDK
- Frontend: React 19+, Next.js 16+, OpenAI SDK (for streaming responses)
- Existing: All Phase II dependencies (JWT auth, Neon PostgreSQL, etc.)

**Storage**:
- Task data: Existing Neon PostgreSQL database (no changes)
- Conversation context: In-memory session storage (temporary, not persisted)
- No new database tables required

**Testing**:
- Backend: pytest for MCP tools and chat API endpoints
- Frontend: Jest + React Testing Library for chat components
- Integration: Test conversation flows end-to-end
- Minimum 80% coverage maintained

**Target Platform**:
- Web application (browser-based chat interface)
- Backend: Linux server (same as Phase II)
- No mobile app in Phase III

**Project Type**: Web application (monorepo with frontend/ and backend/)

**Performance Goals**:
- Chat response time: 2-3 seconds for typical commands
- Support 100 concurrent chat sessions
- Real-time sync between chat and traditional UI: <1 second
- OpenAI API calls optimized (batch operations where possible)

**Constraints**:
- Must not break existing Phase II functionality
- OpenAI API rate limits (depends on user's API tier)
- Conversation context limited to last 10-20 messages (token management)
- English language only (no multi-language in Phase III)
- Text-based only (no voice input/output)

**Scale/Scope**:
- Single chat interface per user session
- Support all 5 basic task operations conversationally
- Handle 10+ different phrasings per operation
- Maintain context for 10+ message exchanges

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Spec-Driven Development ✅
- Specification complete in `specs/003-ai-chatbot/spec.md`
- Planning in progress (this document)
- Tasks will be generated via `/sp.tasks` after planning
- All implementation via Claude Code

### Test-First Development ✅
- TDD approach will be followed: write tests before implementation
- Target: 80% code coverage maintained
- Unit tests for MCP tools and chat logic
- Integration tests for conversation flows
- Component tests for chat UI

### Simplicity and Focus ✅
- Building on existing Phase II foundation (no reinvention)
- Minimal new code: chat interface, MCP tools, chat API endpoint
- Reusing all existing task operations (no duplication)
- No over-engineering: session-based context (not persistent storage)

### Clean Architecture ✅
- Clear separation: chat UI → chat API → MCP tools → existing task API
- No circular dependencies
- Chat feature is additive (doesn't modify existing code)
- Follows existing Phase II patterns

### Integration with Existing System ✅
- Uses existing JWT authentication (no separate auth)
- Uses existing task API endpoints (wrapped by MCP tools)
- Uses existing database (no schema changes)
- Maintains existing user isolation

### Security ✅
- OpenAI API key stored securely on backend (never exposed to frontend)
- JWT authentication required for all chat operations
- User isolation maintained (chatbot can only access user's own tasks)
- Input validation on all natural language inputs
- Rate limiting to prevent API abuse

**Gate Status**: ✅ PASSED - All constitution principles satisfied

## Project Structure

### Documentation (this feature)

```text
specs/003-ai-chatbot/
├── spec.md              # Feature specification (complete)
├── plan.md              # This file (in progress)
├── research.md          # Phase 0 output (to be created)
├── data-model.md        # Phase 1 output (to be created)
├── quickstart.md        # Phase 1 output (to be created)
├── contracts/           # Phase 1 output (to be created)
│   ├── chat-api.yaml    # OpenAPI spec for chat endpoints
│   └── mcp-tools.yaml   # MCP tool definitions
└── tasks.md             # Phase 2 output (created by /sp.tasks)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── api/
│   │   ├── auth.py              # Existing (Phase II)
│   │   ├── tasks.py             # Existing (Phase II)
│   │   └── chat.py              # NEW: Chat API endpoint
│   ├── core/
│   │   ├── config.py            # Existing (Phase II)
│   │   ├── database.py          # Existing (Phase II)
│   │   └── security.py          # Existing (Phase II)
│   ├── models/
│   │   ├── user.py              # Existing (Phase II)
│   │   ├── task.py              # Existing (Phase II)
│   │   └── chat.py              # NEW: Chat message models
│   ├── services/
│   │   ├── auth_service.py      # Existing (Phase II)
│   │   ├── task_service.py      # Existing (Phase II)
│   │   └── chat_service.py      # NEW: Chat orchestration
│   ├── mcp/
│   │   ├── __init__.py          # NEW: MCP tools package
│   │   ├── tools.py             # NEW: MCP tool definitions
│   │   └── handlers.py          # NEW: Tool execution handlers
│   └── main.py                  # Existing (updated to include chat router)
└── tests/
    ├── unit/
    │   ├── test_mcp_tools.py    # NEW: MCP tool tests
    │   └── test_chat_service.py # NEW: Chat service tests
    └── integration/
        └── test_chat_api.py     # NEW: Chat API integration tests

frontend/
├── src/
│   ├── app/
│   │   ├── dashboard/
│   │   │   └── page.tsx         # Existing (updated with chat interface)
│   │   └── layout.tsx           # Existing (Phase II)
│   ├── components/
│   │   ├── chat/                # NEW: Chat components
│   │   │   ├── ChatInterface.tsx
│   │   │   ├── ChatMessage.tsx
│   │   │   ├── ChatInput.tsx
│   │   │   └── ChatWindow.tsx
│   │   ├── tasks/               # Existing (Phase II)
│   │   └── ui/                  # Existing (Phase II)
│   └── lib/
│       ├── api.ts               # Existing (updated with chat endpoints)
│       ├── auth.ts              # Existing (Phase II)
│       └── chat.ts              # NEW: Chat utilities
└── tests/
    └── components/
        └── chat/                # NEW: Chat component tests
            ├── ChatInterface.test.tsx
            └── ChatMessage.test.tsx
```

**Structure Decision**: Web application monorepo (Option 2) - building on existing Phase II structure. New code is additive: chat API endpoint, MCP tools package, and chat UI components. No modifications to existing Phase II code except for integration points (adding chat router to main.py, adding chat interface to dashboard).

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

No violations - all constitution principles are satisfied. Phase III builds cleanly on Phase II foundation without introducing unnecessary complexity.

## Phase 0: Research & Technology Decisions

### Research Tasks

1. **OpenAI Agents SDK Integration**
   - Research: How to set up and use OpenAI Agents SDK in Python backend
   - Research: Best practices for streaming responses from OpenAI
   - Research: Token management and context window optimization
   - Research: Error handling for OpenAI API failures

2. **MCP SDK Implementation**
   - Research: Official MCP SDK documentation and setup
   - Research: How to create MCP tools that wrap existing REST APIs
   - Research: MCP tool parameter validation and error handling
   - Research: Best practices for tool naming and descriptions

3. **Conversation Context Management**
   - Research: Session-based context storage patterns
   - Research: Context pruning strategies (keeping last N messages)
   - Research: How to maintain context across multiple tool calls
   - Research: When to reset context (timeout, explicit user request)

4. **Chat UI Integration**
   - Research: React patterns for real-time chat interfaces
   - Research: Streaming response rendering in React
   - Research: Optimistic UI updates for chat messages
   - Research: Accessibility best practices for chat interfaces

5. **Security Considerations**
   - Research: Secure storage of OpenAI API keys in FastAPI
   - Research: Rate limiting strategies for AI API calls
   - Research: Input sanitization for natural language inputs
   - Research: Preventing prompt injection attacks

### Technology Decisions (to be documented in research.md)

- **OpenAI Model**: GPT-4 or GPT-3.5-turbo (decision based on cost/performance tradeoff)
- **MCP Tool Framework**: Official MCP SDK vs custom implementation
- **Context Storage**: In-memory session store vs Redis (decision based on scale requirements)
- **Frontend Chat Library**: Custom React components vs existing chat UI library
- **Streaming Strategy**: Server-Sent Events (SSE) vs WebSockets vs polling

## Phase 1: Design Artifacts

### Data Model (data-model.md)

**New Entities**:
- ChatMessage: Represents a single message in conversation
- Conversation: Represents a chat session
- MCPTool: Represents an available tool for the AI agent

**No Database Changes**: All entities are transient (session-based), no new tables required.

### API Contracts (contracts/)

**New Endpoints**:
- POST /api/chat - Send message and receive response
- GET /api/chat/history - Get conversation history (optional)
- DELETE /api/chat/session - Clear conversation context

**MCP Tools**:
- create_task: Wraps POST /api/{user_id}/tasks
- list_tasks: Wraps GET /api/{user_id}/tasks
- get_task: Wraps GET /api/{user_id}/tasks/{id}
- update_task: Wraps PUT /api/{user_id}/tasks/{id}
- delete_task: Wraps DELETE /api/{user_id}/tasks/{id}
- mark_complete: Wraps PATCH /api/{user_id}/tasks/{id}/complete

### Quick Start (quickstart.md)

Setup instructions for:
- Installing OpenAI SDK and MCP SDK
- Configuring OpenAI API key
- Running chat interface locally
- Testing conversational commands
- Troubleshooting common issues

## Phase 2: Task Breakdown (via /sp.tasks)

Tasks will be generated after Phase 1 design is complete. Expected task categories:

1. **Backend MCP Tools** (5-8 tasks)
   - Create MCP tool definitions
   - Implement tool handlers
   - Add authentication to tool calls
   - Write unit tests

2. **Backend Chat API** (5-8 tasks)
   - Create chat endpoint
   - Implement conversation context management
   - Integrate OpenAI Agents SDK
   - Add error handling
   - Write integration tests

3. **Frontend Chat UI** (8-12 tasks)
   - Create chat components
   - Implement message rendering
   - Add input handling
   - Integrate with chat API
   - Add streaming response support
   - Write component tests

4. **Integration & Polish** (3-5 tasks)
   - Integrate chat into dashboard
   - Add real-time sync with task list
   - Add loading states and error handling
   - End-to-end testing
   - Documentation updates

**Estimated Total**: 25-35 tasks

## Risk Assessment

### Technical Risks

1. **OpenAI API Rate Limits**
   - Risk: Users may hit rate limits during testing
   - Mitigation: Implement rate limiting on backend, provide clear error messages
   - Fallback: Queue requests or suggest retry timing

2. **Context Window Limitations**
   - Risk: Long conversations may exceed token limits
   - Mitigation: Implement context pruning (keep last 10-20 messages)
   - Fallback: Warn user when context is reset

3. **Natural Language Ambiguity**
   - Risk: AI may misinterpret user commands
   - Mitigation: Implement confirmation prompts for destructive actions
   - Fallback: Provide "undo" capability or clarifying questions

4. **Integration Complexity**
   - Risk: Chat interface may conflict with existing UI
   - Mitigation: Thorough testing of both interfaces
   - Fallback: Make chat interface optional (can be hidden)

### Mitigation Strategies

- Start with P1 user story (basic create/view) to validate approach
- Implement comprehensive error handling early
- Add extensive logging for debugging AI behavior
- Create fallback responses for API failures
- Test with various phrasings and edge cases

## Success Metrics

- All 5 user stories (P1-P5) implemented and tested
- 18 functional requirements satisfied
- 10 success criteria met (95% accuracy, 2-second response time, etc.)
- No regression in Phase II functionality
- 80%+ test coverage maintained
- Chat interface accessible and usable

## Next Steps

1. ✅ Complete this plan document
2. ⏭️ Execute Phase 0: Generate research.md
3. ⏭️ Execute Phase 1: Generate data-model.md, contracts/, quickstart.md
4. ⏭️ Run `/sp.tasks` to generate task breakdown
5. ⏭️ Run `/sp.implement` to execute tasks
