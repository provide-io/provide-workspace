#!/usr/bin/env bash

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# GitHub organization
ORG="provide-io"

# List of repositories to clone
REPOS=(
    "provide-foundation"
    "provide-testkit"
    "pyvider"
    "pyvider-cty"
    "pyvider-hcl"
    "pyvider-rpcplugin"
    "pyvider-components"
    "flavorpack"
    "wrknv"
    "plating"
    "tofusoup"
    "supsrc"
    "provide-foundry"
    "terraform-provider-pyvider"
)

echo "=== provide-workenv Bootstrap ==="
echo

# Get the workspace root (parent of this script)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

echo "Workspace root: $WORKSPACE_ROOT"
echo

# Check prerequisites
echo "Checking prerequisites..."
if ! command -v git &> /dev/null; then
    echo -e "${RED}Error: git is not installed${NC}"
    exit 1
fi

if ! command -v gh &> /dev/null; then
    echo -e "${YELLOW}Warning: gh (GitHub CLI) is not installed${NC}"
    echo "You may need to authenticate manually for private repositories"
    USE_GH=false
else
    USE_GH=true
fi

echo -e "${GREEN}Prerequisites OK${NC}"
echo

# Clone repositories
cd "$WORKSPACE_ROOT"

for repo in "${REPOS[@]}"; do
    if [ -d "$repo" ]; then
        echo -e "${YELLOW}$repo already exists, skipping...${NC}"
    else
        echo "Cloning $repo..."
        if $USE_GH; then
            gh repo clone "$ORG/$repo" || {
                echo -e "${RED}Failed to clone $repo${NC}"
                continue
            }
        else
            git clone "https://github.com/$ORG/$repo.git" || {
                echo -e "${RED}Failed to clone $repo${NC}"
                continue
            }
        fi
        echo -e "${GREEN}$repo cloned successfully${NC}"
    fi
done

echo
echo -e "${GREEN}Bootstrap complete!${NC}"
echo
echo "Next steps:"
echo "  1. Run ./scripts/setup.sh to install dependencies"
echo "  2. Run ./scripts/validate.sh to verify your setup"
