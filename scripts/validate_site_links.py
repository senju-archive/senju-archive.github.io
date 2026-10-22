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
homepage=html("index.html")
assert "archive-home-masthead" in homepage
assert 'id="archive-home-title"' in homepage
assert "SENJU HISTORICAL ARCHIVE" in homepage
assert "archive-hero-mark" in homepage
assert '<span class="archive-lede-line">史料からたどる、</span>' in homepage
assert '<span class="archive-lede-line">千手氏の歴史。</span>' in homepage
assert "senju_archive_logo_master_v1.png" in homepage
assert "千手氏の平家出自" in html("about/index.html")
assert (site/"assets/images/senju_archive_logo_master_v1.png").is_file()
assert "senju_archive_logo_master_v1.png" in homepage
# Mobile design safety checks: labels stay accessible without visible English,
# header text remains legible, and narrow screens retain reading gutters.
header=html("index.html")
style=html("assets/css/extra.css") if (site/"assets/css/extra.css").is_file() else (site/"assets/css/extra.css").read_text("utf-8")
for label in ("メニューを開く","検索を開く"):
    assert label in header, label
# Header: first action is the navigation drawer; logo is not duplicated
# here, while the site-name home link and the homepage emblem remain intact.
header_nav=header.split('data-md-component="header">', 1)[1].split('</header>', 1)[0]
assert 'class="md-header__button md-logo"' not in header_nav
assert header_nav.find('for="__drawer"') < header_nav.find('data-md-component="header-title"')
assert "千手氏歴史アーカイブのホームへ戻る" in header_nav
assert "archive-hero-mark" in homepage
assert "md-header__topic.archive-header-home" in style
# Responsive article hero preserves the original transparent logo and removes
# the former red band / white tile; primary drawer heading uses a serif font.
assert "md-nav--primary > .md-nav__title" in style
assert "md-typeset .archive-hero-mark img" in style
assert "background: transparent;" in style
assert "border-right: 1px solid #e2d6be;" in style
assert "color: #fff9ed" in style
assert "padding-left: clamp(16px, 4.5vw, 20px)" in style
assert "padding-right: clamp(16px, 4.5vw, 20px)" in style
assert "<strong>千手氏（せんじゅし）</strong>" in html("senju/index.html")
print("Validated navigation, logo, mobile readability styles and content indexes.")
