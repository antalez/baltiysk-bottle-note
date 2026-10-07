"""Build the data files for dashboard/index.html.

  dashboard/data.js        public (committed, used by the live page): the squares, the transcript, the cut points,
                           per-piece letter counts and short excerpts. It contains no song lyrics.
  dashboard/data.local.js  local only (git-ignored): the same plus the full song text, so the dashboard can show
                           each square's whole piece of the song. Needs data/song.txt (run src/fetch_song.py first).

The page loads data.local.js when it exists and falls back to data.js.
"""
import json, re
from collections import Counter
from pathlib import Path
from common import normalise
from squares import TRANSCRIPT, SQUARE_ENDS, load
from partition import partition

ROOT = Path(__file__).resolve().parent.parent
TITLE = "Einheitslied"
PHOTO_URLS = ["https://scienceblogs.de/klausis-krypto-kolumne/files/2016/09/Kaliningrad-Cryptogram1.png",
              "https://scienceblogs.de/klausis-krypto-kolumne/files/2016/09/Kaliningrad-Cryptogram-2.png"]
EXCERPT = 3  # words shown at each end of a piece in the public file

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

# the text: title + song, as letters, with word spans
song_raw = (ROOT / "data" / "song.txt").read_text(encoding="utf-8")
words, pos = [], 0
for w in [TITLE] + re.findall(r"[A-Za-zÄÖÜäöüß]+", song_raw):
    nw = normalise(w)
    words.append(dict(w=w, a=pos, b=pos + len(nw))); pos += len(nw)
text, cuts, cost = partition(normalise(TITLE))
assert len(text) == pos

# per-piece summaries for the public file: letter counts, word-final letters, a few words at each end
pieces = []
for k in range(len(squares)):
    a, b = cuts[k], cuts[k + 1]
    inside = [w for w in words if w["b"] > a and w["a"] < b]
    finals = Counter(text[w["b"] - 1] for w in words if a <= w["b"] - 1 < b)
    pieces.append(dict(a=a, b=b, T=dict(Counter(text[a:b])), F=dict(finals),
                       head=" ".join(w["w"] for w in inside[:EXCERPT]), tail=" ".join(w["w"] for w in inside[-EXCERPT:])))

st = ROOT / "results" / "structure.json"
story = json.loads(st.read_text(encoding="utf-8")) if st.exists() else None
base = dict(squares=sq_json, lines=lines, cuts=cuts, cost=cost, title=TITLE, story=story, pieces=pieces)

local_photos = [f"../data/photos/{n}" for n in ("page1.png", "page2.png") if (ROOT / "data" / "photos" / n).exists()]
public = dict(base, photos=PHOTO_URLS)
local = dict(base, photos=local_photos or PHOTO_URLS, text=text, words=words)


def write(name, data):
    out = ROOT / "dashboard" / name
    out.write_text("window.NOTE=window.NOTE||" + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + ";\n", encoding="utf-8")
    print(f"wrote {out} ({out.stat().st_size // 1024} KB)")


write("data.js", public)
write("data.local.js", local)
print(f"cuts {cuts}, total letters off {cost}")
