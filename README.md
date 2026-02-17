# Todo Full-Stack Web Application with AI Chat Assistant (Phase II + Phase III)

A modern, multi-user todo application built with Next.js 16+ and FastAPI, featuring JWT authentication, full CRUD operations, and an AI-powered chat assistant for natural language task management.

## 🚀 Features

### Phase II - Core Application
- **User Authentication**: Secure signup/signin with JWT tokens and bcrypt password hashing
- **Task Management**: Create, read, update, delete, and mark tasks as complete
- **User Isolation**: Each user can only access their own tasks
- **Responsive UI**: Clean, modern interface built with Tailwind CSS
- **Real-time Filtering**: View all tasks, active tasks, or completed tasks
- **Form Validation**: Client-side and server-side validation for data integrity
- **Error Handling**: Comprehensive error handling with user-friendly messages

### Phase III - AI Chat Assistant (NEW)
- **Conversational Task Management**: Create, view, update, mark complete, and delete tasks using natural language
- **OpenAI Integration**: Powered by GPT-4-turbo with function calling for intelligent task operations
- **Context-Aware Conversations**: Maintains conversation history with sliding window (15 messages)
- **Safety Features**: Delete confirmation to prevent accidental data loss
- **Session Management**: Automatic cleanup of inactive sessions (30-minute timeout)
- **Rate Limiting**: 20 requests per minute per user to prevent API abuse
- **Seamless Integration**: Chat interface toggles on/off in dashboard, works alongside traditional UI

## 📋 Tech Stack

### Frontend
- **Framework**: Next.js 16+ with App Router
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **State Management**: React Hooks
- **HTTP Client**: Fetch API with custom wrapper
- **AI Chat**: Custom React components with real-time messaging

### Backend
- **Framework**: FastAPI (Python 3.13+)
- **ORM**: SQLModel
- **Database**: Neon Serverless PostgreSQL
- **Authentication**: JWT tokens with python-jose
- **Password Hashing**: bcrypt via passlib
- **Migrations**: Alembic
- **AI Integration**: OpenAI Python SDK (GPT-4-turbo)
- **MCP Tools**: 6 custom tools for task operations

## 🛠️ Prerequisites

- **Node.js**: 18+ (for frontend)
- **Python**: 3.13+ (for backend)
- **UV**: Python package manager (install via `pip install uv`)
- **PostgreSQL**: Neon account or local PostgreSQL instance
- **OpenAI API Key**: Required for AI chat functionality (get from https://platform.openai.com)

## 📦 Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd hackathon2shzaib
```

### 2. Backend Setup

```bash
cd backend

# Install dependencies using UV
uv sync

# Create .env file
cp ../.env.example .env

# Edit .env and add your database URL and secret key
# DATABASE_URL=postgresql+asyncpg://user:password@host:5432/dbname
# SECRET_KEY=your-secret-key-here (generate with: openssl rand -hex 32)

# Run database migrations
uv run alembic upgrade head

# Start the backend server
uv run uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

The backend API will be available at `http://localhost:8000`
- API Documentation: `http://localhost:8000/docs`
- Alternative Docs: `http://localhost:8000/redoc`

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Create .env.local file
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local

# Start the development server
npm run dev
```

The frontend will be available at `http://localhost:3000`

## 🗄️ Database Schema

### Users Table
- `id` (UUID, Primary Key)
- `email` (String, Unique, Indexed)
- `hashed_password` (String)
- `created_at` (DateTime)

### Tasks Table
- `id` (UUID, Primary Key)
- `title` (String, Max 255 chars)
- `description` (String, Optional)
- `completed` (Boolean, Default: False)
- `user_id` (UUID, Foreign Key → users.id, Indexed)
- `created_at` (DateTime)
- `updated_at` (DateTime)

## 🔐 API Endpoints

### Authentication
- `POST /api/auth/signup` - Create new user account
- `POST /api/auth/signin` - Sign in and receive JWT token
- `POST /api/auth/signout` - Sign out (invalidate token)

### Tasks (All require JWT authentication)
- `GET /api/{user_id}/tasks` - List all tasks for user (optional `?completed=true/false` filter)
- `POST /api/{user_id}/tasks` - Create new task
- `GET /api/{user_id}/tasks/{task_id}` - Get specific task
- `PUT /api/{user_id}/tasks/{task_id}` - Update task
- `DELETE /api/{user_id}/tasks/{task_id}` - Delete task
- `PATCH /api/{user_id}/tasks/{task_id}/complete` - Toggle task completion

## 🧪 Testing

### Backend Tests

```bash
cd backend

# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=src --cov-report=html

# Run specific test file
uv run pytest tests/unit/test_user_model.py
```

### Frontend Tests

```bash
cd frontend

# Run all tests
npm test

# Run tests in watch mode
npm test -- --watch

# Run with coverage
npm test -- --coverage
```

## 🏗️ Project Structure

```
hackathon2shzaib/
├── backend/
│   ├── src/
│   │   ├── api/           # API endpoints
│   │   │   ├── auth.py    # Authentication routes
│   │   │   └── tasks.py   # Task CRUD routes
│   │   ├── core/          # Core utilities
│   │   │   ├── config.py  # Settings management
│   │   │   ├── database.py # Database connection
│   │   │   └── security.py # JWT & password hashing
│   │   ├── models/        # Data models
│   │   │   ├── user.py    # User model
│   │   │   └── task.py    # Task model
│   │   ├── services/      # Business logic
│   │   │   ├── auth_service.py
│   │   │   └── task_service.py
│   │   └── main.py        # FastAPI application
│   ├── tests/             # Test suite
│   │   ├── unit/          # Unit tests
│   │   └── integration/   # Integration tests
│   ├── alembic/           # Database migrations
│   └── pyproject.toml     # Python dependencies
│
├── frontend/
│   ├── src/
│   │   ├── app/           # Next.js App Router
│   │   │   ├── (auth)/    # Auth pages (signin, signup)
│   │   │   ├── dashboard/ # Dashboard page
│   │   │   └── layout.tsx # Root layout
│   │   ├── components/    # React components
│   │   │   ├── auth/      # Auth forms
│   │   │   ├── tasks/     # Task components
│   │   │   └── ui/        # Reusable UI components
│   │   └── lib/           # Utilities
│   │       ├── api.ts     # API client
│   │       └── auth.ts    # Auth utilities
│   ├── tests/             # Test suite
│   └── package.json       # Node dependencies
│
└── specs/                 # Design documents
    └── 002-fullstack-web-app/
        ├── spec.md        # Feature specification
        ├── plan.md        # Implementation plan
        └── tasks.md       # Task breakdown
```

## 🔒 Security Features

- **Password Hashing**: bcrypt with cost factor 12
- **JWT Tokens**: 7-day expiration, signed with HS256
- **User Isolation**: Database-level enforcement (user_id in queries)
- **Input Validation**: Pydantic schemas on backend, form validation on frontend
- **CORS**: Configured for frontend origin only
- **SQL Injection Protection**: SQLModel/SQLAlchemy parameterized queries

## 🚀 Deployment

### Frontend (Vercel)

1. Push code to GitHub
2. Import project in Vercel
3. Set environment variable: `NEXT_PUBLIC_API_URL=<your-backend-url>`
4. Deploy

### Backend (Railway/Render)

1. Create new project
2. Connect GitHub repository
3. Set environment variables:
   - `DATABASE_URL` (Neon PostgreSQL connection string)
   - `SECRET_KEY` (generate with `openssl rand -hex 32`)
   - `CORS_ORIGINS` (your frontend URL)
4. Set start command: `uvicorn src.main:app --host 0.0.0.0 --port $PORT`
5. Deploy

## 📝 Environment Variables

### Backend (.env)
```env
DATABASE_URL=postgresql+asyncpg://user:password@host:5432/dbname
SECRET_KEY=your-secret-key-here
CORS_ORIGINS=http://localhost:3000,https://your-frontend.vercel.app
```

### Frontend (.env.local)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 🤝 Contributing

This project follows Spec-Driven Development (SDD) with Claude Code and Spec-Kit Plus.

1. Create feature specification in `specs/`
2. Generate implementation plan
3. Break down into tasks
4. Implement with TDD approach (tests first)
5. Verify against acceptance criteria

## 📄 License

MIT License - See LICENSE file for details

## 🎯 Hackathon Submission

This project demonstrates:
- ✅ Full-stack development (Next.js + FastAPI)
- ✅ Modern authentication (JWT + bcrypt)
- ✅ RESTful API design
- ✅ Database design and migrations
- ✅ Comprehensive testing (unit + integration)
- ✅ Clean architecture and separation of concerns
- ✅ Responsive UI/UX
- ✅ Security best practices

## 📞 Support

For issues or questions, please open an issue on GitHub.
