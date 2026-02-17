# Quick Start Guide: Todo Full-Stack Web Application (Phase II)

**Feature**: 002-fullstack-web-app
**Date**: 2026-02-17
**Purpose**: Development environment setup and getting started guide

## Overview

This guide walks you through setting up the development environment for the Phase II full-stack web application. The project uses a monorepo structure with separate frontend (Next.js) and backend (FastAPI) directories.

---

## Prerequisites

### Required Software

- **Node.js**: 18.x or higher (for Next.js frontend)
- **Python**: 3.13+ (for FastAPI backend)
- **UV**: Python package manager
- **Git**: Version control
- **PostgreSQL Client**: For database access (optional, for debugging)

### Accounts Needed

- **Neon Account**: For serverless PostgreSQL database (free tier)
- **Vercel Account**: For frontend deployment (optional, free tier)

---

## Project Structure

```
hackathon2shzaib/
├── frontend/              # Next.js application
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── ...
├── backend/               # FastAPI application
│   ├── src/
│   ├── tests/
│   ├── pyproject.toml
│   └── ...
├── specs/                 # Specifications
│   └── 002-fullstack-web-app/
├── .env.example           # Environment variables template
└── README.md
```

---

## Step 1: Clone and Setup Repository

```bash
# Clone the repository (if not already cloned)
git clone <repository-url>
cd hackathon2shzaib

# Checkout Phase II branch
git checkout 002-fullstack-web-app

# Copy environment variables template
cp .env.example .env
```

---

## Step 2: Database Setup (Neon PostgreSQL)

### Create Neon Database

1. Go to [neon.tech](https://neon.tech) and sign up (free tier)
2. Create a new project: "todo-app-phase2"
3. Copy the connection string from the dashboard

### Configure Database Connection

Edit `.env` file and add your Neon connection string:

```env
# Database
DATABASE_URL=postgresql://user:password@ep-xxx.us-east-2.aws.neon.tech/neondb?sslmode=require

# JWT Secret (generate a secure random string)
BETTER_AUTH_SECRET=your-super-secret-key-min-32-chars-long-random-string

# API URLs
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Generate JWT Secret

```bash
# Python method
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Or use this value for development (NEVER use in production)
# BETTER_AUTH_SECRET=dev-secret-key-only-for-local-testing-min-32-chars
```

---

## Step 3: Backend Setup (FastAPI)

### Install Dependencies

```bash
cd backend

# Create virtual environment with UV
uv venv

# Activate virtual environment
# On Linux/Mac:
source .venv/bin/activate
# On Windows:
.venv\Scripts\activate

# Install dependencies
uv pip install -e .

# Install development dependencies
uv pip install pytest pytest-asyncio pytest-cov httpx
```

### Run Database Migrations

```bash
# Initialize Alembic (first time only)
alembic init alembic

# Create initial migration
alembic revision --autogenerate -m "Initial schema: users and tasks"

# Apply migrations
alembic upgrade head
```

### Run Backend Server

```bash
# Development mode with auto-reload
uvicorn src.main:app --reload --port 8000

# Server will start at http://localhost:8000
# API docs available at http://localhost:8000/docs
```

### Verify Backend

```bash
# Test health endpoint
curl http://localhost:8000/health

# Expected response: {"status": "healthy"}
```

---

## Step 4: Frontend Setup (Next.js)

### Install Dependencies

```bash
cd frontend

# Install Node.js dependencies
npm install

# Or using yarn
yarn install
```

### Configure Environment Variables

Create `frontend/.env.local`:

```env
# API URL
NEXT_PUBLIC_API_URL=http://localhost:8000

# Better Auth Secret (must match backend)
BETTER_AUTH_SECRET=your-super-secret-key-min-32-chars-long-random-string
```

### Run Frontend Development Server

```bash
# Start Next.js dev server
npm run dev

# Or using yarn
yarn dev

# Server will start at http://localhost:3000
```

### Verify Frontend

Open browser and navigate to:
- http://localhost:3000 - Landing page
- http://localhost:3000/signin - Sign in page
- http://localhost:3000/signup - Sign up page

---

## Step 5: Run Tests

### Backend Tests

```bash
cd backend

# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=term-missing

# Run specific test file
pytest tests/unit/test_models.py -v

# Run integration tests
pytest tests/integration/ -v
```

### Frontend Tests

```bash
cd frontend

# Run all tests
npm test

# Run with coverage
npm test -- --coverage

# Run in watch mode
npm test -- --watch
```

---

## Step 6: Development Workflow

### Starting Development Session

```bash
# Terminal 1: Backend
cd backend
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
uvicorn src.main:app --reload --port 8000

# Terminal 2: Frontend
cd frontend
npm run dev

# Terminal 3: Tests (optional)
cd backend
pytest --watch  # or use pytest-watch
```

### Making Changes

1. **Read the spec**: Check `specs/002-fullstack-web-app/spec.md`
2. **Check the plan**: Review `specs/002-fullstack-web-app/plan.md`
3. **Review contracts**: See `specs/002-fullstack-web-app/contracts/`
4. **Write tests first**: Follow TDD (Red → Green → Refactor)
5. **Implement feature**: Write minimal code to pass tests
6. **Verify**: Run tests and manual testing
7. **Document**: Create PHR in `history/prompts/002-fullstack-web-app/`

---

## Common Development Tasks

### Create New Database Migration

```bash
cd backend

# Auto-generate migration from model changes
alembic revision --autogenerate -m "Add new field to tasks"

# Review generated migration in alembic/versions/

# Apply migration
alembic upgrade head

# Rollback migration (if needed)
alembic downgrade -1
```

### Add New API Endpoint

1. Define route in `backend/src/api/tasks.py` or `backend/src/api/auth.py`
2. Add service logic in `backend/src/services/`
3. Write tests in `backend/tests/integration/`
4. Update API contract in `specs/002-fullstack-web-app/contracts/`

### Add New Frontend Component

1. Create component in `frontend/src/components/`
2. Write tests in `frontend/tests/components/`
3. Import and use in pages
4. Update UI documentation

### Debug Database Queries

```bash
# Connect to Neon database
psql "postgresql://user:password@ep-xxx.us-east-2.aws.neon.tech/neondb?sslmode=require"

# List tables
\dt

# View users
SELECT * FROM users;

# View tasks
SELECT * FROM tasks;

# Exit
\q
```

---

## Troubleshooting

### Backend Issues

**Issue**: `ModuleNotFoundError: No module named 'src'`
**Solution**: Make sure you're in the backend directory and virtual environment is activated. Run `uv pip install -e .`

**Issue**: `sqlalchemy.exc.OperationalError: could not connect to server`
**Solution**: Check DATABASE_URL in .env file. Verify Neon database is running.

**Issue**: `jose.exceptions.JWTError: Signature verification failed`
**Solution**: Ensure BETTER_AUTH_SECRET matches between frontend and backend.

**Issue**: `CORS error when calling API from frontend`
**Solution**: Check CORS configuration in `backend/src/main.py`. Ensure frontend URL is in `allow_origins`.

### Frontend Issues

**Issue**: `Error: Cannot find module 'next'`
**Solution**: Run `npm install` in frontend directory.

**Issue**: `API calls return 401 Unauthorized`
**Solution**: Check JWT token is being sent in Authorization header. Verify token is valid.

**Issue**: `Environment variables not loading`
**Solution**: Restart Next.js dev server after changing `.env.local`. Ensure variables start with `NEXT_PUBLIC_` for client-side access.

### Database Issues

**Issue**: `relation "users" does not exist`
**Solution**: Run database migrations: `alembic upgrade head`

**Issue**: `duplicate key value violates unique constraint "users_email_key"`
**Solution**: Email already exists. Use different email or delete existing user.

---

## Testing Checklist

Before committing code, verify:

- [ ] All backend tests pass (`pytest`)
- [ ] All frontend tests pass (`npm test`)
- [ ] Backend linting passes (`ruff check src/`)
- [ ] Backend type checking passes (`mypy src/`)
- [ ] Frontend linting passes (`npm run lint`)
- [ ] Manual testing completed (signup, signin, CRUD operations)
- [ ] API documentation updated (if endpoints changed)
- [ ] PHR created for development session

---

## API Documentation

### Interactive API Docs

Once backend is running, access interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Test API with curl

```bash
# Signup
curl -X POST http://localhost:8000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"SecurePass123"}'

# Signin
curl -X POST http://localhost:8000/api/auth/signin \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"SecurePass123"}'

# Save token from response
TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

# List tasks
curl http://localhost:8000/api/{user_id}/tasks \
  -H "Authorization: Bearer $TOKEN"

# Create task
curl -X POST http://localhost:8000/api/{user_id}/tasks \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"Buy groceries","description":"Milk, eggs, bread"}'
```

---

## Deployment (Optional)

### Frontend Deployment (Vercel)

```bash
cd frontend

# Install Vercel CLI
npm install -g vercel

# Deploy
vercel

# Follow prompts to link project and deploy
```

### Backend Deployment (Railway/Render)

1. Create account on Railway or Render
2. Connect GitHub repository
3. Configure environment variables (DATABASE_URL, BETTER_AUTH_SECRET)
4. Deploy backend service
5. Update frontend NEXT_PUBLIC_API_URL to production backend URL

---

## Resources

### Documentation

- **Next.js**: https://nextjs.org/docs
- **FastAPI**: https://fastapi.tiangolo.com/
- **SQLModel**: https://sqlmodel.tiangolo.com/
- **Better Auth**: https://www.better-auth.com/docs
- **Neon**: https://neon.tech/docs

### Project Documentation

- **Specification**: `specs/002-fullstack-web-app/spec.md`
- **Implementation Plan**: `specs/002-fullstack-web-app/plan.md`
- **Data Model**: `specs/002-fullstack-web-app/data-model.md`
- **API Contracts**: `specs/002-fullstack-web-app/contracts/`
- **Research**: `specs/002-fullstack-web-app/research.md`

---

## Next Steps

1. ✅ Complete environment setup (this guide)
2. ⏭️ Run `/sp.tasks` to generate implementation tasks
3. ⏭️ Follow TDD workflow for each task
4. ⏭️ Create PHRs for all development sessions
5. ⏭️ Deploy to production (Vercel + Railway/Render)

---

## Support

If you encounter issues not covered in this guide:

1. Check the troubleshooting section above
2. Review the specification and plan documents
3. Check API contracts for endpoint details
4. Consult framework documentation (links above)
5. Create a PHR documenting the issue and resolution

**Happy coding! 🚀**
