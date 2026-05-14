#!/usr/bin/env python3
"""
build-index.py — regenerate index.html from articles.json
Usage: python3 build-index.py

articles.json order: newest first (index 0 = latest)
- build_featured_grid: uses articles[0] (latest) + articles[1:4] (next 3)
- build_articles_grid: uses articles[4:7] (articles 5-7, 3 items for "Artikel Terbaru")
"""

import json
from pathlib import Path

SITE_DIR = Path(__file__).parent

def load_articles():
    with open(SITE_DIR / "articles.json", "r", encoding="utf-8") as f:
        return json.load(f)

def build_featured_grid(articles):
    """Featured = latest (index 0) + next 3 (index 1-3)."""
    featured = articles[0]
    side = articles[1:4]

    main = f'''<div class="featured-main" onclick="location.href='{featured['slug']}.html'">
      <div class="featured-main-thumb">
        <img src="{featured['cover']}" alt="{featured['title']}">
      </div>
      <span class="featured-main-tag">{featured['tag']}</span>
      <h2>{featured['title']}</h2>
      <p>{featured['description']}</p>
    </div>'''

    side_items = ""
    for a in side:
        side_items += f'''<article class="featured-side-item" onclick="location.href='{a['slug']}.html'" style="cursor:pointer">
        <span class="tag">{a['tag']}</span>
        <h3>{a['title']}</h3>
        <p>{a['readTime']}</p>
      </article>'''

    return f'''<div class="featured-grid">
{main}
<div class="featured-side">
{side_items}
</div>
</div>'''

def build_topic_buttons(tags):
    btns = "".join(f'''<button class="topic-btn">{t}</button>''' for t in sorted(tags))
    return f'''<div class="topics-list">
    <button class="topic-btn active">Semua</button>
    {btns}
  </div>'''

def build_articles_grid(articles):
    """Show articles 4-7 (next 3 after featured 1-3). newest = index 0."""
    cards = []
    # Featured uses index 0-3 (4 articles)
    # Artikel Terbaru shows next 3: index 4, 5, 6
    for a in articles[4:7]:
        cards.append(f'''<article class="article-card" onclick="location.href='{a['slug']}.html'" style="cursor:pointer">
      <div class="article-thumb">
        <img src="{a['cover']}" alt="{a['title']}">
      </div>
      <div class="article-info">
        <span class="tag">{a['tag']}</span>
        <h3>{a['title']}</h3>
        <p>{a['readTime']}</p>
      </div>
    </article>''')
    return "\n".join(cards)

def generate_index(articles):
    with open(SITE_DIR / "index.html", "r", encoding="utf-8") as f:
        html = f.read()

    # Collect unique tags (split on &middot;)
    tags = set()
    for a in articles:
        for t in a['tag'].replace('&middot;', '|').split('|'):
            t = t.strip()
            if t:
                tags.add(t)

    # ── 1. Featured grid (inside <section class="featured">) ─────────────
    # Find the section, then the grid div inside it
    feat_start = html.find('<section class="featured"')
    grid_div = html.find('<div class="featured-grid">', feat_start)
    grid_end = html.find('</div>', grid_div) + len('</div>')
    section_end = html.find('</section>', grid_end) + len('</section>')
    old = html[grid_div:section_end]
    html = html[:grid_div] + build_featured_grid(articles) + "\n</section>" + html[section_end:]

    # ── 2. Topics section ────────────────────────────────────────────────
    topics_start = html.find('<div class="topics" id="topics">')
    topics_end = html.find('</div>', topics_start) + len('</div>')
    old = html[topics_start:topics_end]
    html = html[:topics_start] + f'''<div class="topics" id="topics">
  <span class="topics-label">Telusuri:</span>
  {build_topic_buttons(tags)}
</div>''' + html[topics_end:]

    # ── 3. Articles grid (inside <section class="articles">) ─────────────
    art_start = html.find('<section class="articles">')
    grid_div = html.find('<div class="articles-grid">', art_start)
    grid_end = html.find('</div>', grid_div) + len('</div>')
    section_end = html.find('</section>', grid_end) + len('</section>')
    old = html[grid_div:section_end]
    html = html[:grid_div] + f'''<div class="articles-grid">
{build_articles_grid(articles)}
</div>
</section>''' + html[section_end:]

    with open(SITE_DIR / "index.html", "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Generated index.html — featured: {articles[0]['title']}, grid: {len(articles[4:7])} articles")

if __name__ == "__main__":
    articles = load_articles()
    generate_index(articles)