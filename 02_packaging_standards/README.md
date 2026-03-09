# D1.B.1 — Build & Packaging Standards: Environment & Dependency Management

> **Date:** 2026-03-06

---

## Controls, Recommendations & Deliverables

| # | Controls | Recommendations | Deliverables |
|---|----------|----------------|--------------|
| 1 | **Virtual Environments & Dependency Management Tool** (D1.B.1.1.1 – D1.B.1.1.3) — Standard dependency manager, isolated environments, reproducible configs | Adopt **Poetry** as the single standard tool for dependency management and virtual environment isolation. Every project must use its own isolated environment — never install into system Python. All environment configuration (`pyproject.toml`) must be version-controlled. | **[DEL-1]** Environment & Dependency Management Standard |
| 2 | **Lock Files & Deterministic Builds** (D1.B.1.2.1 – D1.B.1.2.3) — Pinned versions, deterministic resolution, automated updates | Always commit `poetry.lock` to the repository. Pin direct dependencies with version constraints (`^` or `~`); the lock file guarantees the exact resolved tree. Enable **Dependabot / Renovate** for automated dependency update PRs validated by CI. | **[DEL-2]** Dependency Pinning & Lock File Policy |
| 3 | **Python Packaging** (D1.B.1.2.1, D1.B.1.3.1) — Standardized package structure, build reproducibility | Every deliverable must be structured as an installable Python package using `pyproject.toml` (PEP 621). Follow the `src/` layout convention. Package builds must be reproducible from the lock file alone, both locally and in CI/CD. | **[DEL-3]** Python Package Structure Template |
| 4 | **Package Governance & Deployment to Snowflake** (D1.B.1.3.1) — Cross-project dependency coordination, release process, deployment to Snowflake stages | Maintain a shared dependencies registry listing approved versions of common libraries. Define a clear release process (version bump, CHANGELOG, CI build & publish). Deploy packages to **Snowflake stages** for use in Snowpark, UDFs, and stored procedures, ensuring dependency compatibility with the Snowflake Anaconda channel. | **[DEL-4]** Package Governance & Snowflake Deployment Workflow |

---

## Deliverables

| ID | Deliverable | Description | Format |
|----|------------|-------------|--------|
| **DEL-1** | Environment & Dependency Management Standard | Defines Poetry as the standard tool. Includes ready-to-use `pyproject.toml` template, environment setup guide for reproducible dev/test/prod, `poetry install` workflow, CI caching strategy, and Docker integration patterns. | Markdown + TOML template |
| **DEL-2** | Dependency Pinning & Lock File Policy | Policy defining: pinning strategy, lock file commit requirements, process for adding/upgrading dependencies, forbidden/restricted packages list. Includes pre-configured Dependabot/Renovate configs for automated update PRs with CI gating. | Markdown + YAML configs + CI workflow |
| **DEL-3** | Python Package Structure Template | Cookiecutter-ready project template with `src/` layout, `pyproject.toml` (PEP 621), `py.typed` marker, proper `__init__.py` exports, and CI build pipeline. Ready to clone and start a new package in under 5 minutes. | Project template (cookiecutter / copier) |
| **DEL-4** | Package Governance & Snowflake Deployment Workflow | Governance document defining: shared dependencies registry, semantic versioning policy, automated release pipeline (version bump → build → upload to Snowflake stage → CHANGELOG). Includes Snowflake-specific guidance: uploading packages to stages, managing dependencies via the Anaconda channel, and deploying UDFs/stored procedures from versioned packages. | Markdown + CI/CD pipeline configs + SQL templates |

---

## Recommended Sessions

| # | Session | Audience | Duration | Objective |
|---|---------|----------|----------|-----------|
| **S1** | **Poetry for Dependency Management — Hands-on Workshop** | All developers | 1.5h | End-to-end Poetry workflow (`poetry new`, `add`, `lock`, `install`, `build`, `publish`). Practice creating reproducible environments, understanding the lock file, and configuring dependency groups (dev, docs, test). |
| **S2** | **Python Packaging & Project Structure** | All developers | 1.5h | Build a Python package from scratch: `src/` layout, `pyproject.toml` configuration, type hints with `py.typed`, proper public API via `__init__.py`, and local editable installs. Run the CI pipeline to build and validate. |
| **S3** | **Package Governance, Private Registry & Release Automation** | Tech leads + Senior devs | 1h | Set up a private package registry, configure CI/CD to auto-publish on tag, walk through the shared dependencies registry, and define the governance process for approving new dependencies and releasing versions. |

---
---

## Detailed Explanation (Client Presentation)

### 1. Virtual Environments & Dependency Management with Poetry

#### The Problem

Without a standard dependency management tool, teams face:
- **"Works on my machine" syndrome:** Each developer installs packages differently, leading to inconsistent environments that break when code moves to staging or production.
- **System-level pollution:** Installing packages into the global Python interpreter creates conflicts between projects that need different versions of the same library.
- **Onboarding friction:** New team members spend hours (sometimes days) figuring out which packages to install, which versions to use, and how to replicate a working environment.

#### The Solution: Poetry as the Single Standard

**Poetry** is a modern Python dependency manager that solves all three problems in a single tool:

| Capability | How Poetry solves it |
|------------|---------------------|
| **Dependency declaration** | All dependencies are declared in `pyproject.toml` — a single, human-readable file that replaces `requirements.txt`, `setup.py`, and `setup.cfg`. |
| **Virtual environment isolation** | Poetry automatically creates and manages an isolated virtual environment per project. Developers never need to think about `venv` or `conda` — Poetry handles it transparently. |
| **Reproducibility** | Poetry generates a `poetry.lock` file that pins every single package in the dependency tree (direct and transitive) to an exact version + hash. Anyone running `poetry install` gets an identical environment. |
| **Dependency groups** | Dependencies can be organized into groups (`dev`, `docs`, `test`), so production environments never include development tools. |
| **Build & publish** | Poetry can build wheels/sdists and publish to PyPI or private registries — no separate build tool needed. |

#### What changes for the developer

```bash
# Before (fragmented, unreliable)
python -m venv .venv
pip install -r requirements.txt          # which requirements.txt? dev? prod?
pip install pandas==2.1.0                # manually tracked, easy to forget
pip freeze > requirements.txt            # overwrites everything, includes sub-dependencies

# After (standardized, reproducible)
poetry install                           # creates venv + installs exact locked versions
poetry add pandas                        # adds to pyproject.toml + updates lock
poetry add --group dev pytest            # dev-only dependency
poetry install --only main               # production install (no dev tools)
```

#### Why Poetry over alternatives?

| Tool | Pros | Cons | Verdict |
|------|------|------|---------|
| **pip + requirements.txt** | Simple, universal | No lock file, no environment management, no dependency resolution | Not sufficient for teams |
| **pip-tools** | Lock file support | No environment management, no build/publish | Incomplete |
| **conda** | Great for scientific computing | Slow resolution, mixing conda + pip is fragile, not PEP-compliant | Use only when C-level dependencies require it |
| **Poetry** | Full lifecycle (resolve, lock, install, build, publish), PEP-compliant, excellent UX | Slightly slower than uv for resolution | **Recommended standard** |
| **uv** | Extremely fast resolution | Newer, smaller ecosystem, less mature for build/publish | Strong alternative; consider for future |

---

### 2. Lock Files & Deterministic Builds

#### The Problem

Consider two developers working on the same project:

```
Developer A installs on Monday    →  gets pandas 2.1.0, numpy 1.26.0
Developer B installs on Thursday  →  gets pandas 2.1.1, numpy 1.26.1 (new patch released)
```

Both used the same `pyproject.toml`, but they get **different environments**. A subtle bug in pandas 2.1.1 breaks the feature engineering pipeline — but only for Developer B. They spend two days debugging before realizing the issue is a dependency mismatch.

In production, the same problem is catastrophic: a deployment on Tuesday works, but a redeployment on Wednesday (from the same code) installs different package versions and breaks.

#### The Solution: The Lock File

The `poetry.lock` file captures the **exact resolved dependency tree** — every package, every version, every hash:

```toml
# poetry.lock (auto-generated, committed to Git)
[[package]]
name = "pandas"
version = "2.1.0"
description = "Powerful data structures for data analysis"
files = [
    {file = "pandas-2.1.0-cp311-cp311-win_amd64.whl", hash = "sha256:abc123..."},
]

[package.dependencies]
numpy = ">=1.23.2"
python-dateutil = ">=2.8.2"
...
```

When any developer or CI pipeline runs `poetry install`, they get **exactly** these versions. No surprises, no drift.

#### Lock File Workflow

```
Developer adds a dependency:
    poetry add scikit-learn
           │
           ▼
    pyproject.toml updated (constraint: ^1.3)
    poetry.lock updated (resolved: scikit-learn==1.3.2 + all transitive deps)
           │
           ▼
    Both files committed to Git in the same PR
           │
           ▼
    CI runs "poetry install" → deterministic environment
    Other developers run "poetry install" → identical environment
```

#### Automated Dependency Updates

Pinned dependencies solve reproducibility but introduce a new risk: **version rot**. If you never update, you accumulate security vulnerabilities and miss performance improvements.

The solution is **automated dependency update PRs** via Dependabot or Renovate:

1. Bot checks for new versions weekly
2. Bot opens a PR updating `poetry.lock` (and `pyproject.toml` if needed)
3. CI validates the update (tests pass, no regressions)
4. Developer reviews and merges

This keeps dependencies fresh without manual effort, and every update is tested before it reaches `main`.

---

### 3. Python Packages

#### The Problem

Many data science teams write code in loose scripts or notebooks that are:
- **Not importable:** You can't `import` a Jupyter notebook or a script without ugly hacks.
- **Not testable:** Without a package structure, setting up tests with proper imports is painful.
- **Not shareable:** If Team B needs a function from Team A, they copy-paste it — creating drift and duplication.
- **Not deployable:** Moving from "it runs in my notebook" to "it runs in production" requires a complete rewrite.

#### The Solution: Every Deliverable is a Package

Every piece of code that will be used beyond a single notebook must be structured as a proper **installable Python package**:

```
my_project/
├── src/
│   └── my_project/
│       ├── __init__.py          # Public API: what gets exported when someone does "import my_project"
│       ├── py.typed             # PEP 561 marker — this package supports type checking
│       ├── core/
│       │   ├── __init__.py
│       │   └── engine.py        # Core business logic
│       ├── features/
│       │   ├── __init__.py
│       │   └── time_series.py   # Feature engineering
│       └── data/
│           ├── __init__.py
│           └── loaders.py       # Data access layer
├── tests/
│   ├── conftest.py
│   └── unit/
│       └── test_engine.py
├── pyproject.toml               # Single source of truth for project metadata + dependencies
└── poetry.lock                  # Exact dependency tree
```

#### Why the `src/` layout?

The `src/` layout prevents a common trap: **accidentally importing from the local directory instead of the installed package**. Without `src/`, running `python -c "import my_project"` from the project root imports from the local folder — which may not match what gets installed. With `src/`, you must `pip install -e .` first, which guarantees you're testing the real package.

#### The `pyproject.toml` as Single Source of Truth

```toml
[tool.poetry]
name = "my-project"
version = "1.2.0"
description = "Time series forecasting toolkit"
authors = ["Data Science Team <ds@company.com>"]
packages = [{include = "my_project", from = "src"}]

[tool.poetry.dependencies]
python = "^3.11"
pandas = "^2.1"
scikit-learn = "^1.3"

[tool.poetry.group.dev.dependencies]
pytest = "^8.0"
black = "^24.0"
ruff = "^0.4"

[tool.poetry.group.docs.dependencies]
mkdocs-material = "^9.5"
mkdocstrings = {extras = ["python"], version = "^0.25"}
```

One file replaces what used to require `setup.py` + `setup.cfg` + `requirements.txt` + `requirements-dev.txt` + `MANIFEST.in`.

#### Build & Install Workflow

```bash
# Development: editable install (changes to code are immediately reflected)
poetry install

# Build distributable package
poetry build
# → dist/my_project-1.2.0-py3-none-any.whl
# → dist/my_project-1.2.0.tar.gz

# Publish to private registry
poetry publish --repository private-registry
```

---

### 4. Package Governance & Deployment to Snowflake

#### The Problem

As the number of internal packages grows, new challenges emerge:
- **Dependency conflicts:** Project A uses `pandas 2.0`, Project B uses `pandas 2.1`, and a shared library must work with both — and both must be compatible with the Snowflake Anaconda channel.
- **Uncontrolled proliferation:** Anyone can add any dependency, leading to bloated dependency trees, security risks, and packages that fail when deployed to Snowflake because the dependency is not available in the Anaconda channel.
- **No discoverability:** Team B doesn't know Team A already built a utility they need, so they build it again.
- **No release process:** New versions are deployed by manually uploading files to Snowflake stages — no versioning, no changelog, no rollback capability.
- **Snowflake-specific constraints:** Snowpark UDFs and stored procedures can only use packages available in the Snowflake Anaconda channel or explicitly uploaded to a stage. If a team discovers this incompatibility during deployment, they waste days refactoring.

#### The Solution: A Governance Framework with Snowflake Deployment

##### 4a. Shared Dependencies Registry

A centrally maintained file listing **approved versions** of common libraries, explicitly validated against Snowflake Anaconda channel availability:

```toml
# shared-dependencies.toml (maintained by Tech Leads)

[approved]
# Available in Snowflake Anaconda channel — safe to use in Snowpark UDFs
pandas = "^2.1"        # ✅ Snowflake Anaconda
numpy = "^1.26"        # ✅ Snowflake Anaconda
scikit-learn = "^1.3"  # ✅ Snowflake Anaconda
pydantic = "^2.0"      # ✅ Snowflake Anaconda
sqlalchemy = "^2.0"    # ✅ Snowflake Anaconda

[stage-upload-required]
# NOT in Snowflake Anaconda channel — must be uploaded to stage as .whl
company-ml-utils = "^1.3"       # Internal package
company-data-loaders = "^2.1"   # Internal package

[restricted]
# These require explicit approval before use
tensorflow = "Requires GPU budget approval; NOT available in Snowflake Anaconda"
spark = "Use Databricks-managed Spark instead"

[forbidden]
pickle5 = "Security risk — use joblib or parquet"
```

A CI check validates every project's `pyproject.toml` against this registry and flags:
- Unapproved or misaligned versions
- Dependencies not available in the Snowflake Anaconda channel (must be explicitly handled)

##### 4b. Snowflake Deployment Model

Snowflake has a specific model for running Python code: **Snowpark** for DataFrames and **UDFs/Stored Procedures** for custom logic. Both require that dependencies are either:
1. **Available in the Snowflake Anaconda channel** (free to use, pre-installed), or
2. **Uploaded as `.whl` files to a Snowflake stage** (for internal or unavailable packages)

```
Dependency resolution for Snowflake deployment:

  Is the package in Snowflake Anaconda channel?
     ├── YES → Declare in `packages` parameter of UDF/Sproc. Done.
     └── NO  → Build .whl with Poetry → Upload to @stage → Reference via `imports`
```

**Deploying an internal package to Snowflake:**

```bash
# 1. Build the wheel
poetry build
# → dist/company_ml_utils-1.3.0-py3-none-any.whl

# 2. Upload to Snowflake stage
# Via SnowSQL:
PUT file://dist/company_ml_utils-1.3.0-py3-none-any.whl
    @my_db.my_schema.python_packages/
    AUTO_COMPRESS=FALSE
    OVERWRITE=TRUE;
```

**Using the package in a Snowpark Stored Procedure:**

```python
import snowflake.snowpark as snowpark

def register_procedure(session: snowpark.Session) -> None:
    """Register a stored procedure that uses our internal package."""
    session.sproc.register(
        func=my_processing_function,
        name="process_sales_data",
        # Anaconda channel packages — declared here:
        packages=["pandas==2.1.0", "scikit-learn==1.3.2"],
        # Internal packages uploaded to stage — declared here:
        imports=["@my_db.my_schema.python_packages/company_ml_utils-1.3.0-py3-none-any.whl"],
        replace=True,
    )
```

**Using the package in a SQL-defined UDF:**

```sql
CREATE OR REPLACE FUNCTION predict_demand(store_id VARCHAR, date DATE)
RETURNS FLOAT
LANGUAGE PYTHON
RUNTIME_VERSION = '3.11'
PACKAGES = ('pandas==2.1.0', 'scikit-learn==1.3.2')  -- Anaconda channel
IMPORTS = ('@my_db.my_schema.python_packages/company_ml_utils-1.3.0-py3-none-any.whl')
HANDLER = 'company_ml_utils.predict.run';
```

##### 4c. Release & Deployment Process

Every package follows a standardized release workflow that ends with Snowflake deployment:

```
1. Developer opens PR with changes
        │
        ▼
2. CI runs: tests + lint + docstring checks + build
        │
        ▼
3. PR merged to main
        │
        ▼
4. Developer bumps version:
        poetry version minor    # 1.2.0 → 1.3.0
        │
        ▼
5. Update CHANGELOG.md (move [Unreleased] → [1.3.0])
        │
        ▼
6. Create Git tag: v1.3.0
        │
        ▼
7. CI automatically:
   ├── Builds wheel + sdist (poetry build)
   ├── Uploads .whl to Snowflake stage (@python_packages/)
   ├── Updates Snowflake UDFs/Sprocs to reference new version
   ├── Deploys versioned documentation
   └── Creates GitHub Release with notes
```

**CI/CD step for Snowflake upload (example):**

```yaml
# .github/workflows/release.yml (deploy step)
  deploy-to-snowflake:
    runs-on: ubuntu-latest
    needs: [build]
    steps:
      - name: Upload wheel to Snowflake stage
        env:
          SNOWFLAKE_ACCOUNT: ${{ secrets.SF_ACCOUNT }}
          SNOWFLAKE_USER: ${{ secrets.SF_USER }}
          SNOWFLAKE_PASSWORD: ${{ secrets.SF_PASSWORD }}
        run: |
          pip install snowflake-connector-python
          python scripts/upload_to_snowflake.py \
            --stage "@my_db.my_schema.python_packages" \
            --file "dist/*.whl"
```

##### 4d. Dependency Approval Process

```
Developer wants to add a new dependency
        │
        ▼
Is it in the shared-dependencies.toml "approved" list?
   ├── YES (Anaconda channel) → Add it, no approval needed
   ├── YES (stage-upload-required) → Add it, ensure .whl is on the stage
   ├── RESTRICTED → Submit request with justification to Tech Lead
   └── NOT LISTED → Submit request:
        │   ├── License check
        │   ├── Security scan
        │   ├── Is it in Snowflake Anaconda channel?
        │   └── If not: can we build a pure-Python .whl?
        ▼
Tech Lead reviews and decides:
   ├── Approve → Add to registry, developer proceeds
   └── Reject → Suggest alternative or document exception
```

> **Key Snowflake constraint:** Packages with C extensions (e.g., compiled libraries) are difficult to upload as `.whl` files because they must match the Snowflake server's Linux architecture. Always prefer pure-Python packages or packages available in the Anaconda channel.

This ensures the organization maintains control over the dependency landscape while guaranteeing that every package can actually be deployed and executed within Snowflake.
