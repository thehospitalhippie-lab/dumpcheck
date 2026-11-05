#!/usr/bin/env python3
"""Quality gate for DumpCheck. Run after build.py; exits non-zero on problems.

Checks:
- every station has the required fields, a valid region and status, a unique id,
  at least one https source, and a valid last_checked date that isn't in the future
- phones look like 615-555-0123, so tel: links work
- every guide has a Sources section, and no source URL hides an "@" in its host
- every built HTML page has a <title>, a meta description and exactly one <h1>
- every internal link resolves to a built file
"""
import datetime as dt
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs"
REGIONS = {"east", "middle", "west"}
STATUSES = {"open", "check", "seasonal-closed", "closed"}
REQUIRED = ["id", "name", "region", "area", "operator", "kind", "where", "status", "status_note",
            "season", "access", "fee", "water", "sources", "last_checked"]

problems = []


def check_stations():
    stations = json.loads((ROOT / "data" / "stations.json").read_text())
    today = dt.date.today()
    seen = set()
    for s in stations:
        sid = s.get("id", "?")
        for k in REQUIRED:
            if not s.get(k):
                problems.append(f"{sid}: missing {k}")
        if sid in seen:
            problems.append(f"{sid}: duplicate id")
        seen.add(sid)
        if s.get("region") not in REGIONS:
            problems.append(f"{sid}: bad region {s.get('region')}")
        if s.get("status") not in STATUSES:
            problems.append(f"{sid}: bad status {s.get('status')}")
        for src in s.get("sources", []):
            u = str(src.get("url", ""))
            if not u.startswith("https://") or not src.get("title"):
                problems.append(f"{sid}: every source needs a title and an https url")
            elif "@" in u.split("/")[2]:
                problems.append(f"{sid}: suspicious source URL {u}")
        if s.get("phone") and not re.fullmatch(r"\d{3}-\d{3}-\d{4}", s["phone"]):
            problems.append(f"{sid}: phone must look like 615-555-0123")
        try:
            if dt.date.fromisoformat(s.get("last_checked", "")) > today:
                problems.append(f"{sid}: last_checked is in the future")
        except ValueError:
            problems.append(f"{sid}: last_checked must be YYYY-MM-DD")
    for f in sorted((ROOT / "content").rglob("*.md")):
        text = f.read_text()
        if "kind: guide" in text.split("---")[1] and "## Sources" not in text:
            problems.append(f"{f.relative_to(ROOT)}: guide has no Sources section")
        for url in re.findall(r"<(https?://[^>]+)>", text):
            if "@" in url.split("/")[2]:
                problems.append(f"{f.relative_to(ROOT)}: suspicious source URL {url}")
        for sid in re.findall(r"station[s]?\(([^)]*)\)", text):
            for one in re.findall(r"'([^']+)'", sid):
                if one not in seen:
                    problems.append(f"{f.relative_to(ROOT)}: unknown station id {one}")
    return stations


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links, self.has_title, self.has_desc, self.h1 = [], False, False, 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "a" and a.get("href"):
            self.links.append(a["href"])
        if tag == "link" and a.get("rel") == "stylesheet":
            self.links.append(a.get("href", ""))
        if tag == "script" and a.get("src"):
            self.links.append(a["src"])
        if tag == "title":
            self.has_title = True
        if tag == "meta" and a.get("name") == "description" and a.get("content"):
            self.has_desc = True
        if tag == "h1":
            self.h1 += 1


def check_site():
    if not OUT.exists():
        problems.append("docs/ not built — run python3 build.py first")
        return
    base = json.loads((ROOT / "config.json").read_text()).get("base_path", "").rstrip("/")
    # The build may have been run with --base-path; detect it from the home page stylesheet link.
    home = (OUT / "index.html").read_text()
    m = re.search(r'href="([^"]*)/static/style\.css', home)
    if m:
        base = m.group(1)
    for page in OUT.rglob("*.html"):
        p = PageParser()
        p.feed(page.read_text())
        rel = page.relative_to(OUT)
        if not p.has_title:
            problems.append(f"{rel}: missing <title>")
        if not p.has_desc:
            problems.append(f"{rel}: missing meta description")
        if p.h1 != 1:
            problems.append(f"{rel}: expected exactly one <h1>, found {p.h1}")
        for href in p.links:
            if href.startswith(("http", "mailto:", "tel:", "#")):
                continue
            path = href.split("#")[0].split("?")[0]
            if base and path.startswith(base):
                path = path[len(base):]
            if not path.startswith("/"):
                problems.append(f"{rel}: relative link {href} (use url())")
                continue
            target = OUT / path.lstrip("/")
            if path.endswith("/"):
                target = target / "index.html"
            if not target.exists():
                problems.append(f"{rel}: broken internal link {href}")


if __name__ == "__main__":
    stations = check_stations()
    check_site()
    if problems:
        print("CHECK FAILED:")
        for x in problems:
            print(" -", x)
        sys.exit(1)
    print(f"CHECK OK: {len(stations)} stations, site links and pages look good.")
