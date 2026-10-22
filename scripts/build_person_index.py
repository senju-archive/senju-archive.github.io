"""Generate person index and four lineage subindexes from a single catalogue.

Only verified, already published URLs are made clickable.
Run before building the Zensical site.
"""
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
DATA = json.loads((ROOT / "data/person-index.json").read_text("utf-8"))
GROUPS = DATA["groups"]
PEOPLE = DATA["persons"]
KANA = {
 "あ":"あいうえお", "か":"かきくけこ", "さ":"さしすせそ",
 "た":"たちつてと", "な":"なにぬねの", "は":"はひふへほ",
 "ま":"まみむめも", "や":"やゆよ", "ら":"らりるれろ", "わ":"わをん"
}
E = lambda s: html.escape(str(s), quote=True)
assert len({p[0] for p in PEOPLE}) == len(PEOPLE), "Duplicate name; add stable person IDs before names collide"
assert all(p[1] in {g[0] for g in GROUPS}|{"related","unknown"} for p in PEOPLE)

def ordered(rows):
 return sorted(rows, key=lambda p: (p[2] is None, p[2] or 0, p[0]))

def line(p):
 name, group, year, kana, note = p
 return ('<li class="person-item"><strong>'+E(name)+'</strong>'
         '<span>'+E(note)+'</span><small>個別記事準備中</small></li>')

def listing(rows):
 if not rows:
  return '<p class="person-no-items">現在は登録候補がありません。</p>'
 return '<ul class="person-items">'+''.join(line(p) for p in ordered(rows))+'</ul>'

def accordion(title, rows, more=""):
 return ('<details class="person-accordion"><summary><strong>'+E(title)+
         '</strong><span>'+str(len(rows))+'名</span></summary>'
         '<div class="person-accordion-body">'+listing(rows)+more+'</div></details>')

def row_of(p):
 reading=p[3]
 if not reading:
  return "読み未確定"
 for group, letters in KANA.items():
  if reading[0] in letters:
   return group+"行"
 raise ValueError("Invalid reading for "+p[0])

def build_index():
 s=[
 "# 人物から探す","",
 '<div class="archive-status">系統別・五十音順 ／ 個別人物記事は整備中</div>',"",
 "千手氏の人物を、**系統別**または**名前・通称の読みの五十音順**で探せます。"
 "五十音順では名字「千手」を除きます。人名の読みが未確認なら勝手に決めず、末尾に分けます。","",
 "掲載人名は既存概説から抽出した**調査候補**であり、史料・年代・同定が確認済みという意味ではありません。"
 "個別人物記事が公開された人名からクリック可能にします。","",
 '<div class="person-index">',
 '<input class="person-view-radio" id="person-view-lineage" type="radio" name="person-view" checked>',
 '<input class="person-view-radio" id="person-view-kana" type="radio" name="person-view">',
 '<div class="person-tabs"><label for="person-view-lineage">系統別</label><label for="person-view-kana">五十音順</label></div>',
 '<section class="person-view person-view-lineage" aria-label="系統別の人名">',
 '<p>系統を開くと人名一覧が出ます。年代が分かる人物は活動年代順、年代未詳は最後に並べます。</p>'
 ]
 for slug,title in GROUPS:
  rows=[p for p in PEOPLE if p[1]==slug]
  more='<p class="person-subindex"><a href="'+slug+'/">この系統だけの人物一覧へ →</a></p>'
  s.append(accordion(title,rows,more))
 s.append(accordion("系統未確定の千手氏",[p for p in PEOPLE if p[1]=="unknown"]))
 s.append(accordion("関連人物（千手氏以外）",[p for p in PEOPLE if p[1]=="related"]))
 s.extend(['</section>','<section class="person-view person-view-kana" aria-label="名前の五十音順">',
 '千手氏の人物だけを、名字を除いた名前の読みから探します。'])
 rows=[p for p in PEOPLE if p[1]!="related"]
 for group in KANA:
  label=group+"行"
  s.append(accordion(label,[p for p in rows if row_of(p)==label]))
 s.append(accordion("読み未確定",[p for p in rows if row_of(p)=="読み未確定"]))
 s.extend(['</section>','</div>',"",
 "## 個別人物記事へ","",
 "個別人物記事が公開され次第、両方の一覧から同じ固定URLへ進めるようにします。"
 "[人物記事の表示見本](../previews/person/)では構造を確認できます。","",
 "[系統・地域](../lineages/) ／ [時代から探す](../periods/) ／ [史料](../sources/) ／ [トップページへ戻る](../)",""])
 return "\n".join(s)

def build_subindex(slug,title):
 rows=[p for p in PEOPLE if p[1]==slug]
 return "\n".join([
 "# "+title+"｜人物一覧","",
 '<div class="archive-status">系統別人物索引 ／ 個別記事は順次公開</div>',"",
 "この系統に関係する人物の一覧です。活動時期が分かるものは年代順、"
 "不明なものは末尾に掲載します。調査候補であり、原史料の照合・同定は継続中です。","",
 '<nav class="article-context" aria-label="現在の索引位置"><span class="article-context-label">現在地</span>'
 '<a href="../">人物から探す</a><span class="article-context-separator">›</span>'
 '<strong>'+E(title)+'</strong><span class="article-context-kind">人物索引</span></nav>',"",
 "## 登録候補となる人物","",listing(rows),"",
 "個別人物記事を公開するまでは人名にリンクを設定していません。","",
 "[この系統の概要](../../lineages/"+slug+"/) ／ [人物一覧トップ](../) ／ "
 "[時代から探す](../../periods/) ／ [史料から探す](../../sources/)",""
 ])

output=DOCS/"persons"/"index.md"
output.parent.mkdir(parents=True,exist_ok=True)
output.write_text(build_index(),encoding="utf-8")
for slug,title in GROUPS:
 p=DOCS/"persons"/slug/"index.md"
 p.parent.mkdir(parents=True,exist_ok=True)
 p.write_text(build_subindex(slug,title),encoding="utf-8")
print("Generated person index and four lineage person subindexes from one JSON source.")
