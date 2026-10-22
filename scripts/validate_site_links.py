"""Check the rendered theme/era navigation and chronological indexes."""
from pathlib import Path
import re
site=Path("site")
def html(path):
    file=site/path
    assert file.is_file(), f"Missing {file}"
    return file.read_text("utf-8")

tags=html("tags/index.html")
for term in ("原田氏","秋月氏","城郭攻防","移封","鍋島氏"):
    assert term in tags, f"Missing related tag {term}"
assert "lineages/chikuzen/" in tags and "lineages/takanabe/" in tags
overview=html("senju/index.html")
for slug in ("chikuzen","buzen","takanabe","ogi"):
    assert f"lineages/{slug}/" in overview, slug
lineages=html("lineages/index.html")
for name in ("福岡県","宮崎県","佐賀県"):
    assert name in lineages, name
index=html("periods/index.html")
for slug in ("ancient","heian","kamakura","nanbokucho","muromachi","sengoku","azuchi-momoyama","edo","meiji"):
    assert f'{slug}/' in index, slug
    h=html(f"periods/{slug}/index.html")
    years=[int(y) for y in re.findall(r'data-year="([0-9]{3,4})"',h)]
    assert years==sorted(years), (slug,years)
    assert "lineages/" in h or "senju/" in h, slug
assert "periods/" in html("index.html")
assert "encyclopedia/" in html("index.html")
en=html("encyclopedia/index.html")
for label in ("地域・地名","城郭・史跡","関連氏族","制度・用語","存寄","嘉麻市"):
    assert label in en, f"Encyclopedia category missing: {label}"
assert "../sites/" in en, "Encyclopedia lacks the historic sites index"
assert "encyclopedia/" in html("sites/index.html")
assert "関連事典" in html("previews/encyclopedia/index.html")
assert "関連タグ" in html("tags/index.html")
# Context and anchored record links
for lineage,years in {
    "chikuzen": [1185,1323,1337,1354],
    "buzen": [1394,1399],
    "takanabe": [1587,1621,1777],
    "ogi": [1617],
}.items():
    entry=html(f"lineages/{lineage}/index.html")
    assert "article-context" in entry and "article-shortcuts" in entry, lineage
    for year in years:
        assert f"#record-{year}" in entry, (lineage,year)
        assert any(f'id="record-{year}"' in html(str(p.relative_to(site)))
                   for p in (site/"periods").glob("*/index.html")), (lineage,year)
for preview in ("person","event","doc","senju","encyclopedia"):
    assert 'article-context' in html(f"previews/{preview}/index.html")
assert "person-view-lineage" in html("persons/index.html")
assert "person-view-kana" in html("persons/index.html")
assert "person-accordion" in html("persons/index.html")
assert "千手氏の人物" in html("persons/index.html")
assert "読み未確定" in html("persons/index.html")
for slug in ("chikuzen","buzen","takanabe","ogi"):
    assert f"persons/{slug}/" in html(f"lineages/{slug}/index.html")
    assert "人物一覧" in html(f"persons/{slug}/index.html")
    assert f'{slug}/' in html("persons/index.html")
assert "関連人物" in html("persons/index.html")
print("Validated period/lineage context, record anchors, article layouts and related tags.")
