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
print("Validated period navigation, sorted chronology, prefectures and related tags.")
