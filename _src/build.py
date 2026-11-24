#!/usr/bin/env python3
"""Static build for smartvisionai.agency (EN, ES, RU).

Sources live in _src/ (Jekyll on GitHub Pages ignores folders that start
with "_", so they are not published). The build writes finished pages into
the repository root, which GitHub Pages serves as is.

    python3 _src/build.py              # production: clean URLs (/es/services/)
    python3 _src/build.py --preview D  # preview copy in folder D with
                                       # explicit index.html links, for
                                       # viewing without a web server

Languages: English pages live at /, Spanish at /es/, Russian at /ru/.
Page templates: templates/pages/ (EN), templates/es/pages/, templates/ru/pages/.
Shared layouts take interface text from i18n.STRINGS; page titles and
descriptions for ES/RU come from i18n.TR.

Requires Jinja2 (pip install jinja2).
"""
import argparse
import copy
import datetime as dt
import json
import os
import shutil
import sys

sys.dont_write_bytecode = True
from jinja2 import Environment, FileSystemLoader, StrictUndefined  # noqa: E402

SRC = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(SRC)
sys.path.insert(0, SRC)
from site_data import SITE, PAGES  # noqa: E402
from i18n import LANGS, LANG_NAMES, LOCALES, STRINGS, TR  # noqa: E402


def prefix_of(lang):
    return "" if lang == "en" else "/" + lang


def localize(lang):
    """Registry for one language: URLs prefixed, metadata translated."""
    out = []
    for p in PAGES:
        q = copy.deepcopy(p)
        q["en_url"] = p["url"]
        q["url"] = prefix_of(lang) + p["url"]
        q.update(TR.get(lang, {}).get(p["url"], {}))
        if lang != "en":
            q["template"] = lang + "/" + p["template"]
        out.append(q)
    return out


def out_path(url):
    """'/' -> index.html, '/es/services/' -> es/services/index.html."""
    rel = url.strip("/")
    return os.path.join(rel, "index.html") if rel else "index.html"


def make_env(preview, page_url, lang, pages):
    depth = len([p for p in page_url.strip("/").split("/") if p])
    rel_prefix = "../" * depth if preview else "/"
    pre = prefix_of(lang)

    def to_target(url):
        path, _, anchor = url.partition("#")
        anchor = "#" + anchor if anchor else ""
        if not preview:
            return path + anchor
        rel = path.strip("/")
        target = (rel + "/index.html") if rel and "." not in rel.split("/")[-1] else (rel or "index.html")
        return rel_prefix + target + anchor

    def link(url):
        """Link to a page of the current language, given its English URL."""
        if url.startswith(("http://", "https://", "mailto:", "#")):
            return url
        return to_target(pre + url if url.startswith("/") else url)

    def link_lang(en_url, other):
        """Same page in another language."""
        return to_target(prefix_of(other) + en_url)

    def asset(path):
        return (rel_prefix + path.lstrip("/")) if preview else path

    def t(key):
        return STRINGS[lang].get(key, STRINGS["en"][key])

    env = Environment(
        loader=FileSystemLoader(os.path.join(SRC, "templates")),
        undefined=StrictUndefined,
        autoescape=False,
        trim_blocks=True,
        lstrip_blocks=True,
    )
    by_en = {p["en_url"]: p for p in pages}
    env.globals.update(
        link=link, link_lang=link_lang, asset=asset, t=t, site=SITE, lang=lang,
        langs=LANGS, lang_names=LANG_NAMES, locale=LOCALES[lang],
        pages=pages, page_by_url=by_en,
        services=[p for p in pages if p.get("kind") == "service"],
        cases=[p for p in pages if p.get("kind") == "case"],
        posts=[p for p in pages if p.get("kind") == "post"],
        tojson=lambda o: json.dumps(o, ensure_ascii=False),
    )
    return env


def breadcrumbs(page, pages, lang):
    by_en = {p["en_url"]: p for p in pages}
    parts = [p for p in page["en_url"].strip("/").split("/") if p]
    crumbs = []
    for i in range(len(parts) - 1):
        url = "/" + "/".join(parts[: i + 1]) + "/"
        if url in by_en:
            crumbs.append({"url": url, "abs": by_en[url]["url"], "name": by_en[url]["nav"]})
    home = {"url": "/", "abs": prefix_of(lang) + "/", "name": STRINGS[lang]["home"]}
    return [home] + crumbs if parts else []


def write(dest, rel, html):
    target = os.path.join(dest, rel)
    os.makedirs(os.path.dirname(target) or dest, exist_ok=True)
    with open(target, "w", encoding="utf-8") as f:
        f.write(html)


def build(dest, preview):
    all_pages = {}
    for lang in LANGS:
        pages = localize(lang)
        all_pages[lang] = pages
        for page in pages:
            env = make_env(preview, page["url"], lang, pages)
            html = env.get_template(page["template"]).render(
                page=page, crumbs=breadcrumbs(page, pages, lang))
            write(dest, out_path(page["url"]), html)

    # 404 page (GitHub Pages serves /404.html for any missing path) — EN
    pages = all_pages["en"]
    env = make_env(preview, "/", "en", pages)
    nf = {"url": "/404.html", "en_url": "/404.html", "title": "Page not found · Smart Vision AI",
          "description": "Page not found.", "noindex": True, "nav": "404", "kind": "404"}
    write(dest, "404.html", env.get_template("404.html").render(page=nf, crumbs=[]))

    # static assets
    assets_dst = os.path.join(dest, "assets")
    if os.path.isdir(assets_dst):
        shutil.rmtree(assets_dst)
    shutil.copytree(os.path.join(SRC, "assets"), assets_dst)

    if preview:
        return

    today = dt.date.today().isoformat()
    base = SITE["url"].rstrip("/")
    rows = []
    for lang in LANGS:
        for p in all_pages[lang]:
            if p.get("noindex"):
                continue
            alts = "".join(
                '\n    <xhtml:link rel="alternate" hreflang="{}" href="{}{}"/>'.format(
                    l, base, prefix_of(l) + p["en_url"]) for l in LANGS)
            alts += '\n    <xhtml:link rel="alternate" hreflang="x-default" href="{}{}"/>'.format(base, p["en_url"])
            rows.append("  <url><loc>{}{}</loc><lastmod>{}</lastmod>{}\n  </url>".format(
                base, p["url"], p.get("updated", today), alts))
    write(dest, "sitemap.xml",
          '<?xml version="1.0" encoding="UTF-8"?>\n'
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
          'xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
          + "\n".join(rows) + "\n</urlset>\n")

    env = make_env(False, "/", "en", all_pages["en"])
    write(dest, "llms.txt", env.get_template("llms.txt").render())


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
