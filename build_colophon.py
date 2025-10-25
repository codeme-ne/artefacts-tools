#!/usr/bin/env python3
"""Build colophon page from git history."""
import json
import subprocess
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional

import yaml


@dataclass
class Commit:
    """Git commit information."""
    hash: str
    short_hash: str
    author: str
    date: str
    message: str


def load_config() -> dict:
    """Load configuration from _config.yml."""
    config_path = Path('_config.yml')
    if not config_path.exists():
        return {}

    with open(config_path, 'r') as f:
        return yaml.safe_load(f) or {}


def get_git_commits(limit: int = 50) -> list[Commit]:
    """Get recent git commits.

    Args:
        limit: Maximum number of commits to retrieve

    Returns:
        List of Commit objects
    """
    try:
        # Git log format: hash|author|date|message
        result = subprocess.run(
            [
                'git', 'log',
                f'-{limit}',
                '--pretty=format:%H|%an|%ai|%s',
                '--no-merges'
            ],
            capture_output=True,
            text=True,
            check=True
        )

        commits = []
        for line in result.stdout.strip().split('\n'):
            if not line:
                continue

            parts = line.split('|', 3)
            if len(parts) != 4:
                continue

            hash_full, author, date_str, message = parts

            commits.append(Commit(
                hash=hash_full,
                short_hash=hash_full[:7],
                author=author,
                date=date_str,
                message=message
            ))

        return commits

    except subprocess.CalledProcessError as e:
        print(f"Warning: Could not get git log: {e}")
        return []
    except FileNotFoundError:
        print("Warning: git not found")
        return []


def format_date(date_str: str) -> str:
    """Format ISO date to readable format."""
    try:
        dt = datetime.fromisoformat(date_str)
        return dt.strftime('%B %d, %Y at %H:%M')
    except Exception:
        return date_str


def generate_colophon_html(site_title: str, commits: list[Commit], repo_url: Optional[str]) -> str:
    """Generate complete colophon HTML.

    Args:
        site_title: Site title from config
        commits: List of git commits
        repo_url: Repository URL (optional)

    Returns:
        Complete HTML document
    """
    commit_html = []

    for commit in commits:
        commit_link = f'<code>{commit.short_hash}</code>'
        if repo_url:
            commit_link = f'<a href="{repo_url}/commit/{commit.hash}">{commit_link}</a>'

        commit_html.append(f"""
    <div class="commit">
        <div class="commit-header">
            {commit_link} &mdash; <span class="author">{commit.author}</span>
        </div>
        <div class="message">{commit.message}</div>
        <div class="date">{format_date(commit.date)}</div>
    </div>
""")

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Colophon &mdash; {site_title}</title>
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
        .nav {{
            margin-bottom: 20px;
        }}
        .nav a {{
            color: #0366d6;
            text-decoration: none;
        }}
        .nav a:hover {{
            text-decoration: underline;
        }}
        .commit {{
            margin: 20px 0;
            padding: 15px;
            border: 1px solid #e1e4e8;
            border-radius: 6px;
        }}
        .commit-header {{
            font-weight: 600;
            margin-bottom: 5px;
        }}
        .commit code {{
            background: #f6f8fa;
            padding: 2px 6px;
            border-radius: 3px;
            font-size: 0.9em;
        }}
        .commit a {{
            color: #0366d6;
            text-decoration: none;
        }}
        .commit a:hover {{
            text-decoration: underline;
        }}
        .author {{
            color: #586069;
        }}
        .message {{
            margin: 8px 0;
        }}
        .date {{
            color: #586069;
            font-size: 0.9em;
        }}
    </style>
</head>
<body>
    <div class="nav">
        <a href="./">← Back to index</a>
    </div>

    <h1>Colophon</h1>
    <p class="description">
        Recent changes and updates to this collection of tools.
    </p>

{''.join(commit_html) if commits else '<p>No git history available.</p>'}

</body>
</html>
"""


def main():
    """Main entry point."""
    print("=== Building colophon ===")

    # Load config
    config = load_config()
    site_title = config.get('title', 'Tools')
    repo_url = config.get('repo_url')

    # Get commits
    commits = get_git_commits(limit=50)
    print(f"Found {len(commits)} commit(s)")

    # Generate HTML
    html = generate_colophon_html(site_title, commits, repo_url)

    # Write to dist/colophon.html
    dist_dir = Path('dist')
    dist_dir.mkdir(exist_ok=True)

    colophon_path = dist_dir / 'colophon.html'
    colophon_path.write_text(html, encoding='utf-8')

    print(f"✓ Wrote colophon to {colophon_path}")


if __name__ == '__main__':
    main()
