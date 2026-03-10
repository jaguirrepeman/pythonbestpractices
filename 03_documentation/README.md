# Module 3 — Documentation

> **Date:** 2026-03-10  
> **Audience:** All developers  
> **Deliverables:** Sphinx pipeline, GitHub Pages deployment, GitHub Wiki setup, docstring standards, documentation governance checklist

---

## Table of Contents

| Section | Title |
|---------|-------|
| [3.1](#31--docstring-standards) | Docstring Standards |
| [3.2](#32--sphinx-documentation-pipeline) | Sphinx Documentation Pipeline |
| [3.3](#33--deploy-to-github-pages) | Deploy to GitHub Pages |
| [3.4](#34--github-wiki) | GitHub Wiki |
| [3.5](#35--documentation-governance) | Documentation Governance |
| [3.6](#36--data-documentation) | Data Documentation |

---

## 3.1 — Docstring Standards

All projects use **Google Style** docstrings (enforced by `ruff` rule `D` and parsed by Sphinx via the Napoleon extension).

### Function Docstring

```python
def load_dataset(
    path: str,
    columns: list[str] | None = None,
    sample_frac: float = 1.0,
) -> pd.DataFrame:
    """Load a Parquet dataset from the given path.

    Reads the file using PyArrow and optionally selects a subset of
    columns and/or random sample of rows.

    Args:
        path: Absolute or relative path to the Parquet file.
        columns: Columns to keep. ``None`` keeps all columns.
        sample_frac: Fraction of rows to sample (0.0–1.0).

    Returns:
        A DataFrame with the requested columns and sample.

    Raises:
        FileNotFoundError: If ``path`` does not exist.
        ValueError: If ``sample_frac`` is not in (0, 1].

    Example:
        >>> df = load_dataset("data/sales.parquet", columns=["date", "revenue"])
        >>> df.head()
    """
```

### Class Docstring

```python
class SnowflakeConnector:
    """Manage connections and queries to a Snowflake warehouse.

    Wraps ``snowflake.connector`` and provides context-manager support
    for automatic connection cleanup.

    Attributes:
        account: Snowflake account identifier.
        warehouse: Default compute warehouse name.

    Example:
        >>> with SnowflakeConnector(account="xy12345") as conn:
        ...     result = conn.execute("SELECT 1")
    """
```

### Rules

| Rule | Details |
|------|---------|
| Mandatory on all public functions, classes, modules | Private helpers (`_func`) recommended but not required |
| Use `Args`, `Returns`, `Raises`, `Example` sections | In that order |
| One-line summary on the first line | Present tense, imperative mood ("Load", not "Loads") |
| No redundant type info in docstrings | Types belong in signatures, not in `Args:` descriptions |
| Use `autoDocstring` VS Code extension | Generates a skeleton from the function signature |

---

## 3.2 — Sphinx Documentation Pipeline

[Sphinx](https://www.sphinx-doc.org/) builds HTML documentation from your docstrings and reStructuredText/Markdown source files. This replaces MkDocs for projects that need automatic API reference generation from source code.

### Initial Setup

```bash
# Install Sphinx and extensions
poetry add --group dev sphinx sphinx-autodoc-typehints sphinx-rtd-theme myst-parser

# Create docs scaffolding
mkdir docs
cd docs
sphinx-quickstart --sep --project "My Project" --author "Team" --release "1.0.0" --language en
```

This creates:

```
docs/
├── build/          # generated HTML (git-ignored)
├── source/
│   ├── conf.py     # Sphinx configuration
│   ├── index.rst   # root document
│   ├── _static/
│   └── _templates/
├── Makefile
└── make.bat
```

### `conf.py` Configuration

```python
# docs/source/conf.py

project = "My Project"
author = "Team"
release = "1.0.0"

extensions = [
    "sphinx.ext.autodoc",           # pull docstrings from source
    "sphinx.ext.napoleon",          # Google-style docstring parsing
    "sphinx_autodoc_typehints",     # render type hints in docs
    "sphinx.ext.viewcode",          # [source] links in HTML
    "sphinx.ext.intersphinx",       # cross-reference external docs
    "myst_parser",                  # Markdown support (.md files alongside .rst)
]

# Napoleon settings (Google style)
napoleon_google_docstring = True
napoleon_numpy_docstring = False
napoleon_include_init_with_doc = True

# Type hints
autodoc_typehints = "description"
always_document_param_types = True

# Theme
html_theme = "sphinx_rtd_theme"

# Intersphinx targets
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "pandas": ("https://pandas.pydata.org/docs/", None),
}

# Source parsers
source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}
```

### Auto-generate API Reference

```bash
# Generate .rst stubs from your src/ package
sphinx-apidoc -o docs/source/api src/my_project --separate --force

# Build HTML
cd docs
make html   # output → docs/build/html/index.html
```

### `docs/source/index.rst`

```rst
My Project Documentation
========================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   getting_started
   user_guide
   api/modules
   changelog
```

### Adding a Manual Page

Create `docs/source/getting_started.md` (Markdown support via `myst_parser`):

```markdown
# Getting Started

## Installation

\```bash
poetry install
\```

## Quick Start

\```python
from my_project.core import Engine

engine = Engine()
result = engine.run(data)
\```
```

### Build Locally

```bash
cd docs
make html        # full build
make clean html  # clean rebuild

# Preview
python -m http.server -d build/html 8080
# Open http://localhost:8080
```

---

## 3.3 — Deploy to GitHub Pages

Automate documentation builds on every push to `main` and publish to GitHub Pages.

### GitHub Actions Workflow

```yaml
# .github/workflows/docs.yml
name: Build & Deploy Docs

on:
  push:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: "pages"
  cancel-in-progress: false

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install dependencies
        run: |
          pip install poetry
          poetry install --with dev

      - name: Build Sphinx docs
        run: |
          cd docs
          poetry run make html

      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: docs/build/html

  deploy:
    needs: build
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

### Enable GitHub Pages

1. Go to **Settings → Pages** in your GitHub repository.
2. Under **Build and deployment**, select **GitHub Actions** as the source.
3. Push to `main` — the workflow above builds Sphinx and deploys automatically.
4. Your docs are live at `https://<org>.github.io/<repo>/`.

---

## 3.4 — GitHub Wiki

Use the GitHub Wiki for **non-code documentation** that doesn't belong in Sphinx: onboarding guides, architecture decisions, team conventions, meeting notes.

### Wiki Structure

| Page | Content |
|------|---------|
| **Home** | Index with links to all pages |
| **Architecture** | System diagrams, data flows, infrastructure overview |
| **Onboarding** | New team member checklist (environment setup, access requests, key contacts) |
| **ADRs** | Architecture Decision Records (one per significant decision) |
| **Runbooks** | Step-by-step procedures for common operations (deployments, rollbacks, incident response) |
| **Glossary** | Domain-specific terms and abbreviations |

### ADR Template (Architecture Decision Record)

```markdown
# ADR-001: Use Snowflake for Data Warehousing

**Status:** Accepted  
**Date:** 2026-01-15  
**Author:** @jaguirrepeman

## Context
The team needs a cloud data warehouse that supports Python UDFs for ML inference.

## Decision
Adopt Snowflake with Snowpark for Python-based transformations.

## Consequences
- (+) Native Python UDF support, scalable compute
- (-) Vendor lock-in, Snowflake-specific SQL dialects
```

### Wiki Best Practices

- **Use the sidebar** (`_Sidebar.md`) to add persistent navigation.
- **Keep pages focused** — one topic per page.
- **Link to code docs** — reference the Sphinx-built pages for API details.
- **Version decisions** — date all ADRs and significant changes.

---

## 3.5 — Documentation Governance

Documentation degrades unless actively maintained. These processes keep docs current.

### Ownership

| Artifact | Owner | Review cadence |
|----------|-------|----------------|
| API reference (Sphinx) | Auto-generated from code | Every push (CI) |
| User guide pages | Feature owner | Updated with each feature PR |
| Architecture wiki | Tech lead | Quarterly review |
| ADRs | Author | Immutable after acceptance |
| README.md | Whole team | Updated when scope changes |
| CHANGELOG.md | PR author | Updated with each PR |

### PR Checklist (Documentation)

Include this in your PR template:

```markdown
## Documentation
- [ ] Public functions/classes have Google-style docstrings
- [ ] API changes are reflected in Sphinx source files
- [ ] README updated if scope or usage changed
- [ ] CHANGELOG updated with user-facing changes
- [ ] Wiki updated if architecture or processes changed
```

### CHANGELOG.md Format

Follow [Keep a Changelog](https://keepachangelog.com/):

```markdown
# Changelog

## [1.2.0] - 2026-03-10
### Added
- Snowflake stage deployment in CI pipeline

### Changed
- Migrated formatter from black to ruff

### Fixed
- Null handling in `transform_features()` pipeline
```

### CODEOWNERS

Define ownership at the file/directory level:

```
# .github/CODEOWNERS

# Default
*                   @team-leads

# Core pipeline
src/my_project/core/   @pipeline-team
src/my_project/data/   @data-team

# Documentation
docs/                  @tech-lead
```

---

## 3.6 — Data Documentation

For data-heavy projects (dbt models, ML pipelines), maintain documentation that describes:

| Document | Format | Purpose |
|----------|--------|---------|
| **Data dictionary** | Markdown / Wiki table | Column names, types, descriptions, units, valid ranges |
| **Lineage diagram** | Excalidraw / Mermaid | Where data comes from, how it transforms, where it goes |
| **dbt docs** | `dbt docs generate` | Model descriptions, tests, lineage (auto-generated) |
| **Schema contracts** | `pyproject.toml` / JSON Schema | Validate data at ingestion boundaries |

### Data Dictionary Example

```markdown
## Table: `dim_customer`

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| customer_id | VARCHAR(36) | UUID primary key | `a1b2c3d4-...` |
| email | VARCHAR(255) | Verified email address | `user@example.com` |
| segment | VARCHAR(20) | Marketing segment (A/B/C) | `A` |
| created_at | TIMESTAMP_NTZ | Account creation date (UTC) | `2026-01-15T10:30:00` |
```

---

## Deliverables Summary

| ID | Deliverable | Location |
|----|------------|----------|
| **D1** | Sphinx `conf.py` template | `templates/docs/source/conf.py` |
| **D2** | Sphinx `index.rst` template | `templates/docs/source/index.rst` |
| **D3** | GitHub Pages workflow | `templates/.github/workflows/docs.yml` |
| **D4** | Docstring examples | `templates/docstring_examples.py` |
| **D5** | `CHANGELOG.md` template | `templates/CHANGELOG.md` |
| **D6** | `CODEOWNERS` template | `templates/.github/CODEOWNERS` |
| **D7** | Documentation governance checklist | `templates/doc_governance_checklist.md` |
| **D8** | Data dictionary template | `templates/data_documentation_template.md` |
| **D9** | ADR template | `templates/adr_template.md` |

---

**Previous ←** [02_python_best_practices/](../02_python_best_practices/) — Code quality, Poetry, Git workflow  
**Next →** [04_testing/](../04_testing/) — Testing strategy & pytest
