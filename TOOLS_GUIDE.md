# Tools Authoring Guide

Quick guide for adding new tools to this collection.

## File Convention

Each tool consists of **two files** in the repository root:

```
your-tool-name.html       # The tool itself
your-tool-name.docs.md    # Metadata and description
```

### Example: `hello-world.html` + `hello-world.docs.md`

## 1. Create the HTML Tool

Create `your-tool-name.html`:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Your Tool Name</title>
</head>
<body>
    <h1>Your Tool Name</h1>
    <!-- Your tool code here -->

    <footer>
        <a href="./">← Back to tools</a>
    </footer>
</body>
</html>
```

**Important:**
- Use a descriptive `<title>` tag (appears in index)
- Keep it **self-contained** (single file)
- Use relative link `./` for back navigation

## 2. Create the Documentation

Create `your-tool-name.docs.md`:

```markdown
A one-sentence description of what your tool does.

Optional longer description here...
```

**Important:**
- First non-heading line = description shown in index
- Keep it **short and clear** (1 sentence)

### Optional: Add Frontmatter (Metadata)

```markdown
---
category: Images
tags: [conversion, utility]
---

A one-sentence description of what your tool does.
```

**Available frontmatter:**
- `category` - Groups tools by category (enable in `_config.yml`)
- `tags` - List of tags (shown as badges)

## 3. Test Locally

```bash
# Install dependencies
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Build
./build.sh

# Check output
open dist/index.html  # macOS
xdg-open dist/index.html  # Linux
```

Your tool should appear in the index!

## 4. Commit and Push

```bash
git add your-tool-name.html your-tool-name.docs.md
git commit -m "Add: your tool name"
git push
```

GitHub Actions will automatically build and deploy.

## Optional: LLM-Generated Descriptions

If `.docs.md` is missing or empty, the build system can use **Claude** to generate a description automatically.

**Setup (optional):**
1. Go to GitHub repo → Settings → Secrets → Actions
2. Add secret: `ANTHROPIC_API_KEY` (your Anthropic API key)

**Behavior:**
- ✅ With API key: Auto-generates missing descriptions
- ✅ Without API key: Uses fallback "No description available"
- ✅ With `.docs.md`: Always prefers your description

## Tips

- **Keep tools simple** - Single-purpose, self-contained HTML files
- **Mobile-friendly** - Use `<meta name="viewport">` tag
- **Descriptive names** - Use kebab-case: `image-converter.html`
- **Test locally first** - Run `./build.sh` before committing

## Configuration

Edit `_config.yml` to customize:

```yaml
title: Your Site Title
description: Your site description
repo_url: https://github.com/you/repo  # For colophon commit links
categories_enabled: true  # Group by category
```

## Need Help?

Check existing tools in the repo root for examples!
