# Quick Start Guide: Todo Console App (Phase I)

**Date**: 2026-02-17
**Feature**: 001-todo-console-app
**Phase**: 1 (Setup and Usage Guide)

## Overview

This guide provides step-by-step instructions for setting up, running, and testing the Phase I Todo Console App. Follow these instructions to get started quickly.

---

## Prerequisites

### Required Software

- **Python 3.13+**: Download from [python.org](https://www.python.org/downloads/)
- **UV Package Manager**: Install with:
  ```bash
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```
  Or on Windows:
  ```powershell
  powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
  ```

### Verify Installation

```bash
# Check Python version
python --version
# Expected: Python 3.13.0 or higher

# Check UV installation
uv --version
# Expected: uv 0.x.x or higher
```

---

## Project Setup

### 1. Clone Repository (if applicable)

```bash
git clone <repository-url>
cd hackathon2shzaib
git checkout 001-todo-console-app
```

### 2. Initialize Project with UV

```bash
# Create new Python project
uv init todo-console-app
cd todo-console-app

# Create Python version file
echo "3.13" > .python-version
```

### 3. Install Dependencies

```bash
# Install development dependencies
uv add --dev pytest pytest-cov ruff mypy

# Verify installation
uv pip list
```

### 4. Create Project Structure

```bash
# Create source directories
mkdir -p src/models src/services src/cli

# Create test directories
mkdir -p tests/unit tests/integration

# Create __init__.py files
touch src/__init__.py
touch src/models/__init__.py
touch src/services/__init__.py
touch src/cli/__init__.py
touch tests/__init__.py
touch tests/unit/__init__.py
touch tests/integration/__init__.py
```

---

## Development Workflow

### TDD Cycle (Red-Green-Refactor)

**Phase I follows strict TDD**. For each feature:

1. **Red**: Write failing tests first
   ```bash
   # Write test in tests/unit/test_task_model.py
   uv run pytest tests/unit/test_task_model.py
   # Expected: Tests fail (red)
   ```

2. **Green**: Implement minimal code to pass tests
   ```bash
   # Write code in src/models/task.py
   uv run pytest tests/unit/test_task_model.py
   # Expected: Tests pass (green)
   ```

3. **Refactor**: Improve code while keeping tests green
   ```bash
   # Refactor code
   uv run pytest tests/unit/test_task_model.py
   # Expected: Tests still pass (green)
   ```

### Running Tests

```bash
# Run all tests
uv run pytest

# Run specific test file
uv run pytest tests/unit/test_task_model.py

# Run with coverage report
uv run pytest --cov=src --cov-report=term-missing

# Run with verbose output
uv run pytest -v

# Run specific test function
uv run pytest tests/unit/test_task_model.py::test_task_creation
```

### Code Quality Checks

```bash
# Lint code with ruff
uv run ruff check src/ tests/

# Format code with ruff
uv run ruff format src/ tests/

# Type check with mypy
uv run mypy src/

# Run all quality checks
uv run ruff check src/ tests/ && \
uv run ruff format --check src/ tests/ && \
uv run mypy src/
```

---

## Running the Application

### Interactive Mode

```bash
# Run the todo app
uv run python -m src.main

# Or if installed as package
uv run todo
```

### Command-Line Mode

```bash
# Add a task
uv run python -m src.main add "Buy groceries" --description "Milk, eggs, bread"

# List all tasks
uv run python -m src.main list

# Mark task as complete
uv run python -m src.main complete 1

# Update task
uv run python -m src.main update 1 --title "Buy groceries and fruits"

# Delete task
uv run python -m src.main delete 1

# Show help
uv run python -m src.main help
```

---

## Usage Examples

### Example Session

```bash
# Start fresh
$ uv run python -m src.main list
No tasks found.

Use 'todo add <title>' to create your first task.

# Add first task
$ uv run python -m src.main add "Buy groceries" -d "Milk, eggs, bread"
✓ Task created successfully
  ID: 1
  Title: Buy groceries
  Description: Milk, eggs, bread
  Status: Incomplete
  Created: 2026-02-17 10:30:45

# Add more tasks
$ uv run python -m src.main add "Call mom"
✓ Task created successfully
  ID: 2
  Title: Call mom
  Description:
  Status: Incomplete
  Created: 2026-02-17 10:31:12

$ uv run python -m src.main add "Finish homework" -d "Math and science"
✓ Task created successfully
  ID: 3
  Title: Finish homework
  Description: Math and science
  Status: Incomplete
  Created: 2026-02-17 10:31:45

# List all tasks
$ uv run python -m src.main list
Your Tasks:

ID | Status | Title              | Description          | Created
---+--------+--------------------+----------------------+-------------------
1  | [ ]    | Buy groceries      | Milk, eggs, bread    | 2026-02-17 10:30
2  | [ ]    | Call mom           |                      | 2026-02-17 10:31
3  | [ ]    | Finish homework    | Math and science     | 2026-02-17 10:31

Total: 3 tasks (0 completed, 3 incomplete)

# Mark task as complete
$ uv run python -m src.main complete 2
✓ Task marked as complete
  ID: 2
  Title: Call mom
  Status: Complete

# List again to see status change
$ uv run python -m src.main list
Your Tasks:

ID | Status | Title              | Description          | Created
---+--------+--------------------+----------------------+-------------------
1  | [ ]    | Buy groceries      | Milk, eggs, bread    | 2026-02-17 10:30
2  | [✓]    | Call mom           |                      | 2026-02-17 10:31
3  | [ ]    | Finish homework    | Math and science     | 2026-02-17 10:31

Total: 3 tasks (1 completed, 2 incomplete)

# Update task
$ uv run python -m src.main update 1 -t "Buy groceries and fruits"
✓ Task updated successfully
  ID: 1
  Title: Buy groceries and fruits
  Description: Milk, eggs, bread
  Status: Incomplete

# Delete task
$ uv run python -m src.main delete 3
✓ Task deleted successfully
  ID: 3
  Title: Finish homework

# Final list
$ uv run python -m src.main list
Your Tasks:

ID | Status | Title                    | Description          | Created
---+--------+--------------------------+----------------------+-------------------
1  | [ ]    | Buy groceries and fruits | Milk, eggs, bread    | 2026-02-17 10:30
2  | [✓]    | Call mom                 |                      | 2026-02-17 10:31

Total: 2 tasks (1 completed, 1 incomplete)
```

---

## Troubleshooting

### Common Issues

#### Issue: `uv: command not found`

**Solution**: UV not installed or not in PATH
```bash
# Reinstall UV
curl -LsSf https://astral.sh/uv/install.sh | sh

# Add to PATH (Linux/Mac)
export PATH="$HOME/.cargo/bin:$PATH"

# Restart terminal
```

#### Issue: `Python 3.13 not found`

**Solution**: Install Python 3.13+
```bash
# Download from python.org
# Or use pyenv
pyenv install 3.13.0
pyenv local 3.13.0
```

#### Issue: `ModuleNotFoundError: No module named 'src'`

**Solution**: Run from project root
```bash
# Ensure you're in the project root
cd todo-console-app

# Run with python -m
uv run python -m src.main
```

#### Issue: Tests failing with import errors

**Solution**: Install project in editable mode
```bash
uv pip install -e .
```

#### Issue: Coverage below 80%

**Solution**: Add more tests
```bash
# Check coverage report
uv run pytest --cov=src --cov-report=html

# Open htmlcov/index.html to see uncovered lines
```

---

## Project Configuration

### pyproject.toml

```toml
[project]
name = "todo-console-app"
version = "0.1.0"
description = "Phase I Todo Console App - Hackathon Project"
requires-python = ">=3.13"
dependencies = []

[project.optional-dependencies]
dev = [
    "pytest>=8.0.0",
    "pytest-cov>=4.1.0",
    "ruff>=0.1.0",
    "mypy>=1.8.0",
]

[project.scripts]
todo = "src.main:main"

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = "--strict-markers --cov=src --cov-report=term-missing"

[tool.coverage.run]
source = ["src"]
omit = ["tests/*", "**/__pycache__/*"]

[tool.coverage.report]
fail_under = 80
show_missing = true

[tool.ruff]
line-length = 100
target-version = "py313"

[tool.ruff.lint]
select = ["E", "F", "I", "N", "W", "UP"]
ignore = []

[tool.mypy]
python_version = "3.13"
strict = true
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
```

---

## Development Tips

### Best Practices

1. **Always write tests first** (TDD is mandatory)
2. **Run tests frequently** (after every small change)
3. **Keep functions small** (<50 lines)
4. **Use type hints everywhere**
5. **Write descriptive docstrings**
6. **Commit often** (after each passing test)

### Keyboard Shortcuts

```bash
# Quick test run
alias t="uv run pytest"

# Quick test with coverage
alias tc="uv run pytest --cov=src --cov-report=term-missing"

# Quick lint
alias l="uv run ruff check src/ tests/"

# Quick format
alias f="uv run ruff format src/ tests/"

# All checks
alias check="uv run ruff check src/ tests/ && uv run mypy src/ && uv run pytest --cov=src"
```

### Git Workflow

```bash
# Create feature branch (already done)
git checkout 001-todo-console-app

# Commit after each passing test
git add .
git commit -m "test: add task model validation tests"

# Commit implementation
git add .
git commit -m "feat: implement task model with validation"

# Push to remote
git push origin 001-todo-console-app
```

---

## Next Steps

### After Phase I Completion

1. **Verify all tests pass**: `uv run pytest`
2. **Check coverage**: `uv run pytest --cov=src --cov-report=term-missing` (must be ≥80%)
3. **Run quality checks**: `uv run ruff check src/ tests/ && uv run mypy src/`
4. **Create demo video**: Record 90-second demo showing all 5 features
5. **Submit Phase I**: Use hackathon submission form

### Preparing for Phase II

Phase II will add:
- Web interface (Next.js frontend)
- REST API (FastAPI backend)
- Database persistence (Neon PostgreSQL)
- User authentication (Better Auth)

The service layer from Phase I will be reused in Phase II, so keep it clean and well-tested!

---

## Resources

### Documentation

- [Python 3.13 Docs](https://docs.python.org/3.13/)
- [UV Documentation](https://github.com/astral-sh/uv)
- [pytest Documentation](https://docs.pytest.org/)
- [ruff Documentation](https://docs.astral.sh/ruff/)

### Hackathon Resources

- [Hackathon Document](../../hackathon2doc.md)
- [Project Constitution](../../.specify/memory/constitution.md)
- [Feature Specification](./spec.md)
- [Implementation Plan](./plan.md)

### Getting Help

- Check [troubleshooting section](#troubleshooting) above
- Review [CLI command contracts](./contracts/cli-commands.md)
- Review [data model documentation](./data-model.md)
- Ask in hackathon Discord/Slack channel

---

## Summary

You're now ready to start implementing Phase I! Remember:

- ✅ Follow TDD strictly (Red-Green-Refactor)
- ✅ Write tests before code
- ✅ Achieve 80% coverage minimum
- ✅ Use type hints everywhere
- ✅ Keep it simple (YAGNI principle)
- ✅ Document all prompts in PHRs

**Next Command**: `/sp.tasks` to generate implementation tasks

Good luck! 🚀
