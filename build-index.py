#!/usr/bin/env python3
"""
build-index.py — regenerate index.html from articles.json
Usage: python3 build-index.py
"""

import json
from pathlib import Path

SITE_DIR = Path(__file__).parent

def load_articles():
    with open(SITE_DIR / "articles.json", "r", encoding="utf-8") as f:
        return json.load(f)

def build_featured_grid(articles):
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
    cards = []
    for a in articles[1:]:
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

    # 1. Featured grid
    start = html.find('<div class="featured-grid">')
    end = html.find('</div>', html.find('</div>', start)) + len('</div>')
    # find the closing of the section after the grid
    end = html.find('</section>', end) + len('</section>')
    old = html[start:end]
    html = html.replace(old, build_featured_grid(articles) + "\n</section>")

    # 2. Topics
    start = html.find('<div class="topics" id="topics">')
    end = html.find('</div>', start) + len('</div>')
    old = html[start:end]
    html = html.replace(old, f'''<div class="topics" id="topics">
  <span class="topics-label">Telusuri:</span>
  {build_topic_buttons(tags)}
</div>''')

    # 3. Articles grid
    start = html.find('<div class="articles-grid">')
    end = html.find('</div>', start) + len('</div>')
    old = html[start:end]
    html = html.replace(old, f'''<div class="articles-grid">
{build_articles_grid(articles)}
</div>''')

    with open(SITE_DIR / "index.html", "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Generated index.html — {len(articles)} articles")

if __name__ == "__main__":
    articles = load_articles()
    generate_index(articles)