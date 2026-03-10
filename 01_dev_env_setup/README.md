# Module 1 — Development Environment Setup

> **Audience:** All team members. Use this as both an onboarding guide and a day-to-day reference.

---

## Table of Contents

| # | Section |
|---|------|
| | [How the Toolchain Fits Together](#how-the-toolchain-fits-together) |
| 1.1 | [System Package Manager (Homebrew)](#11--system-package-manager) |
| 1.2 | [Python Version Management (pyenv)](#12--python-version-management-pyenv) |
| 1.3 | [Virtual Environments & Poetry](#13--virtual-environments--poetry) |
| 1.4 | [VS Code](#14--vs-code-setup) |
| 1.5 | [Docker](#15--docker-for-development) |
| 1.6 | [Environment Variables & Secrets](#16--environment-variables--secrets) |
| 1.7 | [AI Coding Tools (Copilot, Claude)](#17--ai-assisted-coding-tools) |
| 1.8 | [Setup Scripts & WSL Guide](#18--automated-setup-scripts) |

---

## How the Toolchain Fits Together

The dev environment relies on four tools. They work in layers, and each one covers a different concern:

```
Homebrew / apt        System programs (git, pyenv, fzf, ripgrep...)
       ↓
pyenv                 Python VERSIONS (3.10, 3.11, 3.12...)
       ↓
Python 3.11           The interpreter itself, installed via pyenv
       ↓
Poetry                Creates .venv/, resolves + installs PACKAGES (pandas, pytest...)
```

| Tool | What it does | What it does NOT do |
|------|-------------|---------------------|
| **Homebrew** / **apt** | Installs native programs (git, pyenv, fzf, ripgrep...) | Has nothing to do with Python packages |
| **pyenv** | Installs multiple Python versions and switches between them per project | Does not install packages or create venvs |
| **Poetry** | Creates an isolated `.venv/` per project, resolves, installs, and locks Python packages. Also builds `.whl` packages | Does not install Python itself |

**"If we have Poetry, why do we also need pyenv?"**  
Poetry manages packages and virtual environments, but it expects a Python interpreter to already be available. It cannot install Python. That is pyenv's job. And Homebrew/apt is what installs pyenv itself (along with git and other system tools).

**"What about venv?"**  
Poetry uses Python's built-in `venv` module internally to create isolated environments. You do not need to run `python -m venv` yourself. When you run `poetry install`, Poetry detects the Python version (set by pyenv), creates a `.venv/` directory, and installs all dependencies inside it.

> If the whole team uses a single Python version and does not plan to change, pyenv can be skipped (install Python directly with Homebrew instead). That said, pyenv adds negligible overhead and becomes very useful the moment a second project requires a different version.

> **Windows users:** All development happens inside **WSL 2** (Windows Subsystem for Linux). This means the commands in sections 1.1–1.3 are identical on macOS and Windows/WSL. See [§ 1.8.1](#181--wsl-setup-guide-windows) for WSL installation instructions.

---

## 1.1 — System Package Manager

### macOS: Homebrew

[Homebrew](https://brew.sh/) is the standard package manager on macOS. We use it to install all system-level dependencies.

```bash
# Install Homebrew (if not already installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Verify
brew --version

# Install common system dependencies
brew install git wget curl jq
```

### Windows (WSL): apt + Homebrew

Inside WSL, Ubuntu's `apt` is available by default. The setup script ([`scripts/setup_wsl.sh`](scripts/setup_wsl.sh)) also installs Homebrew for Linux (Linuxbrew), so the Homebrew commands above work the same way.

```bash
# apt is available out of the box in WSL/Ubuntu
sudo apt update && sudo apt install -y git wget curl jq

# Homebrew (installed by the setup script) also works
brew install fzf ripgrep
```

> Native Windows package managers (winget, Chocolatey) are not used for Python development. Everything runs inside WSL.

---

## 1.2 — Python Version Management (pyenv)

[pyenv](https://github.com/pyenv/pyenv) manages multiple Python versions on the same machine. It lets you install, uninstall, and switch versions without ever touching the system Python.

### Installation

```bash
# macOS (via Homebrew)
brew install pyenv

# WSL/Linux (via Homebrew or build from source — the setup script handles this)
brew install pyenv

# Add to shell profile (~/.zshrc or ~/.bashrc)
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
echo '[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
echo 'eval "$(pyenv init -)"' >> ~/.zshrc
source ~/.zshrc
```

> **Note:** We do not use pyenv-win. Windows users install the standard pyenv inside WSL, which behaves identically to macOS.

### Usage

```bash
# List available versions
pyenv install --list | grep "3.11"

# Install a specific version
pyenv install 3.11.9

# Set global default
pyenv global 3.11.9

# Set project-specific version (creates .python-version file)
cd my-project
pyenv local 3.11.9

# Verify
python --version  # → Python 3.11.9
```

### Team Standard

| Rule | Details |
|------|---------|
| Minimum Python version | **≥ 3.10** (preferably 3.11+) |
| Version pinning | Every project has a `.python-version` file committed to Git |
| System Python | **Never** install packages into system Python |

---

## 1.3 — Virtual Environments & Poetry

### What is a virtual environment?

A virtual environment is an isolated copy of Python with its own `site-packages` directory. Each project gets its own environment, which prevents dependency conflicts (e.g. one project needs pandas 1.5, another needs 2.1). Without isolation, installing a package for one project could break another.

Python ships a built-in module (`venv`) to create these environments. **Poetry uses `venv` internally**, so you do not need to create environments manually.

### Poetry configuration

One-time setup so Poetry creates the `.venv/` inside each project directory (instead of a hidden cache folder):

```bash
poetry config virtualenvs.in-project true
```

This makes the venv visible in the project root, which VS Code auto-detects as the interpreter.

### Day-to-day workflow: pyenv + Poetry

```bash
# 1. Clone the repo
git clone https://github.com/org/my-project.git
cd my-project

# 2. pyenv sets the correct Python version (reads .python-version)
python --version  # → 3.11.9

# 3. Poetry creates .venv/ and installs all dependencies
poetry install

# 4. Activate the environment
source .venv/bin/activate   # or: poetry shell

# Ready to work
```

No `python -m venv` step needed. Poetry handles it.

### Adding and removing packages

```bash
# Add a dependency
poetry add pandas

# Add a dev-only dependency
poetry add --group dev pytest ruff

# Remove a dependency
poetry remove pandas

# Update all dependencies to latest compatible versions
poetry update
```

Poetry writes two files:
- `pyproject.toml` — declared dependencies (committed to Git)
- `poetry.lock` — exact resolved versions (committed to Git)

### Rules

| Rule | Details |
|------|---------|
| One venv per project | Always. Never share environments between projects |
| Location | `.venv/` in the project root (set via `virtualenvs.in-project true`) |
| Git | Add `.venv/` to `.gitignore`. Commit `pyproject.toml` and `poetry.lock` |
| Installing packages | Always via `poetry add`, never `pip install` directly |
| Naming | Always `.venv`, for consistency across the team |
| System Python | Never install packages into it |

> For a deeper dive into Poetry (dependency groups, scripts, publishing, monorepo patterns), see [Module 2](../02_python_best_practices/).

---

## 1.4 — VS Code Setup

VS Code is the standard IDE for the team. A detailed catalog of all required and recommended extensions lives in [`vscode_extensions.md`](vscode_extensions.md).

### Mandatory Extensions (quick list)

| Extension | ID | Purpose |
|-----------|----|---------|
| Python | `ms-python.python` | Core Python support |
| Pylance | `ms-python.vscode-pylance` | Type checking & IntelliSense |
| Ruff | `charliermarsh.ruff` | Linting + formatting (replaces black, isort, flake8) |
| Python Debugger | `ms-python.debugpy` | Debugging |
| Jupyter | `ms-toolsai.jupyter` | Notebook support |
| GitLens | `eamodio.gitlens` | Git blame, history, file annotations |
| Claude | `anthropic.claude-code` | AI coding assistant |
| autoDocstring | `njpwerner.autodocstring` | Generate Google Style docstrings |
| Find It Faster | `tomrijndorp.find-it-faster` | Fuzzy file/content search powered by `fd` + `rg` |
| Excalidraw | `pomdtr.excalidraw-editor` | Whiteboard / architecture diagrams inside VS Code |
| WSL | `ms-vscode-remote.remote-wsl` | Develop inside WSL from VS Code on Windows |

### Shared VS Code Settings

Copy to `.vscode/settings.json` in every project:

```json
{
    "editor.formatOnSave": true,
    "[python]": {
        "editor.defaultFormatter": "charliermarsh.ruff",
        "editor.tabSize": 4,
        "editor.codeActionsOnSave": {
            "source.fixAll": "explicit",
            "source.organizeImports": "explicit"
        }
    },
    "ruff.lineLength": 120,
    "python.analysis.typeCheckingMode": "basic",
    "autoDocstring.docstringFormat": "google",
    "autoDocstring.startOnNewLine": true,
    "files.trimTrailingWhitespace": true,
    "files.insertFinalNewline": true,
    "files.exclude": {
        "**/.venv": true,
        "**/__pycache__": true,
        "**/.mypy_cache": true,
        "**/.ruff_cache": true
    }
}
```

> See [`vscode_extensions.md`](vscode_extensions.md) for comprehensive documentation of each extension, including shortcuts, configuration, and usage tips.  
> See the [`debug/`](debug/) folder for a 3-part debugging masterclass.

### Bulk Install Script

```bash
# Install all mandatory extensions at once
code --install-extension ms-python.python
code --install-extension ms-python.vscode-pylance
code --install-extension charliermarsh.ruff
code --install-extension ms-python.debugpy
code --install-extension ms-toolsai.jupyter
code --install-extension eamodio.gitlens
code --install-extension anthropic.claude-code
code --install-extension njpwerner.autodocstring
code --install-extension tomrijndorp.find-it-faster
code --install-extension pomdtr.excalidraw-editor
code --install-extension ms-vscode-remote.remote-wsl
```

---

## 1.5 — Docker for Development

We use Docker to containerize the runtime environment, particularly for CI/CD pipelines in GitHub Actions.

### When to Use Docker

| Scenario | Use Docker? |
|----------|-------------|
| Local development | Optional; pyenv + venv is sufficient |
| CI/CD pipelines (GitHub Actions) | **Yes**, ensures consistent build environment |
| Deploying to production | **Yes**, reproducible runtime |
| Sharing a complex environment with system dependencies | **Yes** |

### Standard Dockerfile for Python Projects

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# System dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    git curl build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install --no-cache-dir poetry
RUN poetry config virtualenvs.create false

# Install dependencies (cached layer)
COPY pyproject.toml poetry.lock ./
RUN poetry install --only main --no-interaction --no-ansi

# Copy application code
COPY src/ src/

# Default command
CMD ["python", "-m", "my_project"]
```

### `.dockerignore`

```
.venv/
.git/
__pycache__/
*.pyc
.env
.mypy_cache/
.ruff_cache/
dist/
build/
notebooks/
tests/
docs/
```

---

## 1.6 — Environment Variables & Secrets

### Local Development: `.env`

Use a `.env` file for local environment settings and credentials. **Never commit it to Git.**

```bash
# .env (local only, listed in .gitignore)
DATABASE_URL=postgresql://localhost:5432/dev_db
SNOWFLAKE_ACCOUNT=xy12345.us-east-1
SNOWFLAKE_USER=dev_user
SNOWFLAKE_PASSWORD=local_password_here
API_KEY=dev-api-key-12345
LOG_LEVEL=DEBUG
```

Provide a `.env.example` file (committed to Git) showing the expected variables without values:

```bash
# .env.example (committed to Git)
DATABASE_URL=
SNOWFLAKE_ACCOUNT=
SNOWFLAKE_USER=
SNOWFLAKE_PASSWORD=
API_KEY=
LOG_LEVEL=DEBUG
```

### Loading `.env` in Python

```python
# Use python-dotenv
from dotenv import load_dotenv
import os

load_dotenv()  # reads .env into os.environ

db_url = os.getenv("DATABASE_URL")
```

### CI/CD & Shared Credentials: GitHub Secrets

| Rule | Details |
|------|---------|
| **Never in code** | Credentials must never appear in source code, config files, or notebooks |
| **GitHub Secrets** | Store all shared/production credentials in **GitHub Repository Secrets** or **Organization Secrets** |
| **Access in CI** | Reference as `${{ secrets.SECRET_NAME }}` in GitHub Actions workflows |
| **.env in .gitignore** | Always. Enforce via pre-commit hook (`check-added-large-files`, `.gitignore` audit) |

```yaml
# In GitHub Actions workflow
env:
  SNOWFLAKE_ACCOUNT: ${{ secrets.SNOWFLAKE_ACCOUNT }}
  SNOWFLAKE_USER: ${{ secrets.SNOWFLAKE_USER }}
  SNOWFLAKE_PASSWORD: ${{ secrets.SNOWFLAKE_PASSWORD }}
```

---

## 1.7 — AI-Assisted Coding Tools

### Approved Tools

| Tool | Extension ID | Primary Use |
|------|-------------|-------------|
| **Claude Code** | `anthropic.claude-code` | Multi-file refactors, architecture, code review, agentic tasks |
| **GitHub Copilot** | `github.copilot` | Inline autocomplete, chat, docstring generation |

### Rules of Engagement

1. **Human review is mandatory.** Every AI-generated code block must be understood, reviewed, and tested before committing.
2. **No sensitive data.** Never send credentials, PII, or proprietary client data to AI tools.
3. **Tests required.** AI-generated code requires the same test coverage as manual code.
4. **Docstrings.** Use AI to draft initial docstrings, then verify accuracy.
5. **Attribution.** Add `# AI-assisted` comment only for substantial generated blocks.

---

### GitHub Copilot Custom Instructions (`copilot-instructions.md`)

Copilot reads a `.github/copilot-instructions.md` file from the root of the repo to gain project-specific context. **This file must be committed to every project repository.**

The team template is at [`templates/.github/copilot-instructions.md`](templates/.github/copilot-instructions.md). It covers: code standards (PEP 8 + team rules), project structure (`src/` layout), data management, reproducibility, feature engineering, modeling, evaluation metrics, testing, performance, and a "Do NOT" checklist. Copy it into each new repo and adjust the project-specific sections.

> **Where to put it:** `.github/copilot-instructions.md` at the repo root. Copilot reads it automatically whenever the repo is open.
>
> **Cross-references:**
> - Coding standards → [02_python_best_practices § 2.3](../02_python_best_practices/#23--python-language-standards)
> - Project structure → [02_python_best_practices § 2.4](../02_python_best_practices/#24--project-structure)
> - Pre-commit hooks → [02_python_best_practices § 2.2](../02_python_best_practices/#22--code-quality-toolchain)
> - Docstring standards → [03_documentation § 3.1](../03_documentation/#31--docstring-standards)
> - Testing patterns → [04_testing](../04_testing/) (pending)

---

### Claude Code Instructions

Claude Code reads a `CLAUDE.md` file at the repo root on startup for project-specific context. Since the content is the same as `copilot-instructions.md`, create a **symlink** instead of duplicating the file:

```bash
# From the project root
ln -s .github/copilot-instructions.md CLAUDE.md
```

This way both Copilot and Claude Code read the same file. Any update to `copilot-instructions.md` is automatically picked up by both tools.

> Commit the symlink to Git. It works on macOS and WSL without issues.

#### Permissions (`.claude/settings.json`)

Claude Code also reads `.claude/settings.json` to scope what it can do. Use it to allow safe commands and block destructive ones:

```json
{
  "permissions": {
    "allow": [
      "Read",
      "Edit",
      "Bash(poetry run pytest*)",
      "Bash(poetry run ruff*)",
      "Bash(poetry run mypy*)",
      "Bash(git diff*)",
      "Bash(git log*)"
    ],
    "deny": [
      "Bash(rm -rf*)",
      "Bash(git push*)",
      "Bash(git commit*)"
    ]
  }
}
```

---

## 1.8 — Automated Setup Scripts

Ready-to-use scripts that install the full dev environment from scratch. Each script handles: system dependencies, pyenv, Python, Poetry, pre-commit, and VS Code extensions.

| OS | Script | Usage |
|----|--------|-------|
| **macOS** | [`scripts/setup_macos.sh`](scripts/setup_macos.sh) | `chmod +x scripts/setup_macos.sh && ./scripts/setup_macos.sh` |
| **Windows (WSL)** | [`scripts/setup_wsl.sh`](scripts/setup_wsl.sh) | `chmod +x scripts/setup_wsl.sh && ./scripts/setup_wsl.sh` |

Both scripts accept an optional Python version argument: `./scripts/setup_macos.sh 3.12.3`

> **Windows users:** We use **WSL 2** (Windows Subsystem for Linux) as the standard development environment. See the WSL setup guide below before running the script.

---

### 1.8.1 — WSL Setup Guide (Windows)

**WSL 2** provides a full Linux environment on Windows. All Python development, pyenv, Homebrew, and terminal workflows run inside WSL, identical to macOS. VS Code connects to WSL through the **WSL extension**.

#### Step 1 — Install WSL 2

Open **PowerShell as Administrator** and run:

```powershell
wsl --install -d Ubuntu
```

This installs WSL 2 + Ubuntu. Restart your machine when prompted. On reboot, a terminal opens asking you to create a Linux username and password.

> If WSL was already installed, make sure you're on version 2: `wsl --set-default-version 2`

#### Step 2 — Verify

```powershell
# From PowerShell
wsl --list --verbose
```

You should see Ubuntu with VERSION = 2.

#### Step 3 — Install VS Code WSL Extension

1. Open VS Code **on Windows**
2. Install the **WSL** extension (`ms-vscode-remote.remote-wsl`)
3. Open a WSL terminal: `Ctrl+Shift+`` → select **Ubuntu (WSL)**
4. Or from the WSL terminal, type `code .` to open VS Code connected to WSL

#### Step 4 — Run the Setup Script

Inside the WSL terminal:

```bash
cd /path/to/pythonbestpractices/01_dev_env_setup
chmod +x scripts/setup_wsl.sh
./scripts/setup_wsl.sh
```

The script installs all the same tools as macOS (Homebrew, pyenv, Poetry, VS Code extensions) plus the build dependencies that Ubuntu needs for compiling Python.

#### How VS Code + WSL Works

```
┌─────────────────────────┐     ┌──────────────────────────┐
│   Windows Host          │     │   WSL 2 (Ubuntu)         │
│                         │     │                          │
│   VS Code UI ◄──────────┼─────┤   VS Code Server         │
│   Extensions (UI)       │     │   Extensions (workspace) │
│                         │     │   Python, pyenv, Poetry  │
│                         │     │   Git, pre-commit, ruff  │
│                         │     │   Your project files     │
└─────────────────────────┘     └──────────────────────────┘
```

- **VS Code runs on Windows**, but the workspace, terminal, debugger, and extensions execute **inside WSL**.
- File system: keep your projects in the **WSL filesystem** (`~/projects/`), not in `/mnt/c/`. The Linux filesystem is significantly faster.
- Git credentials: the setup script configures Git Credential Manager to share credentials between Windows and WSL.
- Terminal: VS Code auto-detects WSL. Default terminal will be Ubuntu bash.

#### Common WSL Commands

| Command | Description |
|---------|-------------|
| `wsl` | Open default WSL distro from PowerShell |
| `wsl --shutdown` | Stop all WSL instances (useful to free RAM) |
| `wsl --list --verbose` | List installed distros and WSL version |
| `explorer.exe .` | Open Windows Explorer in current WSL directory |
| `code .` | Open VS Code connected to WSL in current directory |

#### Troubleshooting

| Issue | Solution |
|-------|----------|
| `code` command not found in WSL | Open VS Code on Windows → `Ctrl+Shift+P` → "Shell Command: Install 'code' command" |
| Slow file access | Move projects to `~/projects/` instead of `/mnt/c/` |
| WSL using too much RAM | Create `%USERPROFILE%\.wslconfig` with `[wsl2]\nmemory=8GB` |
| Git auth fails | Run `git config --global credential.helper "/mnt/c/Program\ Files/Git/mingw64/bin/git-credential-manager.exe"` |

---

## Deliverables Summary

| ID | Deliverable | Location |
|----|------------|----------|
| **D1** | macOS setup script | [`scripts/setup_macos.sh`](scripts/setup_macos.sh) |
| **D2** | WSL (Windows) setup script | [`scripts/setup_wsl.sh`](scripts/setup_wsl.sh) |
| **D3** | VS Code shared settings | `templates/.vscode/settings.json` |
| **D4** | `.env.example` template | `templates/.env.example` |
| **D5** | Copilot custom instructions | `templates/.github/copilot-instructions.md` |
| **D6** | VS Code extensions catalog | [`vscode_extensions.md`](vscode_extensions.md) |
| **D7** | Debugging masterclass (3 notebooks) | [`debug/`](debug/) |
| **D8** | Standard Dockerfile | `templates/Dockerfile` |
| **D9** | `.dockerignore` template | `templates/.dockerignore` |

---

**Next →** [02_python_best_practices/](../02_python_best_practices/) | Poetry, code quality, pre-commit hooks, project structure, git workflow
