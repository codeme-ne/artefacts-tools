#!/bin/bash
set -euo pipefail

echo "╔═══════════════════════════════════════╗"
echo "║  Building tools.neurohackingly.com    ║"
echo "╚═══════════════════════════════════════╝"
echo

# Create dist directory
echo "→ Creating dist/ directory..."
mkdir -p dist

# Step 1: Gather tool metadata
echo
echo "→ Step 1/3: Gathering tool metadata..."
python3 gather_links.py

# Smoke test: Check if any tools were found
if [ ! -f "tools.json" ]; then
    echo "❌ ERROR: tools.json not created!"
    echo "   Make sure gather_links.py ran successfully."
    exit 1
fi

TOOL_COUNT=$(python3 -c "import json; print(len(json.load(open('tools.json'))))")
if [ "$TOOL_COUNT" -eq 0 ]; then
    echo "⚠️  WARNING: No tools found!"
    echo "   Make sure you have *.html + *.docs.md files in the repo root."
fi

echo "   ✓ Found $TOOL_COUNT tool(s)"

# Step 2: Build index page
echo
echo "→ Step 2/3: Building index page..."
python3 build_index.py

# Step 3: Build colophon page
echo
echo "→ Step 3/3: Building colophon page..."
python3 build_colophon.py

# Copy CNAME if exists
if [ -f "CNAME" ]; then
    echo
    echo "→ Copying CNAME..."
    cp CNAME dist/
fi

# Final check
echo
echo "╔═══════════════════════════════════════╗"
echo "║  ✓ Build complete!                    ║"
echo "╚═══════════════════════════════════════╝"
echo
echo "Build artifacts:"
ls -lh dist/

echo
echo "Ready for deployment! 🚀"
