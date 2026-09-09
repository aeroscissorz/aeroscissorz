from pathlib import Path
from html import escape
from datetime import datetime
import shutil
import markdown

ROOT = Path(__file__).parent
OUT = ROOT / "_site"
POSTS = ROOT / "posts"

def read_post(path):
    raw = path.read_text(encoding="utf-8")
    meta, body = {}, raw
    if raw.startswith("---"):
        _, front, body = raw.split("---", 2)
        for line in front.strip().splitlines():
            if ":" in line:
                key, value = line.split(":", 1)
                meta[key.strip()] = value.strip().strip("\"'")
    meta.setdefault("title", path.stem.replace("-", " ").title())
    meta.setdefault("date", datetime.now().strftime("%b %-d, %Y").lower())
    meta.setdefault("status", "public")
    return meta, body.strip()

def document(content, title, post=False):
    prefix = "../../" if post else ""
    nav = '<a class="back" href="../../index.html">← home</a>' if post else '<nav class="nav"><a href="#writing">writing</a><a href="#about">about</a></nav>'
    main_class = 'section post-section' if post else ''
    return f'''<!doctype html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"><meta name="description" content="{escape(title)}"><title>{escape(title)} — Shubham Sharma</title><link rel="stylesheet" href="{prefix}site.css"></head><body><div class="site-shell"><header><a class="wordmark" href="{prefix}index.html">shubham sharma</a>{nav}</header><main class="{main_class}">{content}</main><footer><span>© <span data-year></span> shubham sharma</span><span class="status">available for good work</span></footer></div><script src="{prefix}site.js"></script></body></html>'''

def build():
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    shutil.copy(ROOT / "site.css", OUT / "site.css")
    shutil.copy(ROOT / "site.js", OUT / "site.js")
    entries = []
    for source in sorted(POSTS.glob("*.md"), reverse=True):
        meta, body = read_post(source)
        if meta.get("status", "public").lower() != "public":
            continue
        post_slug = source.stem.lower()
        rendered = markdown.markdown(body, extensions=["fenced_code", "tables"])
        content = f'<div class="section-label"><span>{escape(meta["date"])} · {escape(meta.get("words", ""))} words</span><span>{escape(meta["status"])}</span></div><article class="post"><h1>{escape(meta["title"])}</h1>{rendered}</article>'
        target = OUT / "posts" / post_slug
        target.mkdir(parents=True, exist_ok=True)
        (target / "index.html").write_text(document(content, meta["title"], post=True), encoding="utf-8")
        entries.append((meta, post_slug))
    rows = "".join(f'<a class="writing-row" href="posts/{slug}/"><span class="writing-number">{i:02d}</span><span class="writing-title">{escape(meta["title"])}</span><span class="writing-date">{escape(meta["date"])}</span></a>' for i, (meta, slug) in enumerate(entries, 1))
    content = f'''<section class="hero"><p class="eyebrow">a small internet home / 2026</p><h1>I build systems,<br><em>then write about them.</em></h1><div class="hero-bottom"><p class="hero-note">GenAI engineer building production LLM systems, agentic workflows, and useful software.</p><span class="scroll-cue">↓ scroll slowly</span></div></section><section class="section" id="writing"><div class="section-label"><span>Selected writing</span><span>{len(entries):02d}</span></div><div class="writing-list">{rows}</div></section><section class="section about" id="about"><div class="about-copy">I build the systems that help <span>intelligence</span> become useful.</div><div class="about-details"><p>I’m Shubham Sharma, a Software Engineer (GenAI) at Cognizant. I work with LangChain, LangGraph, RAG, Python, and production LLM applications.</p><p>Currently building real-time voice agents, retrieval systems, and multi-agent workflows.</p><p><a class="contact-link" href="mailto:shubhamsharma10112003@gmail.com">email me ↗</a></p><p><a class="contact-link" href="https://github.com/aeroscissorz">GitHub ↗</a> <a class="contact-link" href="https://www.linkedin.com/in/shubham-sharma-89bb56211/">LinkedIn ↗</a></p></div></section>'''
    (OUT / "index.html").write_text(document(content, "Shubham Sharma"), encoding="utf-8")

if __name__ == "__main__":
    build()
