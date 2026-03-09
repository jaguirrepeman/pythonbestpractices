# Python Best Practices — Repository Index

> **Date:** 2026-03-08  
> **Audience:** Data Science / Analytics / Engineering Teams

---

## Modules

| # | Module | Description | Status |
|---|--------|-------------|--------|
| **01** | [Programming Best Practices](01_programming_best_practices/) | IDE & tooling standards, language conventions, documentation (in-code, off-code, data), code structure & modularity, design principles, maintainability | ✅ Complete |
| **02** | [Packaging Standards](02_packaging_standards/) | Dependency management with Poetry, lock files & deterministic builds, Python package structure, package governance & Snowflake deployment | ✅ Complete |
| **03** | [Testing](03_testing/) | Testing strategy & pyramid, pytest standards, coverage, data/ML/API testing | ⏳ Pending |
| **04** | [Version Control](04_version_control/) | Branching strategy, commit conventions, code review, repository hygiene, tagging & releases | ⏳ Pending |
| **05** | [CI/CD](05_cicd/) | CI pipelines, quality gates, deployment strategies, pipeline orchestration, secrets management | ⏳ Pending |

---

## Repository Structure

```
pythonbestpractices/
├── README.md                              ← This file (index)
│
├── 01_programming_best_practices/
│   ├── README.md                          ← Full guide: IDE, language, docs, structure, design
│   └── templates/
│       ├── .github/
│       │   ├── pull_request_template.md
│       │   └── workflows/
│       │       ├── ci.yml
│       │       └── docs.yml
│       ├── CHANGELOG.md
│       ├── CODEOWNERS
│       ├── README_TEMPLATE.md
│       ├── data_documentation_template.md
│       ├── doc_governance_checklist.md
│       ├── docstring_examples.py
│       └── mkdocs.yml
│
├── 02_packaging_standards/
│   ├── README.md                          ← Controls, recommendations, deliverables + detailed guide
│   └── templates/
│       ├── .pre-commit-config.yaml
│       ├── .vscode/
│       │   └── settings.json
│       └── pyproject.toml
│
├── 03_testing/
│   ├── README.md                          ← Skeleton (pending controls)
│   └── templates/
│
├── 04_version_control/
│   ├── README.md                          ← Skeleton (pending controls)
│   └── templates/
│
└── 05_cicd/
    ├── README.md                          ← Skeleton (pending controls)
    └── templates/
```

---

## How to Use This Repository

1. **Read the module README** for standards and recommendations
2. **Copy templates** from `templates/` into your project
3. **Adapt** to your project's specific needs
4. **Attend the recommended sessions** for hands-on training

---

## Deliverables Summary (across all modules)

| Module | ID | Deliverable | Status |
|--------|----|------------|--------|
| 01 | E1–E13 | IDE config, docstring examples, README/CHANGELOG templates, MkDocs config, PR template, CODEOWNERS, etc. | ✅ |
| 02 | DEL-1 | Environment & Dependency Management Standard | ✅ |
| 02 | DEL-2 | Dependency Pinning & Lock File Policy | ✅ |
| 02 | DEL-3 | Python Package Structure Template | ✅ |
| 02 | DEL-4 | Package Governance & Snowflake Deployment Workflow | ✅ |
| 03 | — | _Pending_ | ⏳ |
| 04 | — | _Pending_ | ⏳ |
| 05 | — | _Pending_ | ⏳ |
