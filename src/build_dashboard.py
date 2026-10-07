"""Build dashboard/data.js for dashboard/index.html (open the HTML file in a browser afterwards).

The song lyrics are not stored in the repository, so run `python src/fetch_song.py` first; this script embeds the
squares, the transcript and the downloaded song into a local data file (git-ignored).
"""
import json, re
from pathlib import Path
from common import normalise
from squares import TRANSCRIPT, SQUARE_ENDS, LETTER, load
from partition import partition

ROOT = Path(__file__).resolve().parent.parent
TITLE = "Einheitslied"

squares = load()
sq_json = [[dict(g=c.glyph, l=c.letter, m=c.marked, d=c.dotted, line=c.line, e=c.wend) for c in s] for s in squares]

# transcript lines with each written word's cells
lines, k, i = [], 0, 0
raw = TRANSCRIPT.read_text(encoding="utf-8")
for n, line in enumerate((l for l in raw.splitlines() if l.strip()), start=1):
    words = []
    for word in line.split():
        if word == "eimat":
            words.append(dict(w="eimat ..........", cells=[], out=True)); continue
        dotted = word.count(".") >= 2
        core = (word.replace(".", "") if dotted else word).replace("f2", "f")
        cells = []
        for tok in re.findall(r"[A-Za-zäöüê]['\"]*", core):
            cells.append([k, i]); i += 1
        words.append(dict(w=word.replace("'", "′").replace('"', "″").replace("f2", "f₂"), cells=cells, dot=dotted))
        if n in SQUARE_ENDS and word.endswith(SQUARE_ENDS[n]):
            k, i = k + 1, 0
    lines.append(words)

# the text: title + song, as letters, with word spans for display
song_raw = (ROOT / "data" / "song.txt").read_text(encoding="utf-8")
words, pos = [], 0
for w in [TITLE] + re.findall(r"[A-Za-zÄÖÜäöüß]+", song_raw):
    nw = normalise(w)
    words.append(dict(w=w, a=pos, b=pos + len(nw))); pos += len(nw)
text, cuts, cost = partition(normalise(TITLE))
assert len(text) == pos
# the structure evidence (src/structure.py) and the public photos (src/fetch_photos.py), if present
st = ROOT / "results" / "structure.json"
story = json.loads(st.read_text(encoding="utf-8")) if st.exists() else None
photos = [f"../data/photos/{n}" for n in ("page1.png", "page2.png") if (ROOT / "data" / "photos" / n).exists()]
data = dict(squares=sq_json, lines=lines, text=text, words=words, cuts=cuts, cost=cost, title=TITLE, story=story, photos=photos)
out = ROOT / "dashboard" / "data.js"
out.write_text("window.NOTE=" + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + ";\n", encoding="utf-8")
print(f"wrote {out} ({out.stat().st_size // 1024} KB); cuts {cuts}, total letters off {cost}")
