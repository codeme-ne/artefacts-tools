#!/usr/bin/env python3
"""Simple index generator for tools site."""
import os
from pathlib import Path
import yaml
import re

def extract_title(html_path):
    """Extract title from HTML file."""
    try:
        content = html_path.read_text('utf-8')
        match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE)
        if match:
            return match.group(1).strip()
    except Exception:
        pass
    return html_path.stem

def extract_description(docs_path):
    """Extract first paragraph from .docs.md file."""
    if not docs_path.exists():
        return ""
    try:
        content = docs_path.read_text('utf-8').strip()
        lines = [line.strip() for line in content.splitlines() if line.strip() and not line.strip().startswith('#')]
        return lines[0] if lines else ""
    except Exception:
        return ""

def main():
    # Load config
    config = {}
    if Path('_config.yml').exists():
        with open('_config.yml', 'r') as f:
            config = yaml.safe_load(f) or {}
    
    site_title = config.get('title', 'Tools')
    site_description = config.get('description', 'A collection of tools')
    
    # Find all HTML files (excluding index.html)
    html_files = sorted([f for f in Path('.').glob('*.html') if f.name != 'index.html'])
    
    # Build tools list
    tools = []
    for html_file in html_files:
        docs_file = html_file.with_suffix('.docs.md')
        tools.append({
            'name': html_file.stem,
            'title': extract_title(html_file),
            'description': extract_description(docs_file),
            'url': html_file.name
        })
    
    # Generate index.html
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{site_title}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
            line-height: 1.6;
            max-width: 800px;
            margin: 40px auto;
            padding: 0 20px;
            color: #24292e;
        }}
        h1 {{
            border-bottom: 1px solid #eaecef;
            padding-bottom: 10px;
        }}
        .description {{
            color: #586069;
            margin-bottom: 30px;
        }}
        .tool {{
            margin: 20px 0;
            padding: 15px;
            border: 1px solid #e1e4e8;
            border-radius: 6px;
        }}
        .tool h2 {{
            margin: 0 0 8px 0;
            font-size: 1.25em;
        }}
        .tool a {{
            color: #0366d6;
            text-decoration: none;
        }}
        .tool a:hover {{
            text-decoration: underline;
        }}
        .tool-description {{
            color: #586069;
            margin: 5px 0 0 0;
        }}
    </style>
</head>
<body>
    <h1>{site_title}</h1>
    <p class="description">{site_description}</p>
"""
    
    if tools:
        for tool in tools:
            html += f"""
    <div class="tool">
        <h2><a href="{tool['url']}">{tool['title']}</a></h2>
        <p class="tool-description">{tool['description']}</p>
    </div>
"""
    else:
        html += """
    <p>No tools available yet.</p>
"""
    
    html += """
</body>
</html>
"""
    
    # Write to dist/index.html
    dist_dir = Path('dist')
    dist_dir.mkdir(exist_ok=True)
    
    (dist_dir / 'index.html').write_text(html, 'utf-8')
    
    # Copy HTML files to dist
    for html_file in html_files:
        content = html_file.read_text('utf-8')
        (dist_dir / html_file.name).write_text(content, 'utf-8')
    
    print(f"Built index with {len(tools)} tool(s)")

if __name__ == '__main__':
    main()
