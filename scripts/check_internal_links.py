"""Report broken internal links in the built Zensical site.

Audit actual HTML <a href> destinations, not merely Markdown references.
External hosts are outside scope; same-domain and relative links are checked.
Fragments are validated for the stable year-record anchors owned by this site.
"""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlsplit, unquote
import posixpath

SITE=Path("site")
HOST="senju-archive.github.io"

class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.hrefs=[]
        self.ids=set()
    def handle_starttag(self, tag, attrs):
        values=dict(attrs)
        if tag=="a" and values.get("href") is not None:
            self.hrefs.append(values["href"])
        if values.get("id"):
            self.ids.add(values["id"])
        if tag=="a" and values.get("name"):
            self.ids.add(values["name"])

def target_file(path):
    rel=unquote(path).lstrip("/")
    normalized=posixpath.normpath(rel or ".")
    if normalized==".." or normalized.startswith("../"):
        return None
    candidates=[]
    p=SITE/normalized
    if rel.endswith("/") or normalized==".":
        candidates=[p/"index.html"]
    else:
        candidates=[p,p/"index.html"]
    for candidate in candidates:
        if candidate.is_file():
            return candidate
    return None

pages=list(SITE.rglob("*.html"))
documents={}
for page in pages:
    doc=Links()
    doc.feed(page.read_text(encoding="utf-8"))
    documents[page]=doc

failures=[]
checked=0
for page,doc in documents.items():
    current="/"+str(page.relative_to(SITE).parent).replace("\\","/")
    if current=="/.":
        current="/"
    elif not current.endswith("/"):
        current+="/"
    base=f"https://{HOST}{current}"
    for href in doc.hrefs:
        if not href.strip():
            continue
        target=urlsplit(urljoin(base,href))
        if target.scheme not in ("http","https") or target.netloc.lower()!=HOST:
            continue
        checked+=1
        dest=target_file(target.path)
        if dest is None:
            failures.append(f"{page}: missing link: {href}")
        elif target.fragment.startswith("record-"):
            parsed=documents.get(dest)
            if parsed is None or unquote(target.fragment) not in parsed.ids:
                failures.append(f"{page}: missing year-record anchor: {href}")
if failures:
    print("\n".join(failures[:75]))
    raise SystemExit(f"Internal link check failed: {len(failures)} of {checked} links")
print(f"Internal navigation check passed: {checked} local links across {len(pages)} pages.")
