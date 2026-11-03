# AGENTS.md

This file provides guidance to Claude Code (claude.ai/code) or other AI agents or models when working with code in this repository.
This file is based on the CLAUDE.md file from the instructor repository.

# Instructor Development Guide

## Commands
- Install deps: `uv pip install -e ".[dev,anthropic]"`
- Run tests: `uv run pytest tests/ 
- Run specific test: `uv run pytest tests/path_to_test.py::test_name`
- Type check: `uv run ty check`
- Lint (if ruff is available): `uv run ruff check business_analytics examples tests`
- Format (not yet implemented): `uv run ruff format business_analytics examples tests`
- Generate coverage (not yet implemented): `uv run coverage run -m pytest tests/ -k "not docs"` then `uv run coverage report`
- Build documentation (not yet implemented): `uv run mkdocs serve` (for local preview)
- Waiting: use `sleep <seconds>` for explicit pauses (e.g., CI waits) or to let external processes finish

## Installation & Setup
- Fork the repository and clone your fork
- Install UV: `pip install uv`
- Create virtual environment: `uv venv`
- Install dependencies: `uv pip install -e ".[dev]"`
- Install pre-commit (not yet implemented): `uv run pre-commit install`
- Run tests to verify (once tests are implemented): `uv run pytest tests/

## Code Style Guidelines
- **Typing**: Use strict typing with annotations for all functions and variables
- **Imports**: Standard lib → third-party → local imports
- **Formatting**: Follow Black's formatting conventions, except for the 88-character line limit, as enforced by Ruff, if Ruff is available
- **Models**: Define structured outputs as Pydantic BaseModel subclasses
- **Naming**: snake_case for functions/variables, PascalCase for classes
- **Error Handling**: If exceptions.py exists, use custom exceptions found there and validate with Pydantic
- **Comments**: Docstrings for public functions, inline comments for complex logic

## Conventional Commits
- **Format**: `type(scope): description`
- **Types**: feat, fix, docs, style, refactor, perf, test, build, ci, chore, revert
- **Examples**:
  - `feat(anthropic): add support for Claude 3.5`
  - `fix(openai): correct response parsing for streaming`
  - `docs(README): update installation instructions`
  - `test(gemini): add validation tests for JSON mode`

## Core Architecture
- **Base Classes**: N/A
- **Factory Pattern**: Provider-specific factory functions (`from_openai`, `from_anthropic`, etc.) are planned (see "Provider Architecture")
- **Patching Mechanism**: Uses Python's dynamic nature to patch provider clients for structured outputs
- **Response Processing**: Transforms raw API responses into validated Pydantic models

## Provider Architecture
- **Supported Providers**: OpenAI is the LLM provider used at the moment, but support for Anthropic and Gemini is planned.
- **Provider Implementation**: Each provider will have a dedicated client file with factory functions
- **Common Pattern**: Factory functions (e.g., `from_anthropic`) will take a native client and return patched client instances
- **Provider Testing**: Test_llm.py defines Pydantic models, makes API calls, verifies structured outputs using a particular llm.

## Key Components
--**main.py**: Main entrypoint, CLI
- **client.py**: Contains the provider-specific factory function
- **validators.py**: Custom validation mechanisms for structured outputs

## Testing Guidelines
- `business_analytics/tests/` contains tests
- Each provider supported has its own test file (test_openai.py, test_anthropic.py for planned Claude support)
- Standard tests cover: basic extraction, validation, evaluation, retries
- Evaluation tests in `assess model capabilities
- Use parametrized tests when testing similar functionality across variants
- **IMPORTANT**: No mocking in tests - tests make real API calls

## Documentation Guidelines
- Every provider needs documentation
- Example code should include complete imports and environment setup
- Tutorials should progress from simple to complex concepts
- New features should include conceptual explanation in `docs/concepts/`
- **Writing Style**: Grade 10 reading level, all examples must be working code

## Branch and Development Workflow
1. Fork and clone the repository
2. Create feature branch: `git checkout -b feat/your-feature`
3. Make changes and add tests
4. Run tests and linting
5. Commit with conventional commit message
6. Push to your fork and create PR
7. Use stacked PRs for complex features


## Contributing to Evals
- Standard evals for each provider test model capabilities
- Create new evals following existing patterns
- Run evals as part of integration test suite
- Performance tracking and comparison

## Pull Request Guidelines
- Keep PRs small and focused
- Include tests for all changes
- Update documentation as needed
- Follow PR template
- Link to relevant issues
- **Update CHANGELOG.md**: Every PR that changes behavior (fix, feat, security, deprecation) should add an entry under the current `[Unreleased]` section in `CHANGELOG.md`. Format: `- **Area**: Description ([#PR](url))`

## Type System and Best Practices

### Type Checking with ty
- **Type Checker**: Using `ty` if available for fast, incremental type checking
- **Python Version**: 3.9+ for compatibility
- **Configuration**: Use `pyproject.toml` settings for type checking if available
- Run `uv run ty check` before committing - aim for zero errors

### Code Quality Checks Before Committing
Always run these checks before committing code (if ruff and ty are available):
1. **Ruff linting**: `uv run ruff check .` - Fix all errors
2. **Ruff formatting**: `uv run ruff format .` - Apply consistent formatting
3. **Type checking**: `uv run ty check` - Aim for zero type errors
4. **Tests**: Run relevant tests to ensure changes don't break functionality

### Type Patterns
- **Bounded TypeVars**: Use `T = TypeVar("T", bound=Union[BaseModel, ...])` for constraints
- **Version Compatibility**: Handle Python 3.9 vs 3.10+ typing differences explicitly
- **Union Type Syntax**: Use `from __future__ import annotations` to enable Python 3.10+ union syntax (`|`) in Python 3.9
- **Simple Type Detection**: Special handling for `list[Union[int, str]]` patterns
- **Runtime Type Handling**: Graceful fallbacks for compatibility

### Pydantic Integration
- Consistent use of `BaseModel` for structured outputs
- Field validators and custom types
- Models serve dual purpose: validation and documentation

## Building Documentation

### Setup
- Not yet implemented
```bash
# Install documentation dependencies
pip install -r requirements-doc.txt
```

### Local Development
- Not yet implemented
```bash
# Serve documentation locally with hot reload
uv run mkdocs serve

# Build documentation for production
./build_mkdocs.sh
```

### Documentation Features
- Not yet implemented

### Writing Documentation
- Not yet implemented

## Project Structure
- `instructor/` - Core library code
  - Base classes, CLI, and core logic in in main.py
  - Provider clients (`client.py`): Factory functions for each provider (currently just openai)
  - Gui.py for future GUI implementation
- `tests/` - Test suite organized by provider
  - Provider-specific tests in test_provider.py
  - Evaluation tests for model capabilities
  - No mocking - all tests use real API calls
- `docs/` - MkDocs documentation
  - Core conceptsintegrations (provider-specific guides--once multiple providers are supported), practical examples/
  - `integrations/` - Provider-specific guide
  - `examples/` - Practical examples and cookbooks
- `examples/` - Runnable code examples
  - Feature demos: TBA
  - Use cases: extraction, knowledge graphs once implemented, etc.
  - Provider examples: openai, anthropic and gemini once supported
  - Each example has `run.py` as the main entry point

## Documentation Structure
- Not yet implemented

## Example Patterns
When creating examples:
- Use `run.py` as the main file name (if run.py exists)
- Include clear imports: stdlib → third-party → local
- Define Pydantic models with descriptive fields
- Show expected output in comments
- Handle errors appropriately
- Make examples self-contained and runnable

## Dependency Management

### Core Dependencies
- **Minimal core**: `openai`, `anthropic`, `pydantic`, `docstring-parser`, 
- **Python requirement**: `<4.0,>=3.9`
- **Pydantic version**: `<3.0.0,>=2.8.0` (constrained for stability)

### Optional Dependencies
N/A

### Development Dependencies
```bash
# Install all development dependencies
uv pip install -e ".[dev]"
```
Includes:
- `ty` 
- `pytest` and `pytest-asyncio` - Testing
- `ruff` - Linting and formatting
- `coverage` - Test coverage
- `mkdocs` and plugins - Documentation

### Version Constraints
- **Create Upper bounds on all dependencies** for stability
- **Provider SDK versions** pinned to tested versions
- **Test dependencies** include evaluation frameworks

### Managing Dependencies
- Update `pyproject.toml` for new dependencies
- Test with multiple Python versions (3.9-3.15)
- Run full test suite after dependency updates
- Document any provider-specific version requirements

The library enables structured LLM outputs using Pydantic models across multiple providers with type safety.