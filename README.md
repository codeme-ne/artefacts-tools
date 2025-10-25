# tools.neurohackingly.com

A collection of simple, single-file tools.

**Live site:** [tools.neurohackingly.com](https://tools.neurohackingly.com)

## Features

- ✅ **Convention-based** - Drop `tool.html` + `tool.docs.md`, auto-appears in index
- ✅ **Auto-deployment** - Push to `master` → GitHub Actions → Live
- ✅ **LLM-enhanced** - Optional Claude integration for auto-descriptions
- ✅ **Git history** - Automatic colophon with commit timeline
- ✅ **Reproducible** - Pinned dependencies, deterministic builds

## Quick Start: Adding a Tool

1. Create `your-tool.html` (self-contained, single file)
2. Create `your-tool.docs.md` (first line = description)
3. Commit & push → Auto-deploys!

**Detailed guide:** See [TOOLS_GUIDE.md](TOOLS_GUIDE.md)

## How It Works

### File Structure

```
your-tool.html          # The tool itself
your-tool.docs.md       # Metadata (description, category, tags)
```

### Build Pipeline

```
gather_links.py  →  build_index.py  →  build_colophon.py  →  dist/
```

1. **gather_links.py** - Scans tools, extracts metadata, optional LLM fallback
2. **build_index.py** - Generates index page with all tools
3. **build_colophon.py** - Creates git history page

### Optional: LLM Integration

Set `ANTHROPIC_API_KEY` secret in GitHub repo settings to auto-generate descriptions for tools missing `.docs.md`.

**Behavior:**
- With API key: Auto-generates missing descriptions
- Without API key: Uses fallback "No description available"
- With `.docs.md`: Always uses your description

## Local Development

```bash
# Setup
git clone https://github.com/codeme-ne/artefacts-tools.git
cd artefacts-tools
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Build
chmod +x build.sh
./build.sh

# View
open dist/index.html  # macOS
xdg-open dist/index.html  # Linux
start dist/index.html  # Windows
```

## Project Structure

```
.
├── *.html              # Tool files (e.g., hello-world.html)
├── *.docs.md           # Tool metadata (e.g., hello-world.docs.md)
├── build.sh            # Build orchestrator
├── gather_links.py     # Tool metadata collector
├── build_index.py      # Index page generator
├── build_colophon.py   # Git history page generator
├── _config.yml         # Site configuration
├── requirements.txt    # Pinned Python dependencies
└── dist/               # Build output (git-ignored)
    ├── index.html
    ├── colophon.html
    └── *.html          # Copied tools
```

## Configuration

Edit `_config.yml`:

```yaml
title: tools.neurohackingly.com
description: A collection of simple, single-file tools
repo_url: https://github.com/codeme-ne/artefacts-tools
domain: tools.neurohackingly.com
categories_enabled: false  # Group tools by category
```

## Deployment

**Branch:** `master` (default)

**Trigger:** Push or manual workflow dispatch

**GitHub Actions:**
1. Installs Python dependencies (cached)
2. Runs `./build.sh`
3. Deploys `dist/` to GitHub Pages

**Custom Domain:** Set in `CNAME` + DNS `CNAME tools → codeme-ne.github.io`

## Inspired By

This project follows patterns from [simonw/tools](https://github.com/simonw/tools) with enhancements:
- LLM integration for auto-descriptions
- Reproducible builds (pinned dependencies)
- Enhanced metadata (categories, tags)
- Git history colophon

## License

Individual tools may have their own licenses. The build system is MIT.
