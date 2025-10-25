#!/usr/bin/env python3
"""Simple index generator for tools site."""
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import yaml

# Configuration defaults
DEFAULT_SITE_TITLE = 'Tools'
DEFAULT_SITE_DESCRIPTION = 'A collection of tools'
CONFIG_FILE = '_config.yml'
DIST_DIR = 'dist'
INDEX_FILE = 'index.html'

# CSS styling for the generated page
PAGE_STYLE = """
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
            line-height: 1.6;
            max-width: 800px;
            margin: 40px auto;
            padding: 0 20px;
            color: #24292e;
        }
        h1 {
            border-bottom: 1px solid #eaecef;
            padding-bottom: 10px;
        }
        .description {
            color: #586069;
            margin-bottom: 30px;
        }
        .tool {
            margin: 20px 0;
            padding: 15px;
            border: 1px solid #e1e4e8;
            border-radius: 6px;
        }
        .tool h2 {
            margin: 0 0 8px 0;
            font-size: 1.25em;
        }
        .tool a {
            color: #0366d6;
            text-decoration: none;
        }
        .tool a:hover {
            text-decoration: underline;
        }
        .tool-description {
            color: #586069;
            margin: 5px 0 0 0;
        }
"""


@dataclass
class Tool:
    """Represents a tool entry with metadata."""
    name: str
    title: str
    description: str
    url: str


def extract_title(html_path: Path) -> str:
    """Extract title from HTML file.

    Args:
        html_path: Path to the HTML file

    Returns:
        Extracted title or filename stem if not found
    """
    try:
        content = html_path.read_text('utf-8')
        match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE)
        if match:
            return match.group(1).strip()
    except Exception:
        pass
    return html_path.stem


def extract_description(docs_path: Path) -> str:
    """Extract first non-header paragraph from .docs.md file.

    Args:
        docs_path: Path to the .docs.md file

    Returns:
        First paragraph or empty string if not found
    """
    if not docs_path.exists():
        return ""

    try:
        content = docs_path.read_text('utf-8').strip()
        for line in content.splitlines():
            line = line.strip()
            if line and not line.startswith('#'):
                return line
    except Exception:
        pass

    return ""


def load_config() -> dict:
    """Load configuration from _config.yml.

    Returns:
        Configuration dictionary or empty dict if file doesn't exist
    """
    config_path = Path(CONFIG_FILE)
    if not config_path.exists():
        return {}

    with open(config_path, 'r') as f:
        return yaml.safe_load(f) or {}


def find_html_files() -> list[Path]:
    """Find all HTML files excluding index.html.

    Returns:
        Sorted list of HTML file paths
    """
    return sorted([
        f for f in Path('.').glob('*.html')
        if f.name != INDEX_FILE
    ])


def build_tool_list(html_files: list[Path]) -> list[Tool]:
    """Build list of Tool objects from HTML files.

    Args:
        html_files: List of HTML file paths

    Returns:
        List of Tool objects with metadata
    """
    tools = []
    for html_file in html_files:
        docs_file = html_file.with_suffix('.docs.md')
        tools.append(Tool(
            name=html_file.stem,
            title=extract_title(html_file),
            description=extract_description(docs_file),
            url=html_file.name
        ))
    return tools


def generate_tool_html(tool: Tool) -> str:
    """Generate HTML markup for a single tool.

    Args:
        tool: Tool object with metadata

    Returns:
        HTML string for the tool entry
    """
    return f"""
    <div class="tool">
        <h2><a href="{tool.url}">{tool.title}</a></h2>
        <p class="tool-description">{tool.description}</p>
    </div>
"""


def generate_index_html(site_title: str, site_description: str, tools: list[Tool]) -> str:
    """Generate complete index.html content.

    Args:
        site_title: Title for the site
        site_description: Description for the site
        tools: List of Tool objects

    Returns:
        Complete HTML document as string
    """
    html_parts = [
        f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{site_title}</title>
    <style>{PAGE_STYLE}
    </style>
</head>
<body>
    <h1>{site_title}</h1>
    <p class="description">{site_description}</p>
"""
    ]

    if tools:
        html_parts.extend(generate_tool_html(tool) for tool in tools)
    else:
        html_parts.append("""
    <p>No tools available yet.</p>
""")

    html_parts.append("""
</body>
</html>
""")

    return ''.join(html_parts)


def copy_html_files(html_files: list[Path], dist_dir: Path) -> None:
    """Copy HTML files to dist directory.

    Args:
        html_files: List of HTML file paths to copy
        dist_dir: Destination directory
    """
    for html_file in html_files:
        content = html_file.read_text('utf-8')
        (dist_dir / html_file.name).write_text(content, 'utf-8')


def main() -> None:
    """Main entry point for building the tools index."""
    # Load configuration
    config = load_config()
    site_title = config.get('title', DEFAULT_SITE_TITLE)
    site_description = config.get('description', DEFAULT_SITE_DESCRIPTION)

    # Find HTML files and build tool list
    html_files = find_html_files()
    tools = build_tool_list(html_files)

    # Generate index HTML
    html = generate_index_html(site_title, site_description, tools)

    # Write to dist/index.html
    dist_dir = Path(DIST_DIR)
    dist_dir.mkdir(exist_ok=True)
    (dist_dir / INDEX_FILE).write_text(html, 'utf-8')

    # Copy HTML files to dist
    copy_html_files(html_files, dist_dir)

    print(f"Built index with {len(tools)} tool(s)")


if __name__ == '__main__':
    main()
