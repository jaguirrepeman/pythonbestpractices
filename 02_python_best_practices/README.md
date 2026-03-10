# Module 2 — Python Best Practices

> **Date:** 2026-03-10  
> **Audience:** All developers  
> **Deliverables:** Poetry quick-start scripts, pre-commit configuration, project structure template, best practices documentation

---

## Table of Contents

| Section | Title |
|---------|-------|
| [2.1](#21--poetry--dependency-management) | Poetry & Dependency Management |
| [2.2](#22--code-quality-toolchain) | Code Quality Toolchain (ruff, pre-commit) |
| [2.3](#23--python-language-standards) | Python Language Standards |
| [2.4](#24--project-structure) | Project Structure (`src/` layout) |
| [2.5](#25--git-workflow--branching-strategy) | Git Workflow & Branching Strategy |
| [2.6](#26--code-design-principles) | Code Design Principles |
| [2.7](#27--packaging--snowflake-deployment) | Packaging & Snowflake Deployment |

---

## 2.1 — Poetry & Dependency Management

[Poetry](https://python-poetry.org/) is the standard tool for dependency management, virtual environment isolation, and package building.

### Quick-Start Script

Copy `templates/poetry_quickstart.sh` to bootstrap any new project:

```bash
#!/bin/bash
set -euo pipefail

PROJECT_NAME="${1:?Usage: ./poetry_quickstart.sh <project-name>}"

# Create project with src/ layout
mkdir -p "${PROJECT_NAME}/src/${PROJECT_NAME}"
cd "${PROJECT_NAME}"

# Initialize poetry
poetry init --name "${PROJECT_NAME}" \
            --python "^3.11" \
            --no-interaction

# Create virtual environment
python -m venv .venv
source .venv/bin/activate
pip install poetry

# Add core dev dependencies
poetry add --group dev pytest pytest-cov ruff mypy pre-commit

# Create essential files
touch src/${PROJECT_NAME}/__init__.py
touch src/${PROJECT_NAME}/py.typed
echo ".venv/" > .gitignore
echo "__pycache__/" >> .gitignore
echo "dist/" >> .gitignore
echo ".env" >> .gitignore

echo "✅ Project '${PROJECT_NAME}' created. Run: cd ${PROJECT_NAME} && poetry install"
```

### Day-to-Day Commands

```bash
# Install all dependencies from lock file (deterministic)
poetry install

# Add a dependency
poetry add pandas
poetry add --group dev pytest-mock

# Update a specific package
poetry update pandas

# Show dependency tree
poetry show --tree

# Build distributable package
poetry build

# Lock without installing (useful in CI)
poetry lock --no-update
```

### Lock File Policy

| Rule | Details |
|------|---------|
| **Always commit** `poetry.lock` | Guarantees identical environments for everyone |
| **Pin direct dependencies** | Use `^` (compatible) or `~` (patch-only) constraints |
| **Lock file = source of truth** | `poetry install` reads the lock, not `pyproject.toml` |
| **Automated updates** | Configure Dependabot / Renovate for weekly dependency PRs |
| **CI caching** | Cache `.venv/` keyed on `poetry.lock` hash |

### Poetry + venv Integration

Poetry can use an existing venv instead of creating its own:

```bash
# Tell Poetry to use the .venv in the project
poetry config virtualenvs.in-project true

# Or use an existing venv
source .venv/bin/activate
poetry install  # installs into the active venv
```

---

## 2.2 — Code Quality Toolchain

### Pre-commit Hooks

The team uses `pre-commit` to enforce code quality checks before every commit. The configuration includes:

| Hook | Purpose |
|------|---------|
| **ruff** | Python linting + formatting (replaces black, isort, flake8) |
| **sqlfluff** | SQL linting (for dbt and raw SQL files) |
| **nb-clean** | Strip notebook outputs, metadata, execution counts |
| **trailing-whitespace** | Remove trailing spaces |
| **end-of-file-fixer** | Ensure files end with newline |
| **check-yaml** | Validate YAML syntax |
| **check-added-large-files** | Prevent accidental commits of large files |
| **check-merge-conflict** | Detect merge conflict markers |

### `.pre-commit-config.yaml`

```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.6.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
        args: ['--maxkb=1000']
      - id: check-merge-conflict

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.4.4
    hooks:
      - id: ruff
        args: ['--fix']
      - id: ruff-format

  - repo: https://github.com/sqlfluff/sqlfluff
    rev: 3.0.0
    hooks:
      - id: sqlfluff-lint
        args: ['--dialect', 'snowflake']
      - id: sqlfluff-fix
        args: ['--dialect', 'snowflake']

  - repo: https://github.com/srstevenson/nb-clean
    rev: "3.3.0"
    hooks:
      - id: nb-clean
        args: ['--remove-empty-cells', '--preserve-cell-metadata', 'tags']

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.10.0
    hooks:
      - id: mypy
        additional_dependencies: [types-requests]
```

### Installation

```bash
# Install pre-commit
pip install pre-commit

# Install hooks for this repo (reads .pre-commit-config.yaml)
pre-commit install

# Run against all files (first time / CI)
pre-commit run --all-files
```

### Ruff Configuration (`pyproject.toml`)

```toml
[tool.ruff]
line-length = 120
target-version = "py311"

[tool.ruff.lint]
select = ["E", "F", "W", "I", "N", "UP", "S", "B", "A", "C4", "DTZ", "T20", "PT"]

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
```

### sqlfluff Configuration (`.sqlfluff`)

```ini
[sqlfluff]
dialect = snowflake
templater = jinja
max_line_length = 120

[sqlfluff:rules:capitalisation.keywords]
capitalisation_policy = upper

[sqlfluff:rules:capitalisation.identifiers]
capitalisation_policy = lower
```

---

## 2.3 — Python Language Standards

| Area | Standard |
|------|----------|
| Python version | **≥ 3.10** (preferably 3.11+) |
| Style guide | **PEP 8** enforced via `ruff` |
| Type hints | Mandatory on all public function signatures (PEP 484 / 604) |
| Naming | `snake_case` functions/variables, `PascalCase` classes, `UPPER_CASE` constants |
| Encoding | UTF-8 everywhere |
| Line length | 120 characters max |
| Imports | Grouped: stdlib → third-party → local (managed by `ruff` with `isort` rules) |

### Type Hints

```python
# ✅ Modern Python 3.10+ style
def calculate_metric(data: list[float], threshold: float | None = None) -> dict[str, float]:
    ...

# ❌ Legacy style — do not use
from typing import List, Dict, Optional
def calculate_metric(data: List[float], threshold: Optional[float] = None) -> Dict[str, float]:
    ...
```

### Common Pitfalls

```python
# ❌ Mutable default argument
def process(items: list[str] = []):
    items.append("x")  # mutates the shared default!
    return items

# ✅ Correct
def process(items: list[str] | None = None):
    items = items or []
    items.append("x")
    return items
```

---

## 2.4 — Project Structure

Every deliverable follows the `src/` layout with `pyproject.toml`:

```
my_project/
├── .github/
│   ├── workflows/
│   │   └── ci.yml
│   ├── copilot-instructions.md
│   └── pull_request_template.md
├── .vscode/
│   └── settings.json
├── src/
│   └── my_project/
│       ├── __init__.py
│       ├── py.typed
│       ├── core/
│       ├── data/
│       ├── features/
│       └── utils/
├── tests/
│   ├── conftest.py
│   ├── unit/
│   └── integration/
├── notebooks/
├── scripts/
├── docs/
├── .pre-commit-config.yaml
├── .gitignore
├── .python-version
├── .env.example
├── pyproject.toml
├── poetry.lock
├── README.md
└── CHANGELOG.md
```

### Key Principles

| Principle | Rule |
|-----------|------|
| **`src/` layout** | Code always under `src/package_name/` — prevents accidental local imports |
| **Single responsibility** | Each module (.py) has one clear purpose |
| **Layer separation** | `core`, `data`, `api`, `config`, `utils` are independent layers |
| **Tests mirror src** | `tests/unit/test_engine.py` tests `src/my_project/core/engine.py` |
| **Notebooks separate** | Notebooks in `notebooks/`, never in `src/` |
| **No circular imports** | Dependencies flow: `api` → `core` → `data` → `utils` |

---

## 2.5 — Git Workflow & Branching Strategy

### Branch Structure

```
main (production) ← requires PR review before merge
  └── qa (staging)
       └── dev (development)
```

All work flows: **branch from dev → merge to dev → merge to qa → merge to main**.

### Branch Naming

| Type | Convention | Example |
|------|-----------|---------|
| **Issue-linked** (preferred) | `issue/<number>-<description>` | `issue/126-sequence-table` |
| **Feature** | `feature/<description>` | `feature/add-snowflake-loader` |
| **Bug fix** | `fix/<description>` | `fix/null-handling-pipeline` |
| **Refactor** | `refactor/<description>` | `refactor/extract-validation` |
| **Chore** | `chore/<description>` | `chore/update-dependencies` |

- **Issue tracking:** Use GitHub Projects for ticket and epic management. Each ticket gets its own branch using the `issue/` prefix.
- **Branch names are always lowercase** with hyphens, never underscores or spaces.

### Commit Messages

Write **descriptive commits** that explain *what* and *why*:

```
# ✅ Good
feat: add Snowflake stage upload to CI pipeline

Adds a deployment step that uploads .whl files to @python_packages
stage after tagging a release. Closes #142.

# ❌ Bad
fixed stuff
update
wip
```

Recommended format: [Conventional Commits](https://www.conventionalcommits.org/) — `type: description`.

| Type | When |
|------|------|
| `feat` | New feature |
| `fix` | Bug fix |
| `refactor` | Code restructuring (no behavior change) |
| `docs` | Documentation only |
| `test` | Adding or modifying tests |
| `chore` | Tooling, config, dependencies |
| `ci` | CI/CD pipeline changes |

### Pull Requests

- **Always create a PR** for merging into dev/qa/main.
- **main requires review** before merge.
- **Use the PR template** (see `templates/.github/pull_request_template.md`).
- **PRs should be small and focused** — one logical change per PR.
- **Write descriptive PR titles and descriptions** — explain the context and impact.

---

## 2.6 — Code Design Principles

### Functions

| Principle | Rule |
|-----------|------|
| **Small and focused** | Max ~30 lines. Split if longer. |
| **One level of abstraction** | Don't mix high-level logic with low-level details |
| **No hidden side effects** | If there's a side effect, make it explicit in the name/docstring |
| **Fail early** | Validate inputs at the top with clear exceptions |
| **Immutable defaults** | Never `def f(x=[])` — use `def f(x: list | None = None)` |

### Classes

| Principle | Rule |
|-----------|------|
| **SRP** | One class, one responsibility |
| **Composition > Inheritance** | Inject dependencies, don't inherit |
| **Dataclasses** | Use `@dataclass` for DTOs, configs, value objects |
| **ABC** | Use `abc.ABC` for interfaces and contracts |
| **Immutability** | `@dataclass(frozen=True)` when possible |

### Examples

```python
# ✅ Pure function — no side effects, deterministic
def calculate_discount(price: float, discount_rate: float) -> float:
    """Calculate the discounted price."""
    if price < 0:
        raise ValueError(f"Price must be non-negative, got {price}")
    if not 0 <= discount_rate <= 1:
        raise ValueError(f"Discount rate must be in [0, 1], got {discount_rate}")
    return round(price * (1 - discount_rate), 2)


# ✅ Immutable value object
from dataclasses import dataclass

@dataclass(frozen=True)
class ForecastResult:
    date: str
    predicted_value: float
    lower_bound: float
    upper_bound: float
```

---

## 2.7 — Packaging & Snowflake Deployment

This section covers the full lifecycle: building packages, managing a shared dependency registry, and deploying to Snowflake stages.

For the detailed explanation, templates, and CI/CD pipeline configs, see the **[packaging guide](packaging_guide.md)**.

### Quick Reference

```bash
# Build
poetry build  # → dist/my_project-1.0.0-py3-none-any.whl

# Upload to Snowflake stage
# PUT file://dist/my_project-1.0.0-py3-none-any.whl @my_db.my_schema.python_packages/ AUTO_COMPRESS=FALSE;

# Use in Snowpark stored procedure
# packages=["pandas==2.1.0"]   ← Anaconda channel
# imports=["@stage/my_project-1.0.0-py3-none-any.whl"]  ← custom package
```

---

## Deliverables Summary

| ID | Deliverable | Location |
|----|------------|----------|
| **D1** | Poetry quick-start script | `templates/poetry_quickstart.sh` |
| **D2** | `.pre-commit-config.yaml` | `templates/.pre-commit-config.yaml` |
| **D3** | `pyproject.toml` template | `templates/pyproject.toml` |
| **D4** | `.vscode/settings.json` | `templates/.vscode/settings.json` |
| **D5** | Project structure template | `templates/project_structure/` |
| **D6** | PR template | `templates/.github/pull_request_template.md` |
| **D7** | Packaging & Snowflake guide | [`packaging_guide.md`](packaging_guide.md) |
| **D8** | `.sqlfluff` config | `templates/.sqlfluff` |
| **D9** | `.gitignore` template | `templates/.gitignore` |

---

**Previous ←** [01_dev_env_setup/](../01_dev_env_setup/) — Dev environment, pyenv, venv, VS Code, Docker  
**Next →** [03_documentation/](../03_documentation/) — Sphinx, GitHub Pages, GitHub Wiki
