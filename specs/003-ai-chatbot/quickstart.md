# Quick Start Guide: AI-Powered Todo Chatbot (Phase III)

**Feature**: 003-ai-chatbot
**Date**: 2026-02-17
**Purpose**: Setup and development guide for Phase III chat functionality

## Overview

This guide walks you through setting up and developing the Phase III AI-powered chatbot feature. This builds on top of Phase II (full-stack web application) and adds conversational AI capabilities for natural language task management.

---

## Prerequisites

### Required Software

- **Node.js**: 18.x or higher (from Phase II)
- **Python**: 3.13+ (from Phase II)
- **UV**: Python package manager (from Phase II)
- **Git**: Version control (from Phase II)
- **OpenAI API Key**: Required for AI functionality (NEW)

### Accounts Needed

- **OpenAI Account**: For API access (https://platform.openai.com)
- **Neon Account**: For PostgreSQL database (from Phase II)
- **Vercel Account**: For frontend deployment (optional, from Phase II)

### Phase II Completion

Phase III requires a working Phase II application:
- ✅ Backend API running (FastAPI)
- ✅ Frontend running (Next.js)
- ✅ Database configured (Neon PostgreSQL)
- ✅ Authentication working (JWT)
- ✅ Task CRUD operations functional

---

## Step 1: Get OpenAI API Key

### Create OpenAI Account

1. Go to https://platform.openai.com
2. Sign up or sign in
3. Navigate to API Keys section
4. Click "Create new secret key"
5. Copy the key (starts with `sk-...`)
6. **Important**: Save this key securely - you won't see it again

### Set API Key in Environment

Edit your `.env` file (in repository root):

```bash
# Existing Phase II variables
DATABASE_URL=postgresql+asyncpg://...
BETTER_AUTH_SECRET=your-secret-key
NEXT_PUBLIC_API_URL=http://localhost:8000

# NEW: Phase III variables
OPENAI_API_KEY=sk-your-openai-api-key-here
OPENAI_MODEL=gpt-4-turbo
```

**Security Note**: Never commit `.env` file to git. It's already in `.gitignore`.

---

## Step 2: Install Phase III Dependencies

### Backend Dependencies

```bash
cd backend

# Install OpenAI SDK (COMPLETED)
uv pip install openai

# Verify installation
uv pip list | grep openai
```

### Frontend Dependencies

```bash
cd frontend

# Install react-markdown (COMPLETED)
npm install react-markdown

# Verify installation
npm list react-markdown
```

**Status**: ✅ All dependencies installed

---

## Step 3: Verify Phase II is Working

Before starting Phase III development, ensure Phase II is fully functional:

### Start Backend

```bash
cd backend
uv run uvicorn src.main:app --reload --port 8000
```

Verify at http://localhost:8000/docs

### Start Frontend

```bash
cd frontend
npm run dev
```

Verify at http://localhost:3000

### Test Phase II Functionality

1. Sign up / Sign in
2. Create a task
3. View task list
4. Mark task complete
5. Edit task
6. Delete task

If any of these fail, fix Phase II before proceeding to Phase III.

---

## Step 4: Development Workflow

### Phase III Development Structure

```
specs/003-ai-chatbot/
├── spec.md              # Feature specification ✅
├── plan.md              # Implementation plan ✅
├── research.md          # Technology research ✅
├── data-model.md        # Data structures ✅
├── contracts/           # API contracts ✅
│   ├── chat-api.yaml
│   └── mcp-tools.md
├── quickstart.md        # This file ✅
└── tasks.md             # Task breakdown (to be generated)
```

### Generate Tasks

```bash
# From repository root
# This will generate tasks.md with all implementation tasks
/sp.tasks
```

### Implement Tasks

```bash
# From repository root
# This will execute all tasks in tasks.md
/sp.implement
```

---

## Step 5: Testing the Chat Interface

### Manual Testing

Once implementation is complete:

1. **Start Backend**:
   ```bash
   cd backend
   uv run uvicorn src.main:app --reload --port 8000
   ```

2. **Start Frontend**:
   ```bash
   cd frontend
   npm run dev
   ```

3. **Open Dashboard**: http://localhost:3000/dashboard

4. **Test Chat Commands**:
   - "Add a task to buy groceries"
   - "Show me all my tasks"
   - "Mark my first task as complete"
   - "Update my second task to say meeting at 3pm"
   - "Delete all completed tasks"

### Automated Testing

Run backend tests:
```bash
cd backend
uv run pytest tests/unit/test_mcp_tools.py -v
uv run pytest tests/unit/test_chat_service.py -v
uv run pytest tests/integration/test_chat_api.py -v
```

Run frontend tests:
```bash
cd frontend
npm test -- tests/components/chat/
```

---

## Step 6: Common Development Tasks

### Add New MCP Tool

1. Define tool in `backend/src/mcp/tools.py`
2. Implement handler in `backend/src/mcp/handlers.py`
3. Register tool with OpenAI client
4. Write unit tests
5. Update documentation

### Modify Chat UI

1. Edit components in `frontend/src/components/chat/`
2. Update styles with Tailwind CSS
3. Test responsiveness
4. Write component tests

### Debug AI Behavior

1. Check logs in backend console
2. Inspect tool calls in response
3. Verify system prompt is correct
4. Test with different phrasings
5. Adjust tool descriptions if needed

### Monitor OpenAI API Usage

1. Check usage at https://platform.openai.com/usage
2. Set budget alerts in OpenAI dashboard
3. Monitor costs per request
4. Optimize context window if needed

---

## Step 7: Troubleshooting

### Backend Issues

**Issue**: `ModuleNotFoundError: No module named 'openai'`
**Solution**:
```bash
cd backend
uv pip install openai
```

**Issue**: `openai.AuthenticationError: Invalid API key`
**Solution**:
- Check `.env` file has correct `OPENAI_API_KEY`
- Verify key starts with `sk-`
- Regenerate key if needed

**Issue**: `Rate limit exceeded`
**Solution**:
- Wait a few minutes and retry
- Check OpenAI dashboard for rate limits
- Upgrade OpenAI plan if needed
- Implement request queuing

**Issue**: `Context length exceeded`
**Solution**:
- Reduce conversation history (keep fewer messages)
- Shorten system prompt
- Use GPT-3.5-turbo instead of GPT-4

### Frontend Issues

**Issue**: Chat interface not showing
**Solution**:
- Check browser console for errors
- Verify chat component is imported in dashboard
- Check CSS classes are applied correctly

**Issue**: Messages not sending
**Solution**:
- Check network tab for API errors
- Verify JWT token is being sent
- Check CORS configuration

**Issue**: Streaming not working
**Solution**:
- Verify SSE endpoint is configured
- Check browser supports EventSource
- Test with polling as fallback

### Integration Issues

**Issue**: Chat creates tasks but they don't appear in task list
**Solution**:
- Check real-time sync is working
- Verify user_id matches between chat and tasks
- Refresh page to force reload

**Issue**: AI misinterprets commands
**Solution**:
- Improve tool descriptions
- Add more examples to system prompt
- Test with different phrasings
- Implement clarifying questions

---

## Step 8: API Documentation

### Interactive API Docs

Once backend is running, access interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Test Chat API with curl

```bash
# Get JWT token first (from Phase II)
TOKEN="your-jwt-token-here"

# Send chat message
curl -X POST http://localhost:8000/api/chat \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Add a task to buy groceries",
    "session_id": null
  }'

# Response:
# {
#   "message": "I've created a task: Buy groceries",
#   "session_id": "550e8400-e29b-41d4-a716-446655440000",
#   "tool_calls": [...],
#   "timestamp": "2026-02-17T10:30:15Z"
# }

# Continue conversation
curl -X POST http://localhost:8000/api/chat \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Show me all my tasks",
    "session_id": "550e8400-e29b-41d4-a716-446655440000"
  }'

# Clear session
curl -X DELETE http://localhost:8000/api/chat/session/550e8400-e29b-41d4-a716-446655440000 \
  -H "Authorization: Bearer $TOKEN"
```

---

## Step 9: Deployment (Optional)

### Frontend Deployment (Vercel)

Phase III frontend deploys the same way as Phase II:

```bash
cd frontend
vercel
```

No additional configuration needed - chat interface is part of the dashboard.

### Backend Deployment (Railway/Render)

Add OpenAI API key to environment variables:

1. Go to Railway/Render dashboard
2. Navigate to environment variables
3. Add: `OPENAI_API_KEY=sk-...`
4. Add: `OPENAI_MODEL=gpt-4-turbo`
5. Redeploy backend

### Cost Considerations

**OpenAI API Costs** (GPT-4-turbo):
- ~$0.02 per conversation exchange
- ~$600/month for 100 users × 10 messages/day

**Optimization**:
- Use GPT-3.5-turbo for simple queries (5x cheaper)
- Implement caching for common responses
- Set max_tokens limits
- Monitor usage and set budget alerts

---

## Step 10: Development Best Practices

### Code Quality

- Follow existing Phase II patterns
- Write tests before implementation (TDD)
- Use type hints in Python
- Use TypeScript in frontend
- Run linters before committing

### Git Workflow

```bash
# Work on feature branch
git checkout 003-ai-chatbot

# Commit frequently with clear messages
git add .
git commit -m "feat: implement MCP tools for task operations"

# Push to remote
git push origin 003-ai-chatbot

# Create PR when ready
gh pr create --title "Phase III: AI-Powered Todo Chatbot"
```

### Testing Strategy

1. **Unit Tests**: Test individual components (tools, handlers)
2. **Integration Tests**: Test API endpoints end-to-end
3. **Component Tests**: Test React components
4. **Manual Tests**: Test conversational flows

### Documentation

- Update README.md with Phase III features
- Document new API endpoints
- Add examples of chat commands
- Create troubleshooting guide

---

## Resources

### Documentation

- **OpenAI API**: https://platform.openai.com/docs
- **OpenAI Function Calling**: https://platform.openai.com/docs/guides/function-calling
- **FastAPI**: https://fastapi.tiangolo.com/
- **Next.js**: https://nextjs.org/docs
- **React**: https://react.dev/learn

### Project Documentation

- **Specification**: `specs/003-ai-chatbot/spec.md`
- **Implementation Plan**: `specs/003-ai-chatbot/plan.md`
- **Research**: `specs/003-ai-chatbot/research.md`
- **Data Model**: `specs/003-ai-chatbot/data-model.md`
- **API Contracts**: `specs/003-ai-chatbot/contracts/`

### Phase II Documentation

- **Phase II Spec**: `specs/002-fullstack-web-app/spec.md`
- **Phase II Plan**: `specs/002-fullstack-web-app/plan.md`
- **Phase II Tasks**: `specs/002-fullstack-web-app/tasks.md`

---

## Next Steps

1. ✅ Complete quickstart guide (this document)
2. ⏭️ Run `/sp.tasks` to generate task breakdown
3. ⏭️ Run `/sp.implement` to execute tasks
4. ⏭️ Test chat functionality
5. ⏭️ Deploy to production

---

## Support

If you encounter issues not covered in this guide:

1. Check the troubleshooting section above
2. Review the specification and plan documents
3. Check API contracts for endpoint details
4. Consult framework documentation (links above)
5. Check OpenAI API status: https://status.openai.com

**Happy coding! 🚀**
