#!/bin/bash
# setup_wsl.sh — One-command dev environment setup for WSL (Ubuntu) on Windows
# Usage: chmod +x setup_wsl.sh && ./setup_wsl.sh
#
# Prerequisites:
#   WSL 2 with Ubuntu must already be installed. See the WSL setup guide
#   in 01_dev_env_setup/README.md § 1.2.1 for step-by-step instructions.
set -euo pipefail

PYTHON_VERSION="${1:-3.11.9}"

echo "=== Dev Environment Setup (WSL / Ubuntu) ==="
echo "Python version: ${PYTHON_VERSION}"
echo ""

# ── 1. System packages (apt) ─────────────────────────────────
echo "▸ Updating apt and installing system dependencies..."
sudo apt update && sudo apt upgrade -y

# Dev tools
sudo apt install -y build-essential git curl wget jq fd-find ripgrep fzf unzip

# pyenv build dependencies — required to compile Python from source
# (see https://github.com/pyenv/pyenv/wiki#suggested-build-environment)
sudo apt install -y \
    libssl-dev \
    zlib1g-dev \
    libbz2-dev \
    libreadline-dev \
    libsqlite3-dev \
    libncursesw5-dev \
    xz-utils \
    tk-dev \
    libxml2-dev \
    libxmlsec1-dev \
    libffi-dev \
    liblzma-dev

# ── 2. Homebrew (Linuxbrew) ──────────────────────────────────
if ! command -v brew &>/dev/null; then
    echo "▸ Installing Homebrew (Linuxbrew)..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    # Add to current session
    eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"
    # Persist in .bashrc
    echo 'eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"' >> "${HOME}/.bashrc"
else
    echo "▸ Homebrew already installed — updating..."
    brew update
fi

# ── 3. pyenv — install Python ────────────────────────────────
if ! command -v pyenv &>/dev/null; then
    echo "▸ Installing pyenv..."
    brew install pyenv

    # Shell integration
    {
        echo ''
        echo '# pyenv'
        echo 'export PYENV_ROOT="${HOME}/.pyenv"'
        echo 'export PATH="${PYENV_ROOT}/bin:${PATH}"'
        echo 'eval "$(pyenv init -)"'
    } >> "${HOME}/.bashrc"

    export PYENV_ROOT="${HOME}/.pyenv"
    export PATH="${PYENV_ROOT}/bin:${PATH}"
    eval "$(pyenv init -)"
fi

echo "▸ Installing Python ${PYTHON_VERSION} via pyenv..."
pyenv install -s "${PYTHON_VERSION}"
pyenv global "${PYTHON_VERSION}"

echo "  Python location: $(which python)"
echo "  Python version:  $(python --version)"

# ── 4. pip essentials ─────────────────────────────────────────
echo "▸ Installing pip essentials..."
pip install --upgrade pip
pip install poetry pre-commit

# Configure Poetry to create .venv inside projects
poetry config virtualenvs.in-project true

# ── 5. VS Code extensions (via Windows VS Code) ──────────────
# VS Code on Windows + WSL extension handles the connection.
# The 'code' command should be available in WSL if VS Code is installed on Windows.
if command -v code &>/dev/null; then
    echo "▸ Installing VS Code extensions..."
    extensions=(
        ms-python.python
        ms-python.vscode-pylance
        ms-python.debugpy
        charliermarsh.ruff
        ms-toolsai.jupyter
        ms-toolsai.datawrangler
        GitHub.copilot
        anthropic.claude-code
        njpwerner.autodocstring
        eamodio.gitlens
        snowflake.snowflake-vsc
        yzhang.markdown-all-in-one
        bierner.markdown-mermaid
        pomdtr.excalidraw-editor
        tomrijndorp.find-it-faster
        ms-vscode-remote.remote-wsl
    )
    for ext in "${extensions[@]}"; do
        code --install-extension "$ext" --force 2>/dev/null || true
    done
else
    echo "⚠  VS Code CLI ('code') not found in WSL."
    echo "   Open VS Code on Windows → install the 'WSL' extension → reopen terminal."
fi

# ── 6. Git config (use Windows credential manager) ───────────
echo "▸ Configuring Git credential manager..."
git config --global credential.helper "/mnt/c/Program\ Files/Git/mingw64/bin/git-credential-manager.exe" 2>/dev/null || true

# ── Done ──────────────────────────────────────────────────────
echo ""
echo "=== ✅ Setup complete ==="
echo ""
echo "Next steps:"
echo "  source ~/.bashrc"
echo "  cd your-project"
echo "  poetry install          # creates .venv/ and installs dependencies"
echo "  source .venv/bin/activate"
echo "  pre-commit install"
echo ""
echo "To open VS Code from WSL:"
echo "  code ."
