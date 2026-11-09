#!/usr/bin/env python3
"""Build DumpCheck into docs/ for GitHub Pages.

Layout:
  config.json                 site settings
  data/stations.json          every station, each checked against an official source
  content/guides/*.md         guides (front matter + Markdown)
  content/*.md                site pages (about, disclosures, suggest)

Front matter keys: title, description, path, kind (guide|page), eyebrow, lede,
updated, order, summary.
Jinja helpers inside Markdown: url(path), station(id) -> card,
stations(*ids) -> grid of cards, amazon(query, label) -> link, count(status).
"""
import argparse
import datetime as dt
import hashlib
import json
import os
import shutil
from pathlib import Path
from urllib.parse import quote_plus

import markdown
from jinja2 import Environment, FileSystemLoader, select_autoescape
from markupsafe import Markup, escape

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "docs"

REGIONS = [("east", "East Tennessee"), ("middle", "Middle Tennessee"), ("west", "West Tennessee")]
STATUS = {
    "open": ("Open", "The official source shows it operating now."),
    "check": ("Call first", "An official source confirms the station, but not this season's dates or hours."),
    "seasonal-closed": ("Closed for the season", "Seasonal station that is past its posted season."),
    "closed": ("Closed", "An official source says it's closed or gone."),
}


def human_date(value):
    if not value:
        return ""
    if isinstance(value, str):
        value = dt.date.fromisoformat(value[:10])
    return value.strftime("%b %-d, %Y")


def parse_front_matter(text):
    if not text.startswith("---"):
        return {}, text
    _, fm, body = text.split("---", 2)
    meta = {}
    for line in fm.strip().splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip()
    return meta, body.lstrip("\n")


def maps_link(s):
    q = s.get("address") or f"{s['name']}, {s['where']}, Tennessee"
    return "https://www.google.com/maps/search/?api=1&query=" + quote_plus(q)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base-path", default=None)
    ap.add_argument("--site-url", default=None)
    ap.add_argument("--relative", action="store_true")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    global OUT
    if args.out:
        OUT = Path(args.out).resolve()

    site = json.loads((ROOT / "config.json").read_text())
    if args.base_path is not None:
        site["base_path"] = args.base_path
    if args.site_url is not None:
        site["site_url"] = args.site_url
    base = site.get("base_path", "").rstrip("/")

    stations = json.loads((ROOT / "data" / "stations.json").read_text())
    by_id = {s["id"]: s for s in stations}
    for s in stations:
        s["maps"] = maps_link(s)
        s["status_label"] = STATUS[s["status"]][0]

    current = {"page": "/"}

    def url(path):
        if not args.relative:
            return f"{base}{path}"
        target, _, frag = path.partition("#")
        if target.endswith("/"):
            target += "index.html"
        page_dir = current["page"] if current["page"].endswith("/") else str(Path(current["page"]).parent) + "/"
        rel = os.path.relpath(target, page_dir)
        return rel + (("#" + frag) if frag else "")

    def canonical(path):
        return f"{site['site_url'].rstrip('/')}{base}{path}"

    env = Environment(loader=FileSystemLoader(ROOT / "templates"), autoescape=select_autoescape(["html"]))
    env.filters["human_date"] = human_date
    build_id = hashlib.sha1(dt.datetime.now().isoformat().encode()).hexdigest()[:8]
    card = env.get_template("_card.html")

    # ---------- Markdown helpers ----------
    def station(sid):
        # One line of HTML so Markdown passes it through as a raw block.
        html = card.render(s=by_id[sid], url=url, compact=True)
        return Markup(" ".join(html.split()))

    def stations_grid(*ids):
        cards = " ".join(" ".join(card.render(s=by_id[i], url=url, compact=True).split()) for i in ids)
        return Markup(f'<div class="cards">{cards}</div>')

    def amazon(query, label=None):
        tag = site.get("amazon_tag", "").strip()
        href = f"https://www.amazon.com/s?k={quote_plus(query)}" + (f"&tag={tag}" if tag else "")
        rel = "sponsored nofollow noopener" if tag else "nofollow noopener"
        return Markup(f'<a href="{href}" rel="{rel}">{label or query}</a>')

    def rv_programs():
        # Only approved affiliate programs show; nothing renders until Micaiah pastes a link in chat.
        progs = [p for p in site.get("rv_programs", []) if p.get("affiliate")]
        if not progs:
            return Markup("")
        slug = current.get("page", "/").strip("/").replace("/", "-") or "home"
        items = "".join(f'<li><a href="{escape(p["url"].replace("{page}", slug))}" rel="sponsored nofollow noopener"><strong>{escape(p["name"])}</strong></a> — {escape(p["blurb"])}</li>' for p in progs)
        return Markup('<aside class="haul"><h3>Planning more nights on the road?</h3>'
                      f'<ul>{items}</ul><p class="affiliate-note">These are affiliate links: if you join through one, DumpCheck may earn a commission '
                      f'at no extra cost to you. They never affect which stations we list. <a href="{url("/disclosures/")}">Disclosures</a>.</p></aside>')

    def count(status):
        return sum(1 for s in stations if s["status"] == status)

    md_globals = dict(site=site, url=url, station=station, stations=stations_grid, amazon=amazon, count=count, rv_programs=rv_programs)

    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)
    shutil.copytree(ROOT / "static", OUT / "static")
    (OUT / ".nojekyll").write_text("")
    sitemap = []

    def write(path, html):
        target = OUT / path.lstrip("/") / "index.html" if path.endswith("/") else OUT / path.lstrip("/")
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(html)

    md = markdown.Markdown(extensions=["extra", "sane_lists", "smarty"])

    guides, pages = [], []
    for f in sorted((ROOT / "content").rglob("*.md")):
        meta, body = parse_front_matter(f.read_text())
        meta["_body"] = body
        (guides if meta.get("kind") == "guide" else pages).append(meta)
    guides.sort(key=lambda m: int(m.get("order", 99)))

    updated_all = max([s["last_checked"] for s in stations] + [m.get("updated", "2000-01-01") for m in guides])
    common = dict(site=site, url=url, canonical=canonical, build_id=build_id, guides=guides,
                  updated_human=human_date(updated_all), status_info=STATUS)

    # ---------- guides + pages ----------
    for meta in guides + pages:
        current["page"] = meta["path"]
        html_body = md.reset().convert(env.from_string(meta["_body"]).render(**md_globals))
        jsonld = ""
        if meta.get("kind") == "guide":
            jsonld = json.dumps({"@context": "https://schema.org", "@type": "Article", "headline": meta["title"],
                                 "description": meta.get("description", ""), "dateModified": meta.get("updated", updated_all)})
        write(meta["path"], env.get_template("page.html").render(page=meta, body=html_body, jsonld=jsonld, **common))
        sitemap.append((meta["path"], meta.get("updated", updated_all)))

    # ---------- statewide directory ----------
    current["page"] = "/tennessee/"
    page = dict(path="/tennessee/", title=f"RV dump stations in {site['state']}, checked and dated",
                description=f"Every {site['state']} RV dump station we've checked against an official source: status, season, fee, water, phone and the date we checked.")
    groups = [(label, [s for s in stations if s["region"] == key]) for key, label in REGIONS]
    groups = [(label, items) for label, items in groups if items]
    order = {"open": 0, "check": 1, "seasonal-closed": 2, "closed": 3}
    for _, items in groups:
        items.sort(key=lambda s: (order[s["status"]], s["area"], s["name"]))
    item_list = {"@context": "https://schema.org", "@type": "ItemList", "name": page["title"],
                 "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": s["name"]} for i, s in enumerate(stations)]}
    write(page["path"], env.get_template("directory.html").render(page=page, groups=groups, stations=stations,
                                                                  jsonld=json.dumps(item_list), **common))
    sitemap.append((page["path"], updated_all))

    # ---------- home + 404 ----------
    current["page"] = "/"
    page = dict(path="/", title=site["site_name"], description=site["description"])
    open_now = [s for s in stations if s["status"] == "open"]
    write("/", env.get_template("home.html").render(page=page, stations=stations, open_now=open_now,
                                                     counts={k: count(k) for k in STATUS}, **common))
    sitemap.insert(0, ("/", updated_all))
    page = dict(path="/404.html", title="Page not found", description="This page could not be found.")
    (OUT / "404.html").write_text(env.get_template("404.html").render(page=page, **common))

    urls = "".join(f"<url><loc>{canonical(p)}</loc><lastmod>{d}</lastmod></url>" for p, d in sitemap)
    (OUT / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>')
    if site.get("adsense_client"):
        pub = site["adsense_client"].replace("ca-", "")
        (OUT / "ads.txt").write_text(f"google.com, {pub}, DIRECT, f08c47fec0942fa0\n")
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {canonical('/sitemap.xml')}\n")
    print(f"Built {len(sitemap)} pages, {len(stations)} stations -> {OUT}")


if __name__ == "__main__":
    main()
