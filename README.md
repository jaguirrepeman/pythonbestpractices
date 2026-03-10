# Python Best Practices — Repository Index

> **Date:** 2026-03-10  
> **Audience:** Data Science / Analytics / Engineering Teams  
> **Stack:** pyenv · Poetry · venv · ruff · Sphinx · GitHub Actions · VS Code · Docker · Snowflake

---

## Modules

| # | Module | Description | Status |
|---|--------|-------------|--------|
| **01** | [Dev Environment Setup](01_dev_env_setup/) | Homebrew/winget, pyenv, venv, VS Code + extensions, Docker, .env & GitHub Secrets, AI tools (Copilot, Claude), automated setup scripts | ✅ Complete |
| **02** | [Python Best Practices](02_python_best_practices/) | Poetry & dependency management, code quality toolchain (ruff, sqlfluff, nb-clean, pre-commit), language standards, project structure (src/ layout), git workflow & branching strategy, code design principles, Snowflake deployment | ✅ Complete |
| **03** | [Documentation](03_documentation/) | Docstring standards (Google Style), Sphinx pipeline, GitHub Pages deployment, GitHub Wiki, documentation governance, data documentation | ✅ Complete |
| **04** | [Testing](04_testing/) | Testing strategy & pyramid, pytest standards, coverage, data/ML/API testing | ⏳ Pending |
| **05** | [Version Control](05_version_control/) | Branching strategy, commit conventions, code review, repository hygiene, tagging & releases | ⏳ Pending |
| **06** | [CI/CD](06_cicd/) | CI pipelines, quality gates, deployment strategies, pipeline orchestration, secrets management | ⏳ Pending |

---

## Repository Structure

```
pythonbestpractices/
├── README.md                                  ← This file (index)
│
├── 01_dev_env_setup/
│   ├── README.md                              ← pyenv, venv, VS Code, Docker, .env, AI tools, setup scripts
│   ├── vscode_extensions.md                   ← Detailed VS Code extensions guide
│   └── debug/                                 ← Debugging masterclass (3 notebooks + examples)
│       ├── 01_fundamentals.ipynb
│       ├── 02_intermediate.ipynb
│       ├── 03_advanced.ipynb
│       ├── debug_example.py
│       └── pipeline_example.py
│
├── 02_python_best_practices/
│   ├── README.md                              ← Poetry, ruff, pre-commit, project structure, git workflow
│   └── templates/
│       ├── .github/
│       │   ├── pull_request_template.md
│       │   └── workflows/ci.yml
│       ├── .vscode/settings.json
│       ├── .pre-commit-config.yaml
│       ├── .sqlfluff
│       ├── pyproject.toml
│       ├── poetry_quickstart.sh
│       └── README_TEMPLATE.md
│
├── 03_documentation/
│   ├── README.md                              ← Sphinx, GitHub Pages, Wiki, governance
│   └── templates/
│       ├── .github/
│       │   ├── CODEOWNERS
│       │   └── workflows/docs.yml
│       ├── docs/source/
│       │   ├── conf.py
│       │   └── index.rst
│       ├── adr_template.md
│       ├── CHANGELOG.md
│       ├── data_documentation_template.md
│       ├── doc_governance_checklist.md
│       ├── docstring_examples.py
│       └── mkdocs.yml
│
├── 04_testing/
│   ├── README.md                              ← Skeleton (pending)
│   └── templates/
│
├── 05_version_control/
│   ├── README.md                              ← Skeleton (pending)
│   └── templates/
│
└── 06_cicd/
    ├── README.md                              ← Skeleton (pending)
    └── templates/
```

---

## How to Use This Repository

1. **Start with Module 01** — set up your local development environment
2. **Read Module 02** — understand code quality standards and project structure
3. **Copy templates** from each module's `templates/` folder into your project
4. **Follow Module 03** — set up Sphinx documentation and GitHub Pages
5. **Adapt** everything to your project's specific needs

---

## Deliverables Summary (across all modules)

| Module | ID | Deliverable | Status |
|--------|----|------------|--------|
| 01 | D1–D10 | Setup scripts (macOS/Windows), VS Code settings, Dockerfile, .env.example, copilot-instructions.md, Claude prompt templates | ✅ |
| 02 | D1–D9 | Poetry quickstart script, pre-commit config, pyproject.toml, .sqlfluff, project structure template, PR template, packaging guide | ✅ |
| 03 | D1–D9 | Sphinx conf.py, index.rst, GitHub Pages workflow, docstring examples, CHANGELOG, CODEOWNERS, governance checklist, ADR template | ✅ |
| 04 | — | _Pending_ | ⏳ |
| 05 | — | _Pending_ | ⏳ |
| 06 | — | _Pending_ | ⏳ |
