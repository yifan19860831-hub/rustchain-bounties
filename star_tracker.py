#!/usr/bin/env python3
"""
GitHub Star Tracker - Track Scottcjn repo stars over time
Bounty: https://github.com/Scottcjn/rustchain-bounties/issues/1110
"""

from __future__ import annotations

import sqlite3
import requests
import json
from datetime import datetime, date
import os
from typing import List, Dict, Any, Optional, Tuple

# Configuration
DB_PATH: str = "star_tracker.db"
OWNER: str = "Scottcjn"
GITHUB_TOKEN: str = os.environ.get("GITHUB_TOKEN", "")

# API Endpoints
GITHUB_API: str = "https://api.github.com"


def init_db() -> sqlite3.Connection:
    """Initialize SQLite database."""
    conn: sqlite3.Connection = sqlite3.connect(DB_PATH)
    cursor: sqlite3.Cursor = conn.cursor()
    
    # Create tables
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS repos (
            id INTEGER PRIMARY KEY,
            name TEXT UNIQUE NOT NULL,
            full_name TEXT,
            stars INTEGER,
            forks INTEGER,
            description TEXT,
            updated_at TEXT
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS snapshots (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            repo_name TEXT NOT NULL,
            stars INTEGER NOT NULL,
            recorded_at TEXT NOT NULL,
            FOREIGN KEY (repo_name) REFERENCES repos (name)
        )
    """)
    
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_snapshot_date 
        ON snapshots (recorded_at)
    """)
    
    conn.commit()
    return conn


def get_all_repos() -> List[Dict[str, Any]]:
    """Fetch all repos for the owner."""
    repos: List[Dict[str, Any]] = []
    page: int = 1
    per_page: int = 100
    
    while True:
        url: str = f"{GITHUB_API}/users/{OWNER}/repos"
        params: Dict[str, Any] = {"per_page": per_page, "page": page, "type": "all"}
        headers: Dict[str, str] = {"Accept": "application/vnd.github.v3+json"}
        if GITHUB_TOKEN:
            headers["Authorization"] = f"token {GITHUB_TOKEN}"
        
        resp: requests.Response = requests.get(url, params=params, headers=headers)
        
        if resp.status_code != 200:
            print(f"Error fetching repos: {resp.status_code} - {resp.text}")
            break
        
        data: List[Dict[str, Any]] = resp.json()
        if not data:
            break
            
        repos.extend(data)
        
        if len(data) < per_page:
            break
        page += 1
    
    return repos


def save_repos(conn: sqlite3.Connection, repos: List[Dict[str, Any]]) -> None:
    """Save repo info to database."""
    cursor: sqlite3.Cursor = conn.cursor()
    
    for repo in repos:
        cursor.execute("""
            INSERT OR REPLACE INTO repos 
            (id, name, full_name, stars, forks, description, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            repo["id"],
            repo["name"],
            repo["full_name"],
            repo["stargazers_count"],
            repo["forks_count"],
            repo["description"],
            repo["updated_at"]
        ))
    
    conn.commit()
    print(f"Saved {len(repos)} repos")


def record_snapshot(conn: sqlite3.Connection) -> None:
    """Record current star counts."""
    cursor: sqlite3.Cursor = conn.cursor()
    now: str = datetime.now().isoformat()
    
    cursor.execute("SELECT name, stars FROM repos")
    repos: List[Tuple[str, int]] = cursor.fetchall()
    
    for name, stars in repos:
        cursor.execute("""
            INSERT INTO snapshots (repo_name, stars, recorded_at)
            VALUES (?, ?, ?)
        """, (name, stars, now))
    
    conn.commit()
    print(f"Recorded snapshot for {len(repos)} repos at {now}")


def get_stats(conn: sqlite3.Connection) -> Dict[str, Any]:
    """Get statistics."""
    cursor: sqlite3.Cursor = conn.cursor()
    
    # Total stars
    cursor.execute("SELECT SUM(stars) FROM repos")
    total_stars: int = cursor.fetchone()[0] or 0
    
    # Total repos
    cursor.execute("SELECT COUNT(*) FROM repos")
    total_repos: int = cursor.fetchone()[0]
    
    # Latest snapshot for each repo
    cursor.execute("""
        SELECT r.name, r.stars, s.recorded_at
        FROM repos r
        JOIN (
            SELECT repo_name, MAX(recorded_at) as max_date
            FROM snapshots
            GROUP BY repo_name
        ) latest ON r.name = latest.repo_name
        JOIN snapshots s ON r.name = s.repo_name AND s.recorded_at = latest.max_date
        ORDER BY r.stars DESC
        LIMIT 10
    """)
    top_repos: List[Tuple[str, int, str]] = cursor.fetchall()
    
    # Get yesterday's stars for delta
    cursor.execute("""
        SELECT repo_name, stars
        FROM snapshots
        WHERE date(recorded_at) = date('now', '-1 day')
    """)
    yesterday: Dict[str, int] = {row[0]: row[1] for row in cursor.fetchall()}
    
    # Calculate deltas
    top_with_delta: List[Tuple[str, int, int]] = []
    for name, stars, _ in top_repos:
        yesterday_stars: int = yesterday.get(name, stars)
        delta: int = stars - yesterday_stars
        top_with_delta.append((name, stars, delta))
    
    return {
        "total_stars": total_stars,
        "total_repos": total_repos,
        "top_repos": top_with_delta,
        "yesterday": yesterday
    }


def print_dashboard(conn: sqlite3.Connection) -> None:
    """Print CLI dashboard."""
    stats: Dict[str, Any] = get_stats(conn)
    
    print("\n" + "="*60)
    print(f"📊 GitHub Star Tracker - {OWNER}")
    print("="*60)
    print(f"Total Stars: ⭐ {stats['total_stars']}")
    print(f"Total Repos: 📁 {stats['total_repos']}")
    print()
    print("🏆 Top 10 Repos by Stars:")
    print("-"*50)
    print(f"{'Repo':<35} {'Stars':>8} {'Delta':>8}")
    print("-"*50)
    
    for name, stars, delta in stats['top_repos']:
        delta_str: str = f"+{delta}" if delta > 0 else str(delta)
        print(f"{name:<35} {stars:>8} {delta_str:>8}")
    
    print("="*60)


def generate_html_report(conn: sqlite3.Connection) -> None:
    """Generate HTML report with chart."""
    cursor: sqlite3.Cursor = conn.cursor()
    stats: Dict[str, Any] = get_stats(conn)
    
    # Get historical data for chart
    cursor.execute("""
        SELECT date(recorded_at) as day, SUM(stars) as total
        FROM snapshots
        GROUP BY day
        ORDER BY day
        LIMIT 30
    """)
    history: List[Tuple[str, int]] = cursor.fetchall()
    
    html = f"""<!DOCTYPE html>
<html>
<head>
    <title>GitHub Star Tracker - {OWNER}</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; 
               max-width: 900px; margin: 0 auto; padding: 20px; 
               background: #0d1117; color: #c9d1d9; }}
        h1 {{ color: #58a6ff; }}
        .stat {{ display: inline-block; margin: 10px 20px; }}
        .stat-value {{ font-size: 2em; font-weight: bold; color: #58a6ff; }}
        .stat-label {{ color: #8b949e; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
        th, td {{ padding: 10px; text-align: left; border-bottom: 1px solid #30363d; }}
        th {{ color: #8b949e; }}
        .delta-pos {{ color: #3fb950; }}
        .delta-neg {{ color: #f85149; }}
    </style>
</head>
<body>
    <h1>📊 GitHub Star Tracker - {OWNER}</h1>
    
    <div class="stat">
        <div class="stat-value">{stats['total_stars']}</div>
        <div class="stat-label">Total Stars ⭐</div>
    </div>
    <div class="stat">
        <div class="stat-value">{stats['total_repos']}</div>
        <div class="stat-label">Total Repos 📁</div>
    </div>
    
    <h2>🏆 Top 10 Repos</h2>
    <table>
        <tr><th>Repo</th><th>Stars</th><th>24h Change</th></tr>
"""
    
    for name, stars, delta in stats['top_repos']:
        delta_class: str = "delta-pos" if delta >= 0 else "delta-neg"
        delta_str: str = f"+{delta}" if delta >= 0 else str(delta)
        html += f"<tr><td>{name}</td><td>{stars}</td><td class='{delta_class}'>{delta_str}</td></tr>\n"
    
    html += """
    </table>
    
    <p>Generated at: """ + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + """</p>
</body>
</html>"""
    
    with open("star_tracker.html", "w") as f:
        f.write(html)
    
    print("Generated: star_tracker.html")


def main() -> None:
    """Main entry point."""
    conn: sqlite3.Connection = init_db()
    
    # Fetch and save repos
    print("Fetching repos...")
    repos: List[Dict[str, Any]] = get_all_repos()
    print(f"Found {len(repos)} repos")
    save_repos(conn, repos)
    
    # Record snapshot
    print("Recording snapshot...")
    record_snapshot(conn)
    
    # Show dashboard
    print_dashboard(conn)
    
    # Generate HTML
    stats: Dict[str, Any] = get_stats(conn)
    generate_html_report(conn)
    
    conn.close()
    print("\nDone!")


if __name__ == "__main__":
    main()
