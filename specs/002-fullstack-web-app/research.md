# Technical Research: Todo Full-Stack Web Application (Phase II)

**Feature**: 002-fullstack-web-app
**Date**: 2026-02-17
**Purpose**: Document technical decisions, rationale, and alternatives considered for Phase II implementation

## Research Summary

This document captures the technical research and decision-making process for transforming the Phase I console application into a full-stack web application with authentication, persistent storage, and responsive UI.

---

## Decision 1: Frontend Framework - Next.js 16+ with App Router

**Decision**: Use Next.js 16+ with App Router for the frontend

**Rationale**:
- **Hackathon Requirement**: Explicitly specified in Phase II requirements
- **Modern React**: Built on React 19+ with latest features (Server Components, Suspense)
- **App Router**: New routing paradigm with improved performance and developer experience
- **Built-in Optimization**: Automatic code splitting, image optimization, font optimization
- **Deployment**: Seamless deployment to Vercel (free tier available)
- **TypeScript Support**: First-class TypeScript integration
- **API Routes**: Can serve as BFF (Backend for Frontend) if needed

**Alternatives Considered**:
1. **Create React App (CRA)**
   - Rejected: Deprecated, no longer maintained, lacks modern features
2. **Vite + React**
   - Rejected: While excellent for SPAs, lacks Next.js's SSR, routing, and optimization features
3. **Remix**
   - Rejected: Not specified in hackathon requirements, smaller ecosystem

**Implementation Notes**:
- Use App Router (not Pages Router) for modern routing patterns
- Leverage Server Components for initial page loads
- Use Client Components for interactive UI (forms, modals)
- Implement route groups for authentication pages

---

## Decision 2: Backend Framework - FastAPI

**Decision**: Use FastAPI for the backend API

**Rationale**:
- **Hackathon Requirement**: Explicitly specified in Phase II requirements
- **Performance**: One of the fastest Python frameworks (async/await support)
- **Type Safety**: Built on Pydantic for automatic validation and serialization
- **OpenAPI**: Automatic API documentation generation
- **Modern Python**: Leverages Python 3.13+ features and type hints
- **Async Support**: Native async/await for database operations
- **Easy Testing**: Excellent testing support with pytest

**Alternatives Considered**:
1. **Django + Django REST Framework**
   - Rejected: Heavier framework, more boilerplate, not specified in requirements
2. **Flask**
   - Rejected: Older, synchronous by default, lacks automatic validation
3. **Node.js + Express**
   - Rejected: Would require JavaScript/TypeScript for backend, hackathon specifies Python

**Implementation Notes**:
- Use async route handlers for all endpoints
- Implement dependency injection for database sessions and auth
- Use Pydantic models for request/response validation
- Enable CORS for frontend-backend communication

---

## Decision 3: ORM - SQLModel

**Decision**: Use SQLModel for database ORM

**Rationale**:
- **Hackathon Requirement**: Explicitly specified in Phase II requirements
- **Type Safety**: Combines SQLAlchemy and Pydantic for full type safety
- **Single Model Definition**: One model serves as both ORM model and Pydantic schema
- **FastAPI Integration**: Designed to work seamlessly with FastAPI
- **Modern Python**: Leverages Python type hints
- **Async Support**: Works with async SQLAlchemy

**Alternatives Considered**:
1. **SQLAlchemy (direct)**
   - Rejected: More verbose, requires separate Pydantic models for validation
2. **Tortoise ORM**
   - Rejected: Less mature, smaller ecosystem, not specified in requirements
3. **Raw SQL**
   - Rejected: No type safety, manual validation, SQL injection risks

**Implementation Notes**:
- Define models with SQLModel (inherits from SQLAlchemy Base and Pydantic BaseModel)
- Use relationships for User-Task foreign key
- Implement async session management
- Use Alembic for database migrations

---

## Decision 4: Database - Neon Serverless PostgreSQL

**Decision**: Use Neon Serverless PostgreSQL for data storage

**Rationale**:
- **Hackathon Requirement**: Explicitly specified in Phase II requirements
- **Serverless**: Auto-scaling, pay-per-use pricing
- **Free Tier**: Generous free tier for hackathon development
- **PostgreSQL**: Full PostgreSQL compatibility (not a subset)
- **Branching**: Database branching for development/staging
- **Performance**: Fast cold starts, connection pooling built-in
- **Easy Setup**: Simple connection string, no server management

**Alternatives Considered**:
1. **Supabase**
   - Rejected: Not specified in requirements, includes features we don't need
2. **PlanetScale (MySQL)**
   - Rejected: MySQL not PostgreSQL, different SQL dialect
3. **Self-hosted PostgreSQL**
   - Rejected: Requires server management, no free hosting for hackathon

**Implementation Notes**:
- Use connection pooling (SQLAlchemy pool)
- Store connection string in environment variables
- Use async driver (asyncpg) for better performance
- Implement proper connection lifecycle management

---

## Decision 5: Authentication - Better Auth with JWT

**Decision**: Use Better Auth for authentication with JWT tokens

**Rationale**:
- **Hackathon Requirement**: Explicitly specified in Phase II requirements
- **Modern Auth**: TypeScript-first authentication library
- **JWT Support**: Built-in JWT token generation and validation
- **Next.js Integration**: Designed for Next.js App Router
- **Flexible**: Supports multiple auth strategies
- **Type Safe**: Full TypeScript support

**JWT Token Strategy**:
- **Stateless**: No server-side session storage required
- **Scalable**: Tokens can be verified by any backend instance
- **Shared Secret**: Frontend (Better Auth) and backend (FastAPI) use same secret
- **Token Expiry**: 7-day expiry with automatic refresh

**Alternatives Considered**:
1. **NextAuth.js**
   - Rejected: Better Auth is more modern, better TypeScript support
2. **Custom JWT Implementation**
   - Rejected: Reinventing the wheel, security risks
3. **Session-based Auth**
   - Rejected: Requires shared session store, less scalable

**Implementation Notes**:
- Configure Better Auth with JWT plugin in Next.js
- Store JWT in HTTP-only cookies (secure)
- Validate JWT on every FastAPI request (middleware)
- Use python-jose for JWT verification in backend
- Hash passwords with bcrypt (passlib)

---

## Decision 6: Styling - Tailwind CSS

**Decision**: Use Tailwind CSS for frontend styling

**Rationale**:
- **Utility-First**: Rapid UI development with utility classes
- **Responsive**: Built-in responsive design utilities
- **Customizable**: Easy to customize theme and colors
- **Performance**: Purges unused CSS in production
- **Next.js Integration**: Official Next.js support
- **No CSS-in-JS Runtime**: Zero runtime overhead

**Alternatives Considered**:
1. **CSS Modules**
   - Rejected: More verbose, requires separate CSS files
2. **Styled Components**
   - Rejected: Runtime overhead, not as performant
3. **Material-UI**
   - Rejected: Opinionated design, larger bundle size

**Implementation Notes**:
- Configure Tailwind in next.config.js
- Use Tailwind's responsive utilities (sm:, md:, lg:)
- Create reusable component classes with @apply
- Use Tailwind's dark mode support (optional)

---

## Decision 7: Monorepo Structure

**Decision**: Use monorepo with separate frontend/ and backend/ directories

**Rationale**:
- **Hackathon Requirement**: Explicitly specified in Phase II requirements
- **Clear Separation**: Frontend and backend are independent projects
- **Independent Deployment**: Can deploy frontend and backend separately
- **Technology Isolation**: Different package managers (npm vs UV)
- **Simplified Development**: Single repository for all code
- **Shared Documentation**: Specs and docs in one place

**Alternatives Considered**:
1. **Separate Repositories**
   - Rejected: More complex to manage, harder to keep in sync
2. **Monorepo with Shared Packages**
   - Rejected: Overkill for hackathon, adds complexity
3. **Backend as Next.js API Routes**
   - Rejected: Mixing Python and TypeScript in same project is problematic

**Implementation Notes**:
- Root-level README.md with setup instructions
- Separate package.json (frontend) and pyproject.toml (backend)
- Shared .env.example for environment variables
- Git ignores for both node_modules/ and .venv/

---

## Decision 8: API Design - RESTful

**Decision**: Use RESTful API design principles

**Rationale**:
- **Standard**: Industry-standard API design
- **HTTP Methods**: Clear semantics (GET, POST, PUT, DELETE, PATCH)
- **Stateless**: Each request contains all necessary information
- **Resource-Based**: URLs represent resources (tasks, users)
- **Status Codes**: Standard HTTP status codes for responses

**API Endpoint Structure**:
```
POST   /api/auth/signup          # Create account
POST   /api/auth/signin          # Sign in
POST   /api/auth/signout         # Sign out
GET    /api/{user_id}/tasks      # List all tasks
POST   /api/{user_id}/tasks      # Create task
GET    /api/{user_id}/tasks/{id} # Get task details
PUT    /api/{user_id}/tasks/{id} # Update task
DELETE /api/{user_id}/tasks/{id} # Delete task
PATCH  /api/{user_id}/tasks/{id}/complete # Toggle completion
```

**Alternatives Considered**:
1. **GraphQL**
   - Rejected: Overkill for simple CRUD operations, adds complexity
2. **gRPC**
   - Rejected: Not web-friendly, requires protobuf compilation
3. **JSON-RPC**
   - Rejected: Less standard, fewer tools and libraries

**Implementation Notes**:
- Use FastAPI's automatic OpenAPI documentation
- Return consistent JSON response format
- Use appropriate HTTP status codes (200, 201, 400, 401, 404, 500)
- Implement CORS middleware for cross-origin requests

---

## Decision 9: Testing Strategy

**Decision**: Implement comprehensive testing at multiple levels

**Frontend Testing**:
- **Unit Tests**: Jest + React Testing Library for components
- **Integration Tests**: Test user flows (optional: Playwright)

**Backend Testing**:
- **Unit Tests**: pytest for models, services, utilities
- **Integration Tests**: pytest with TestClient for API endpoints
- **Coverage Target**: 80% minimum (aligned with Phase I)

**Rationale**:
- **Quality Assurance**: Catch bugs early in development
- **Confidence**: Safe refactoring and feature additions
- **Documentation**: Tests serve as usage examples
- **Hackathon Requirement**: TDD approach required

**Implementation Notes**:
- Use pytest fixtures for database setup/teardown
- Mock external dependencies (database, auth)
- Test authentication and authorization logic thoroughly
- Test user isolation (users can't access other users' tasks)

---

## Decision 10: Development Workflow

**Decision**: Follow Spec-Driven Development with TDD

**Workflow**:
1. **Specify**: Create feature specification (spec.md) ✅ Complete
2. **Plan**: Generate implementation plan (plan.md) ✅ Complete
3. **Research**: Document technical decisions (research.md) ✅ Complete
4. **Design**: Create data model and API contracts (Phase 1)
5. **Tasks**: Break down into actionable tasks (tasks.md)
6. **Implement**: TDD cycle (Red → Green → Refactor)
7. **Document**: Create PHRs for all development sessions

**Rationale**:
- **Hackathon Requirement**: Spec-driven development mandatory
- **Traceability**: Every line of code maps to a task and spec
- **Quality**: TDD ensures correctness and test coverage
- **Documentation**: PHRs provide learning and audit trail

---

## Security Considerations

**Password Security**:
- Hash passwords with bcrypt (cost factor 12)
- Never store plaintext passwords
- Validate password strength on signup

**JWT Security**:
- Use strong secret key (256-bit minimum)
- Set reasonable expiry (7 days)
- Validate signature on every request
- Include user_id in token payload

**API Security**:
- Validate all inputs (Pydantic models)
- Sanitize user inputs to prevent XSS
- Use parameterized queries (SQLModel) to prevent SQL injection
- Implement rate limiting (optional for hackathon)

**User Isolation**:
- Filter all queries by authenticated user_id
- Verify user_id in URL matches JWT token user_id
- Return 403 Forbidden for unauthorized access attempts

---

## Performance Considerations

**Database**:
- Use connection pooling (SQLAlchemy)
- Index foreign keys (user_id in tasks table)
- Use async queries for better concurrency

**API**:
- Enable gzip compression
- Use async route handlers
- Implement pagination for task lists (if > 100 tasks)

**Frontend**:
- Use Next.js automatic code splitting
- Lazy load components where appropriate
- Optimize images with Next.js Image component
- Use React.memo for expensive components

---

## Deployment Strategy

**Frontend**:
- Deploy to Vercel (free tier)
- Automatic deployments from Git
- Environment variables for API URL

**Backend**:
- Deploy to cloud platform (Railway, Render, or DigitalOcean)
- Environment variables for database URL and JWT secret
- CORS configuration for frontend domain

**Database**:
- Neon Serverless PostgreSQL (already cloud-hosted)
- Connection string from Neon dashboard

---

## Summary

All technical decisions align with hackathon Phase II requirements and follow industry best practices. The chosen stack (Next.js + FastAPI + SQLModel + Neon + Better Auth) provides:

- **Type Safety**: TypeScript (frontend) and Python type hints (backend)
- **Performance**: Async operations, serverless database, optimized frontend
- **Developer Experience**: Modern tooling, automatic validation, great documentation
- **Scalability**: Stateless architecture, connection pooling, serverless database
- **Security**: JWT authentication, password hashing, input validation, user isolation

**Ready for Phase 1**: Design (data model, API contracts, quickstart guide)
