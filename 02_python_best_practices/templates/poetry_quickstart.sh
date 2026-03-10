#!/bin/bash
# poetry_quickstart.sh - Bootstrap a new Python project with Poetry + src/ layout
# Usage: ./poetry_quickstart.sh <project-name>
set -euo pipefail

PROJECT_NAME="${1:?Usage: ./poetry_quickstart.sh <project-name>}"
PYTHON_VERSION="${2:-3.11}"

echo "🚀 Creating project '${PROJECT_NAME}' with Python ${PYTHON_VERSION}..."

# Create directory structure
mkdir -p "${PROJECT_NAME}/src/${PROJECT_NAME}"
mkdir -p "${PROJECT_NAME}/tests/unit"
mkdir -p "${PROJECT_NAME}/tests/integration"
mkdir -p "${PROJECT_NAME}/notebooks"
mkdir -p "${PROJECT_NAME}/scripts"
mkdir -p "${PROJECT_NAME}/docs"
mkdir -p "${PROJECT_NAME}/.github/workflows"
mkdir -p "${PROJECT_NAME}/.vscode"

cd "${PROJECT_NAME}"

# Initialize Poetry
poetry init \
  --name "${PROJECT_NAME}" \
  --python "^${PYTHON_VERSION}" \
  --no-interaction

# Configure Poetry to use in-project venv
poetry config virtualenvs.in-project true

# Add dev dependencies
poetry add --group dev \
  pytest pytest-cov \
  ruff mypy \
  pre-commit \
  sphinx sphinx-autodoc-typehints sphinx-rtd-theme myst-parser

# Create source files
cat > "src/${PROJECT_NAME}/__init__.py" << 'EOF'
"""Top-level package."""

__version__ = "0.1.0"
EOF

touch "src/${PROJECT_NAME}/py.typed"

# Create conftest
cat > "tests/conftest.py" << 'EOF'
"""Shared test fixtures."""

import pytest
EOF

touch "tests/unit/__init__.py"
touch "tests/integration/__init__.py"

# Create .gitignore
cat > ".gitignore" << 'EOF'
# Python
__pycache__/
*.py[cod]
*.egg-info/
dist/
build/
.eggs/

# Virtual environments
.venv/
venv/

# IDE
.vscode/settings.json
.idea/

# Environment
.env

# OS
.DS_Store
Thumbs.db

# Docs build
docs/build/

# Coverage
htmlcov/
.coverage
coverage.xml
EOF

# Create .env.example
cat > ".env.example" << 'EOF'
# Copy to .env and fill in values (never commit .env)
# DATABASE_URL=snowflake://user:pass@account/db/schema
# API_KEY=your_key_here
EOF

# Create .python-version
echo "${PYTHON_VERSION}" > ".python-version"

# Create README
cat > "README.md" << EOF
# ${PROJECT_NAME}

## Setup

\`\`\`bash
# Install dependencies
poetry install

# Activate virtual environment
source .venv/bin/activate  # macOS/Linux
# .venv\\Scripts\\activate  # Windows

# Install pre-commit hooks
pre-commit install
\`\`\`

## Usage

\`\`\`python
from ${PROJECT_NAME} import __version__
print(__version__)
\`\`\`

## Tests

\`\`\`bash
pytest --cov=src/${PROJECT_NAME}
\`\`\`
EOF

# Install dependencies
poetry install

# Initialize git
git init
poetry run pre-commit install 2>/dev/null || true

echo ""
echo "✅ Project '${PROJECT_NAME}' created successfully!"
echo ""
echo "Next steps:"
echo "  cd ${PROJECT_NAME}"
echo "  source .venv/bin/activate"
echo "  code ."
