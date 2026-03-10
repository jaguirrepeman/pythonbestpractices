#!/bin/bash
# setup_macos.sh — One-command dev environment setup for macOS
# Usage: chmod +x setup_macos.sh && ./setup_macos.sh
set -euo pipefail

PYTHON_VERSION="${1:-3.11.9}"

echo "=== Dev Environment Setup (macOS) ==="
echo "Python version: ${PYTHON_VERSION}"
echo ""

# ── 1. Homebrew ──────────────────────────────────────────────
if ! command -v brew &>/dev/null; then
    echo "▸ Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    # Add to PATH for Apple Silicon
    if [[ -f /opt/homebrew/bin/brew ]]; then
        eval "$(/opt/homebrew/bin/brew shellenv)"
    fi
else
    echo "▸ Homebrew already installed — updating..."
    brew update
fi

# ── 2. System dependencies ───────────────────────────────────
echo "▸ Installing system dependencies..."
brew install git pyenv wget curl jq fd ripgrep fzf

# ── 3. pyenv — install Python ────────────────────────────────
echo "▸ Installing Python ${PYTHON_VERSION} via pyenv..."

# Ensure pyenv shell integration
export PYENV_ROOT="${HOME}/.pyenv"
export PATH="${PYENV_ROOT}/bin:${PATH}"
eval "$(pyenv init -)"

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

# ── 5. VS Code extensions ────────────────────────────────────
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
    echo "⚠  VS Code CLI ('code') not found — skipping extension install."
    echo "   Open VS Code → Cmd+Shift+P → 'Shell Command: Install code command in PATH'"
fi

# ── Done ──────────────────────────────────────────────────────
echo ""
echo "=== ✅ Setup complete ==="
echo ""
echo "Next steps:"
echo "  cd your-project"
echo "  poetry install          # creates .venv/ and installs dependencies"
echo "  source .venv/bin/activate"
echo "  pre-commit install"
