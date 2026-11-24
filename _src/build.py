#!/usr/bin/env python3
"""Static build for smartvisionai.agency.

Sources live in _src/ (Jekyll on GitHub Pages ignores folders that start
with "_", so they are not published). The build writes finished pages into
the repository root, which GitHub Pages serves as is.

    python3 _src/build.py              # production: clean URLs (/services/)
    python3 _src/build.py --preview D  # preview copy in folder D with
                                       # explicit index.html links, for
                                       # viewing without a web server

Requires Jinja2 (pip install jinja2).
"""
import argparse
import datetime as dt
import json
import os
import shutil
import sys

from jinja2 import Environment, FileSystemLoader, StrictUndefined

SRC = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(SRC)
sys.path.insert(0, SRC)
from site_data import SITE, PAGES, SERVICES, CASES, POSTS  # noqa: E402


def out_path(url):
    """'/' -> index.html, '/services/' -> services/index.html."""
    rel = url.strip("/")
    return os.path.join(rel, "index.html") if rel else "index.html"


def make_env(preview, page_url):
    depth = len([p for p in page_url.strip("/").split("/") if p])
    prefix = "../" * depth if preview else "/"

    def link(url):
        """Internal link. Production: absolute clean URL. Preview: relative
        path to index.html so the copy works from any folder."""
        if url.startswith(("http://", "https://", "mailto:", "#")):
            return url
        path, _, anchor = url.partition("#")
        anchor = "#" + anchor if anchor else ""
        if not preview:
            return path + anchor
        rel = path.strip("/")
        target = (rel + "/index.html") if rel and "." not in rel.split("/")[-1] else (rel or "index.html")
        return prefix + target + anchor

    def asset(path):
        return (prefix + path.lstrip("/")) if preview else path

    env = Environment(
        loader=FileSystemLoader(os.path.join(SRC, "templates")),
        undefined=StrictUndefined,
        autoescape=False,
        trim_blocks=True,
        lstrip_blocks=True,
    )
    env.globals.update(link=link, asset=asset, site=SITE, pages=PAGES,
                       services=SERVICES, cases=CASES, posts=POSTS,
                       page_by_url={p["url"]: p for p in PAGES},
                       tojson=lambda o: json.dumps(o, ensure_ascii=False))
    return env


def breadcrumbs(page):
    by_url = {p["url"]: p for p in PAGES}
    crumbs, parts = [], [p for p in page["url"].strip("/").split("/") if p]
    for i in range(len(parts) - 1):
        url = "/" + "/".join(parts[: i + 1]) + "/"
        if url in by_url:
            crumbs.append({"url": url, "name": by_url[url]["nav"]})
    return [{"url": "/", "name": "Home"}] + crumbs if parts else []


def build(dest, preview):
    for page in PAGES:
        env = make_env(preview, page["url"])
        tpl = env.get_template(page["template"])
        html = tpl.render(page=page, crumbs=breadcrumbs(page))
        target = os.path.join(dest, out_path(page["url"]))
        os.makedirs(os.path.dirname(target) or dest, exist_ok=True)
        with open(target, "w", encoding="utf-8") as f:
            f.write(html)

    # 404 page (GitHub Pages serves /404.html for any missing path)
    env = make_env(False if not preview else True, "/")
    html = env.get_template("404.html").render(
        page={"url": "/404.html", "title": "Page not found · Smart Vision AI",
              "description": "Page not found.", "noindex": True, "nav": "404", "kind": "404"},
        crumbs=[])
    with open(os.path.join(dest, "404.html"), "w", encoding="utf-8") as f:
        f.write(html)

    # static assets
    assets_src = os.path.join(SRC, "assets")
    assets_dst = os.path.join(dest, "assets")
    if os.path.isdir(assets_dst):
        shutil.rmtree(assets_dst)
    shutil.copytree(assets_src, assets_dst)

    if preview:
        return

    today = dt.date.today().isoformat()
    # sitemap.xml
    rows = []
    for p in PAGES:
        if p.get("noindex"):
            continue
        rows.append(
            "  <url><loc>{}{}</loc><lastmod>{}</lastmod></url>".format(
                SITE["url"].rstrip("/"), p["url"], p.get("updated", today)))
    with open(os.path.join(dest, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n'
                '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                + "\n".join(rows) + "\n</urlset>\n")

    # llms.txt — plain map of the site for AI assistants
    env = make_env(False, "/")
    txt = env.get_template("llms.txt").render()
    with open(os.path.join(dest, "llms.txt"), "w", encoding="utf-8") as f:
        f.write(txt)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--preview", metavar="DIR")
    a = ap.parse_args()
    if a.preview:
        os.makedirs(a.preview, exist_ok=True)
        for name in ("petr-belyaev-4x5-v2.jpg", "petr-belyaev-4x5-v2-660.jpg",
                     "favicon.svg", "og-v2.jpg"):
            shutil.copy(os.path.join(ROOT, name), os.path.join(a.preview, name))
        build(a.preview, True)
        print("preview built in", a.preview)
    else:
        build(ROOT, False)
        print("site built in", ROOT)


if __name__ == "__main__":
    main()
