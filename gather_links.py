#!/usr/bin/env python3
"""Gather tool metadata and links for site generation.

Scans HTML files, extracts metadata from .docs.md files, and optionally
uses LLM to generate descriptions if missing.
"""
import json
import os
import re
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Optional

import yaml


@dataclass
class ToolMetadata:
    """Metadata for a single tool."""
    slug: str
    title: str
    description: str
    url: str
    category: Optional[str] = None
    tags: list[str] = None

    def __post_init__(self):
        if self.tags is None:
            self.tags = []


def extract_title_from_html(html_path: Path) -> str:
    """Extract title from HTML <title> tag."""
    try:
        content = html_path.read_text('utf-8')
        match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE | re.DOTALL)
        if match:
            return match.group(1).strip()
    except Exception as e:
        print(f"Warning: Could not extract title from {html_path}: {e}")

    # Fallback to filename
    return html_path.stem.replace('-', ' ').title()


def parse_frontmatter(content: str) -> tuple[dict, str]:
    """Parse YAML frontmatter from markdown content.

    Returns:
        Tuple of (frontmatter_dict, remaining_content)
    """
    if not content.startswith('---'):
        return {}, content

    try:
        # Find closing ---
        parts = content.split('---', 2)
        if len(parts) < 3:
            return {}, content

        frontmatter = yaml.safe_load(parts[1]) or {}
        remaining = parts[2].strip()
        return frontmatter, remaining
    except Exception as e:
        print(f"Warning: Could not parse frontmatter: {e}")
        return {}, content


def extract_description_from_docs(docs_path: Path) -> tuple[str, dict]:
    """Extract description and metadata from .docs.md file.

    Returns:
        Tuple of (description, metadata_dict)
    """
    if not docs_path.exists():
        return "", {}

    try:
        content = docs_path.read_text('utf-8').strip()
        frontmatter, body = parse_frontmatter(content)

        # Find first non-empty, non-heading line
        for line in body.splitlines():
            line = line.strip()
            if line and not line.startswith('#'):
                return line, frontmatter

        return "", frontmatter
    except Exception as e:
        print(f"Warning: Could not read {docs_path}: {e}")
        return "", {}


def generate_description_with_llm(html_path: Path, title: str) -> Optional[str]:
    """Generate description using Anthropic LLM if API key available.

    Returns:
        Generated description or None if unavailable/failed
    """
    api_key = os.environ.get('ANTHROPIC_API_KEY')
    dry_run = os.environ.get('LLM_DRY_RUN', '').lower() == 'true'

    if not api_key or dry_run:
        return None

    try:
        from anthropic import Anthropic

        # Read HTML content for context
        html_content = html_path.read_text('utf-8')[:2000]  # First 2KB

        client = Anthropic(api_key=api_key)
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=150,
            messages=[{
                "role": "user",
                "content": f"""Generate a concise 1-sentence description for this web tool.

Title: {title}
HTML snippet:
{html_content}

Return ONLY the description, no preamble."""
            }]
        )

        description = message.content[0].text.strip()
        print(f"  → LLM generated description for {html_path.name}")
        return description

    except ImportError:
        print("  → anthropic package not installed, skipping LLM")
        return None
    except Exception as e:
        print(f"  → LLM generation failed: {e}")
        return None


def gather_tools() -> list[ToolMetadata]:
    """Scan directory and gather metadata for all tools.

    Returns:
        List of ToolMetadata objects
    """
    tools = []
    html_files = sorted([
        f for f in Path('.').glob('*.html')
        if f.name != 'index.html'
    ])

    print(f"Found {len(html_files)} tool(s)")

    for html_file in html_files:
        slug = html_file.stem
        title = extract_title_from_html(html_file)

        # Try to get description from .docs.md
        docs_file = html_file.with_suffix('.docs.md')
        description, metadata = extract_description_from_docs(docs_file)

        # Fallback to LLM if no description
        if not description:
            print(f"  {slug}: No description in .docs.md, trying LLM...")
            llm_desc = generate_description_with_llm(html_file, title)
            description = llm_desc or "No description available."

        tools.append(ToolMetadata(
            slug=slug,
            title=title,
            description=description,
            url=html_file.name,
            category=metadata.get('category'),
            tags=metadata.get('tags', [])
        ))

    return tools


def main():
    """Main entry point."""
    print("=== Gathering tool metadata ===")

    tools = gather_tools()

    # Write to JSON for other build scripts
    output_path = Path('tools.json')
    with output_path.open('w', encoding='utf-8') as f:
        json.dump(
            [asdict(tool) for tool in tools],
            f,
            indent=2,
            ensure_ascii=False
        )

    print(f"✓ Wrote {len(tools)} tool(s) to {output_path}")


if __name__ == '__main__':
    main()
