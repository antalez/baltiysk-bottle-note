"""The search that found the text: an order-free letter-count sieve.

Scrambling letters inside a square changes their order, not their counts. So for any candidate text, every window
with as many letters as a square is compared with the square by letter counts ("letters off"). A true source scores
close to 0 for its square; unrelated German text of this length stays far away (in 592 million letters of German
Wikisource and 475 books the best window was 13+ letters off for S2).

usage: python sieve.py FILE_OR_DIR [...]      (plain-text files; data/song.txt is the song after fetch_song.py)
"""
import sys
from collections import Counter
from pathlib import Path
import numpy as np
from common import ALPHABET, normalise
from squares import load, letters

IDX = {c: i for i, c in enumerate(ALPHABET)}


def scan(text, squares):
    t = normalise(text)
    if len(t) < 100:
        return {}
    a = np.frombuffer(t.encode(), dtype=np.uint8) - 97
    onehot = np.zeros((len(t) + 1, 26), np.int32); onehot[np.arange(1, len(t) + 1), a] = 1
    cum = np.cumsum(onehot, 0)
    out = {}
    for k, sq in enumerate(squares, start=1):
        n = len(sq)
        if len(t) < n:
            continue
        want = np.array([Counter(letters(sq))[c] for c in ALPHABET])
        win = cum[n:] - cum[:-n]
        off = np.abs(win - want).sum(1) // 2
        i = int(off.argmin()); out[k] = (int(off[i]), t[i:i + 40])
    return out


if __name__ == "__main__":
    files = []
    for arg in sys.argv[1:] or [str(Path(__file__).resolve().parent.parent / "data" / "song.txt")]:
        p = Path(arg); files += sorted(p.rglob("*.txt")) if p.is_dir() else [p]
    squares = load()
    best = {k: [] for k in range(1, len(squares) + 1)}
    for f in files:
        for k, (off, snippet) in scan(f.read_text(encoding="utf-8", errors="ignore"), squares).items():
            best[k].append((off, f.name, snippet))
    for k in best:
        top = sorted(best[k])[:3]
        print(f"S{k}: " + " | ".join(f"{off} off: {name} \"{snip}…\"" for off, name, snip in top))
