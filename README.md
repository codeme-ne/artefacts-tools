# tools.neurohackingly.com

A collection of simple, single-file tools.

## How it works

Each tool is a single HTML file with an accompanying `.docs.md` file for metadata.

The build script (`build.sh`) generates an index page that lists all available tools.

## Adding a new tool

1. Create a new HTML file (e.g., `my-tool.html`)
2. Create a matching docs file (e.g., `my-tool.docs.md`) with a brief description
3. Run `./build.sh` to regenerate the index
4. Commit and push - GitHub Actions will deploy automatically

## Local development

```bash
# Install dependencies
python3 -m venv .venv
source .venv/bin/activate
pip install pyyaml jinja2 markdown beautifulsoup4

# Build the site
chmod +x build.sh
./build.sh

# View the generated site in dist/
```

## Deployment

The site automatically deploys to GitHub Pages via GitHub Actions when you push to the main branch.

Custom domain: tools.neurohackingly.com
