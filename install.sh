#!/usr/bin/env bash

set -euo pipefail

REPO="PIGU-PPPgu/harness-skill-v2"
INSTALL_DIR="${HOME}/.local/bin"

echo "Installing Harness Engineering..."

mkdir -p "$INSTALL_DIR"

# harness CLI
curl -fsSL "https://raw.githubusercontent.com/${REPO}/main/harness" \
  -o "${INSTALL_DIR}/harness"
chmod +x "${INSTALL_DIR}/harness"

# harness-daemon
curl -fsSL "https://raw.githubusercontent.com/${REPO}/main/bin/harness-daemon" \
  -o "${INSTALL_DIR}/harness-daemon"
chmod +x "${INSTALL_DIR}/harness-daemon"

# Python src modules
SRC_DIR="${INSTALL_DIR}/../lib/harness"
mkdir -p "${SRC_DIR}/checks"
for f in harness_runtime harness_check agent_loop; do
  curl -fsSL "https://raw.githubusercontent.com/${REPO}/main/src/${f}.py" \
    -o "${SRC_DIR}/${f}.py"
done
for f in __init__ audit garden golden_rules; do
  curl -fsSL "https://raw.githubusercontent.com/${REPO}/main/src/checks/${f}.py" \
    -o "${SRC_DIR}/checks/${f}.py"
done

# PATH check
if [[ ":$PATH:" != *":${INSTALL_DIR}:"* ]]; then
  echo ""
  echo "Add to your shell config (~/.zshrc or ~/.bashrc):"
  echo "  export PATH=\"\$PATH:${INSTALL_DIR}\""
fi

echo ""
echo "Done. Run: harness init"
