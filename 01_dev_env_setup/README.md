# Module 1 — Development Environment Setup

> **Audience:** All team members. Use this as both an onboarding guide and a day-to-day reference.

---

## Table of Contents

| # | Section |
|---|------|
| 1.1 | [Environment Toolchain Overview](#11--environment-toolchain-overview) |
| 1.2 | [System Package Manager & WSL](#12--system-package-manager) |
| 1.3 | [Python Version Management (pyenv)](#13--python-version-management-pyenv) |
| 1.4 | [Virtual Environments & Poetry](#14--virtual-environments--poetry) |
| 1.5 | [VS Code](#15--vs-code-setup) |
| 1.6 | [Docker](#16--docker-for-development) |
| 1.7 | [Environment Variables & Secrets](#17--environment-variables--secrets) |
| 1.8 | [AI Coding Tools (Copilot, Claude)](#18--ai-assisted-coding-tools) |
| 1.9 | [Setup Scripts & New Project Checklist](#19--setup-scripts--new-project-checklist) |

---

## 1.1 — Environment Toolchain Overview

The dev environment relies on four tools. They work in layers, and each one covers a different concern:

```
System package manager  System programs (git, pyenv, fzf, ripgrep...)
       ↓
pyenv                  Python Versions (3.10, 3.11, 3.12...)
       ↓
Python 3.11            The interpreter itself, installed via pyenv
       ↓
Poetry                 Creates .venv/, resolves + installs PACKAGES (pandas, pytest...)
```

| Tool | What it does | What it does NOT do |
|------|-------------|---------------------|
| **System package manager** | Installs native programs (git, pyenv, fzf, ripgrep...) | Has nothing to do with Python packages |
| **pyenv** | Installs multiple Python versions and switches between them per project | Does not install packages or create venvs |
| **Poetry** | Creates an isolated `.venv/` per project, resolves, installs, and locks Python packages. Also builds `.whl` packages | Does not install Python itself |

### System package manager: Homebrew vs apt

The first layer in the diagram is a system package manager. Which one you use depends on the OS:

| OS | Package manager | Notes |
|----|----------------|-------|
| **macOS** | [Homebrew](https://brew.sh/) | The standard on macOS. Installed manually (see § 1.2) |
| **Windows (WSL)** | **apt** (pre-installed) + Homebrew | Windows users develop inside **WSL 2** (Windows Subsystem for Linux), a full Linux environment that runs on Windows. Inside WSL, `apt` comes pre-installed. The setup script also installs [Homebrew for Linux](https://docs.brew.sh/Homebrew-on-Linux) so that `brew` commands work identically across macOS and WSL. See [§ 1.2.1](#121--wsl-setup-guide-windows) for installation instructions |

In practice, both do the same thing: install system-level programs like `git`, `pyenv`, `fzf`, and `ripgrep`. The rest of this guide uses `brew` in examples because it works on both platforms.


**"Poetry and venv"**  
Poetry uses Python's built-in `venv` module internally to create isolated environments (you do not need to run `python -m venv` yourself). When you run `poetry install`, Poetry detects the Python version (set by pyenv), creates a `.venv/` directory, and installs all dependencies inside it.

> **Windows users:** All development happens inside **WSL 2** (Windows Subsystem for Linux). This means the commands in sections 1.2–1.4 are identical on macOS and Windows/WSL. See [§ 1.2.1](#121--wsl-setup-guide-windows) for WSL installation instructions.

---

## 1.2 — System Package Manager

### 1.2.1 — WSL Setup Guide (Windows)

> **macOS users:** Skip this subsection. It only applies to Windows.

**WSL 2** (Windows Subsystem for Linux) provides a full Linux environment on Windows. All Python development, pyenv, Homebrew, and terminal workflows run inside WSL, identical to macOS. You need to install WSL before you can use `apt` or `brew`.

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

The script installs all the same tools as macOS (Homebrew, pyenv, Poetry, VS Code extensions) plus the build dependencies that Ubuntu needs for compiling Python. See [§ 1.9](#19--setup-scripts--new-project-checklist) for details on both setup scripts.

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

---

## 1.3 — Python Version Management (pyenv)

[pyenv](https://github.com/pyenv/pyenv) manages multiple Python versions on the same machine. It lets you install, uninstall, and switch versions without ever touching the system Python.

### Installation

```bash
brew install pyenv

# Add to shell profile (~/.zshrc or ~/.bashrc)
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
echo '[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
echo 'eval "$(pyenv init -)"' >> ~/.zshrc
source ~/.zshrc
```

`brew install pyenv` installs the binary, but pyenv also needs to hook into the shell so it can intercept the `python` command and switch versions automatically. The three `echo` lines add that hook to the shell profile. Without them, commands like `pyenv local 3.11.9` would have no effect.

> The setup scripts ([§ 1.9](#19--automated-setup-scripts)) already handle this configuration. These manual steps are only needed if you are setting up pyenv without the script.

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
| Minimum Python version | **≥ 3.11** |
| Version pinning | Every project has a `.python-version` file committed to Git |
| System Python | **Never** install packages into system Python |

The `.python-version` file lives in the **project root** (next to `pyproject.toml`) and contains a single line with the version number (e.g. `3.11.9`). You create it once when setting up the project:

```bash
cd my-project
pyenv local 3.11.9   # creates .python-version
```

After that, you do not need to use pyenv again for day-to-day work. When you (or a new team member) clone the repo and run `poetry install`, Poetry reads `.python-version`, picks up the correct Python, and creates the `.venv/` automatically. The file just needs to exist in the repo.

---

## 1.4 — Virtual Environments & Poetry

### What is a virtual environment?

A virtual environment is an isolated copy of Python with its own `site-packages` directory. Each project gets its own environment, which prevents dependency conflicts (e.g. one project needs pandas 1.5, another needs 2.1). Without isolation, installing a package for one project could break another.

Python ships a built-in module (`venv`) to create these environments. **Poetry uses `venv` internally**, so you do not need to create environments manually.

### What is Poetry?

[Poetry](https://python-poetry.org/) is the tool we use to manage dependencies and virtual environments. In a single command (`poetry install`) it:

1. Reads `.python-version` to pick the correct Python interpreter
2. Creates an isolated `.venv/` in the project root
3. Resolves and installs all dependencies declared in `pyproject.toml`
4. Generates a `poetry.lock` file that pins exact versions for reproducibility

It replaces the manual workflow of `python -m venv` + `pip install` + `requirements.txt`.

### Team configuration

One-time setup so Poetry creates the `.venv/` inside each project directory (instead of a hidden cache folder):

```bash
poetry config virtualenvs.in-project true
```

This makes the venv visible in the project root, which VS Code auto-detects as the interpreter.

> The setup scripts ([§ 1.9](#19--automated-setup-scripts)) already run this command.

### Quick start

```bash
git clone https://github.com/org/my-project.git
cd my-project
poetry install                  # creates .venv/ + installs everything
source .venv/bin/activate       # or: poetry shell
```

### Rules

| Rule | Details |
|------|---------|
| One venv per project | Always. Never share environments between projects |
| Location | `.venv/` in the project root (set via `virtualenvs.in-project true`) |
| Git | Add `.venv/` to `.gitignore`. Commit `pyproject.toml` and `poetry.lock` |
| Installing packages | Always via `poetry add`, never `pip install` directly |
| Naming | Always `.venv`, for consistency across the team |
| System Python | Never install packages into it |

> **Poetry Guide:** For detailed usage (adding/removing packages, dependency groups, scripts, publishing, monorepo patterns, and more), see the [Poetry Guide](TODO_POETRY_GUIDE_LINK).

---

## 1.5 — VS Code Setup

VS Code is the standard IDE for the team. A detailed catalog of all required and recommended extensions lives in [`vscode_extensions.md`](vscode_extensions.md).

### Mandatory Extensions

| Extension | ID | Purpose |
|-----------|----|---------|
| Python | `ms-python.python` | Core Python support |
| Pylance | `ms-python.vscode-pylance` | Type checking & IntelliSense |
| Ruff | `charliermarsh.ruff` | Linting + formatting (replaces black, isort, flake8) |
| Python Debugger | `ms-python.debugpy` | Debugging |
| Jupyter | `ms-toolsai.jupyter` | Notebook support |
| GitLens | `eamodio.gitlens` | Git blame, history, file annotations |
| Claude Code | `anthropic.claude-code` | AI coding assistant |
| autoDocstring | `njpwerner.autodocstring` | Generate Google Style docstrings |
| Excalidraw | `pomdtr.excalidraw-editor` | Whiteboard / architecture diagrams inside VS Code |
| WSL | `ms-vscode-remote.remote-wsl` | Develop inside WSL from VS Code on Windows |

### Recommended (optional)

| Extension | ID | Purpose |
|-----------|----|---------|
| Find It Faster | `tomrijndorp.find-it-faster` | Fuzzy file/content search powered by `fd` + `rg` |
| Rainbow CSV | `mechatroner.rainbow-csv` | Color-coded columns in CSV/TSV files |
| Excel Viewer | `GrapeCity.gc-excelviewer` | Read-only `.xlsx`/`.csv` viewer |

> See [`vscode_extensions.md`](vscode_extensions.md) for the full catalog with detailed documentation, shortcuts, configuration tips, a bulk install script, and an `extensions.json` template.

### Shared VS Code Settings

These settings ensure the entire team uses the same formatting, linting, and editor behavior. Copy to `.vscode/settings.json` in every project:

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

What each setting does:

| Setting | Effect |
|---------|--------|
| `editor.formatOnSave` | Automatically formats the file every time you save |
| `editor.defaultFormatter: ruff` | Uses Ruff as the formatter for Python files |
| `editor.tabSize: 4` | 4-space indentation (PEP 8 standard) |
| `source.fixAll` | Applies all auto-fixable lint rules on save |
| `source.organizeImports` | Sorts and groups imports on save (replaces isort) |
| `ruff.lineLength: 120` | Maximum line length. Team standard is 120 characters |
| `python.analysis.typeCheckingMode: basic` | Pylance checks type hints at a basic level (catches common errors without being too strict) |
| `autoDocstring.docstringFormat: google` | Generates docstrings in Google Style format |
| `files.trimTrailingWhitespace` | Removes trailing spaces on save (avoids noisy git diffs) |
| `files.insertFinalNewline` | Ensures every file ends with a newline (POSIX standard) |
| `files.exclude` | Hides `.venv/`, `__pycache__/`, and cache folders from the VS Code explorer |

> See the [`debug/`](debug/) folder for a 3-part debugging masterclass.

### Bulk Install Script

```bash
# === Mandatory ===
code --install-extension ms-python.python
code --install-extension ms-python.vscode-pylance
code --install-extension charliermarsh.ruff
code --install-extension ms-python.debugpy
code --install-extension ms-toolsai.jupyter
code --install-extension eamodio.gitlens
code --install-extension anthropic.claude-code
code --install-extension njpwerner.autodocstring
code --install-extension pomdtr.excalidraw-editor
code --install-extension ms-vscode-remote.remote-wsl

# === Optional ===
code --install-extension tomrijndorp.find-it-faster
code --install-extension mechatroner.rainbow-csv
code --install-extension GrapeCity.gc-excelviewer
```

---

## 1.6 — Docker for Development

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

## 1.7 — Environment Variables & Secrets

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

## 1.8 — AI-Assisted Coding Tools

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

## 1.9 — Automated Setup Scripts

Ready-to-use scripts that install the full dev environment from scratch. Each script handles: system dependencies, pyenv, Python, Poetry, pre-commit, and VS Code extensions.

| OS | Script | Usage |
|----|--------|-------|
| **macOS** | [`scripts/setup_macos.sh`](scripts/setup_macos.sh) | `chmod +x scripts/setup_macos.sh && ./scripts/setup_macos.sh` |
| **Windows (WSL)** | [`scripts/setup_wsl.sh`](scripts/setup_wsl.sh) | `chmod +x scripts/setup_wsl.sh && ./scripts/setup_wsl.sh` |

Both scripts accept an optional Python version argument: `./scripts/setup_macos.sh 3.12.3`

> **Windows users:** Install WSL 2 first ([§ 1.2.1](#121--wsl-setup-guide-windows)), then run `setup_wsl.sh`.

---

## Project Setup — Step by Step

This is the sequence to set up a new project from scratch, combining all the tools covered in this module.

### 1. Create the project and pin the Python version

```bash
mkdir my-project && cd my-project
pyenv local 3.11.9          # creates .python-version
```

### 2. Initialize Poetry

```bash
poetry init                 # interactive — creates pyproject.toml
poetry install              # creates .venv/ and poetry.lock
```

### 3. Add project configuration files

```bash
# Git
git init
cp /path/to/templates/.gitignore .gitignore

# VS Code settings
mkdir -p .vscode
cp /path/to/templates/.vscode/settings.json .vscode/settings.json

# Environment variables
cp /path/to/templates/.env.example .env.example
cp .env.example .env        # fill in local values

# AI coding instructions
mkdir -p .github
cp /path/to/templates/.github/copilot-instructions.md .github/copilot-instructions.md
ln -s .github/copilot-instructions.md CLAUDE.md

# Pre-commit hooks
cp /path/to/templates/.pre-commit-config.yaml .pre-commit-config.yaml
pre-commit install
```

### Resulting directory structure

```
my-project/
├── .github/
│   └── copilot-instructions.md   ← AI coding instructions (Copilot reads this)
├── .vscode/
│   └── settings.json             ← shared editor settings (§ 1.5)
├── .venv/                        ← virtual environment (created by Poetry, in .gitignore)
├── src/
│   └── my_project/
│       └── __init__.py
├── tests/
│   └── __init__.py
├── .env                          ← local secrets (in .gitignore)
├── .env.example                  ← template showing expected variables (committed)
├── .gitignore
├── .python-version               ← pinned Python version, e.g. "3.11.9" (committed)
├── .pre-commit-config.yaml       ← pre-commit hook configuration (committed)
├── CLAUDE.md                     ← symlink → .github/copilot-instructions.md (committed)
├── pyproject.toml                ← project metadata + dependencies (committed)
└── poetry.lock                   ← exact resolved versions (committed)
```

| File | Committed to Git? | Created by |
|------|--------------------|------------|
| `.python-version` | Yes | `pyenv local <version>` |
| `pyproject.toml` | Yes | `poetry init` |
| `poetry.lock` | Yes | `poetry install` |
| `.venv/` | **No** (.gitignore) | `poetry install` |
| `.env` | **No** (.gitignore) | Manual (copy from `.env.example`) |
| `.env.example` | Yes | Manual (template) |
| `.vscode/settings.json` | Yes | Manual (copy from template) |
| `.github/copilot-instructions.md` | Yes | Manual (copy from template) |
| `CLAUDE.md` | Yes | `ln -s .github/copilot-instructions.md CLAUDE.md` |
| `.pre-commit-config.yaml` | Yes | Manual (copy from template) |

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
