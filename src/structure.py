"""What the note itself shows: the structure that pointed to a known text, a song.

Parts 1-4 use only the transcript (and, for part 4, ordinary German news as a reference), so they show what could be
seen before the text was known. Part 5 uses the song to check the hand-placement habit directly.

  1. Word breaks fall on the ends of 13-letter rows (the squares were copied out row by row).
  2. Dotted groups sit in reserved cells around each square's centre.
  3. Squares 2-5 are more alike in their letters than chance allows (a repeated part: a refrain); square 1 differs.
  4. The letter mix against ordinary German (too many f, w, n; too few b, c, a).
  5. With the text known: where the next letter of the song sits on the board, relative to the previous one.

Writes results/structure.txt and results/structure.json (the dashboard's "How it was found" view reads the JSON).
Part 4 downloads the same German news corpus as null_test.py; part 5 needs data/song.txt (fetch_song.py).
"""
import json
from collections import Counter
from pathlib import Path
import numpy as np
from common import ALPHABET
from squares import load, letters

ROOT = Path(__file__).resolve().parent.parent
W = 13
rng = np.random.default_rng(2026)
SQ = load()
out, lines = {}, []


def say(s=""):
    print(s); lines.append(s)


# 1. Word breaks on row ends ------------------------------------------------------------------------------------
say("1. Word breaks on the ends of 13-letter rows (null: the square's word lengths in random order)")
hits_real, null_tot, per = 0, np.zeros(20000, int), []
for k, sq in enumerate(SQ):
    n = len(sq)
    ends = [i for i, c in enumerate(sq) if c.wend]
    lengths = np.diff([-1] + ends)
    interior_row_ends = [i for i in range(W - 1, n - 1, W)]
    h = sum(1 for e in ends[:-1] if e % W == W - 1)
    null = np.empty(len(null_tot), int)
    for t in range(len(null_tot)):
        pos = np.cumsum(rng.permutation(lengths)) - 1
        null[t] = np.sum(pos[:-1] % W == W - 1)
    null_tot += null; hits_real += h
    per.append(dict(square=k + 1, cells=n, full_rows=n % W == 0, breaks=len(ends) - 1,
                    row_ends=len(interior_row_ends), on_row_end=h, expected=round(float(null.mean()), 1)))
    say(f"   S{k+1}: {n} cells{' (whole rows)' if n % W == 0 else ''}; {h} of {len(ends)-1} breaks on a row end, chance {null.mean():.1f}")
p1 = float(np.mean(null_tot >= hits_real))
say(f"   all squares: {hits_real} on row ends vs {null_tot.mean():.1f} by chance (p {max(p1, 1/len(null_tot)):.0e}{' or less' if p1 == 0 else ''})")
out["rows"] = dict(per_square=per, total=hits_real, expected=round(float(null_tot.mean()), 1), p=max(p1, 1 / len(null_tot)))

# 2. Dotted groups -----------------------------------------------------------------------------------------------
say("\n2. Dotted groups (row, column) in each 13-wide square; the centre of a full square is (6, 6)")
groups = []
for k, sq in enumerate(SQ):
    i = 0
    while i < len(sq):
        if sq[i].dotted:
            j = i
            while j < len(sq) and sq[j].dotted and sq[j].word == sq[i].word: j += 1
            cells = list(range(i, j))
            groups.append(dict(square=k + 1, word=sq[i].word, cells=cells))
            say(f"   S{k+1} {sq[i].word:10s} cells {[(c // W, c % W) for c in cells]}")
            i = j
        else:
            i += 1
s2 = [g for g in groups if g["square"] == 2]
if len(s2) == 2 and len(SQ[1]) == 169:
    mirror = sorted(168 - c for c in s2[0]["cells"]) == sorted(s2[1]["cells"])
    say(f"   S2's two groups are mirror images through the centre: {mirror}")
out["groups"] = groups

# 3. Squares 2-5 alike -------------------------------------------------------------------------------------------
say("\n3. Are squares 2-5 more alike than chance? (homogeneity chi-square of their letter counts; lower = more alike)")
body = [letters(SQ[k]) for k in (1, 2, 3, 4)]
pool = "".join(body); sizes = [len(b) for b in body]
keep = [c for c in ALPHABET if pool.count(c) >= 8]


def chi2(parts):
    M = np.array([[p.count(c) for c in keep] for p in parts], float)
    M = M[:, M.sum(0) > 0]
    E = M.sum(1, keepdims=True) * M.sum(0, keepdims=True) / M.sum()
    return float(((M - E) ** 2 / E).sum())


real = chi2(body)
arr = np.array(list(pool))
split = []
for _ in range(5000):
    a = rng.permutation(arr); cuts = np.cumsum(sizes)[:-1]
    split.append(chi2(["".join(x) for x in np.split(a, cuts)]))
split = np.array(split)
say(f"   S2-S5: chi-square {real:.1f}; random splits of their own letters {split.mean():.1f} ± {split.std():.1f}; "
    f"as alike or more: p {np.mean(split <= real):.3f}")
news = None
try:
    from null_test import corpus
    news = corpus()
except Exception as e:  # offline: skip the German reference
    say(f"   (German news reference skipped: {e})")
if news:
    gp = []
    for _ in range(3000):
        s = int(rng.integers(0, len(news) - sum(sizes) - 1)); parts, o = [], s
        for z in sizes: parts.append(news[o:o + z]); o += z
        gp.append(chi2(parts))
    gp = np.array(gp)
    say(f"   consecutive passages of German news, same sizes: {gp.mean():.1f} ± {gp.std():.1f}; as alike or more: p {np.mean(gp <= real):.3f}")
show = ["w", "u", "g", "n", "f", "c", "a", "l"]
table = {c: [letters(s).count(c) for s in SQ] for c in show}
for c in show:
    say(f"   {c}: " + " ".join(f"S{k+1} {v:2d}" for k, v in enumerate(table[c])))
out["alike"] = dict(chi2=round(real, 1), split_mean=round(float(split.mean()), 1), split_sd=round(float(split.std()), 1),
                    p_split=float(np.mean(split <= real)), counts=table,
                    sizes=[len(s) for s in SQ])
if news:
    out["alike"].update(german_mean=round(float(gp.mean()), 1), german_sd=round(float(gp.std()), 1), p_german=float(np.mean(gp <= real)))

# 4. Letter mix vs German --------------------------------------------------------------------------------------
if news:
    say("\n4. The note's letters against ordinary German (random windows of German news of the same length)")
    allx = "".join(letters(s) for s in SQ); n = len(allx); real_c = Counter(allx)
    a = np.frombuffer(news.encode(), dtype=np.uint8) - 97
    starts = rng.integers(0, len(a) - n, 4000)
    M = np.array([np.bincount(a[s:s + n], minlength=26) for s in starts])
    mix = []
    for i, c in enumerate(ALPHABET):
        m, sd = M[:, i].mean(), M[:, i].std() or 1
        mix.append(dict(letter=c, note=real_c[c], german=round(float(m), 1), z=round(float((real_c[c] - m) / sd), 1)))
    mix.sort(key=lambda d: -d["z"])
    say("   " + "  ".join(f"{d['letter']} {d['note']} vs {d['german']:.0f} ({d['z']:+.1f})" for d in mix if abs(d["z"]) >= 2))
    out["mix"] = dict(letters=n, rows=mix)

# 5. Hops, with the text known ---------------------------------------------------------------------------------
try:
    from partition import partition
    text, cuts, _ = partition()
except SystemExit as e:
    text = None; say(f"\n5. skipped: {e}")
if text:
    say("\n5. With the text known: where does the next letter of the song sit, relative to the previous one?")
    say("   For each step on the board (rows down, columns across), how often consecutive song letters are found that")
    say("   far apart, compared with the same square's letters shuffled (z-score; 6 squares combined).")
    OFF = [(dr, dc) for dr in (-1, 0, 1, 2) for dc in range(-4, 5) if (dr, dc) != (0, 0)]
    Z = {o: [] for o in OFF}; hopz = []
    HOP = [(0, -3), (0, -2), (0, 2), (0, 3), (1, -3), (1, -2), (1, 2), (1, 3)]
    for k, sq in enumerate(SQ):
        L = np.array([ord(c.letter) - 97 for c in sq]); n = len(L)
        piece = text[cuts[k]:cuts[k + 1]]
        P = np.zeros((26, 26))
        for x, y in zip(piece, piece[1:]): P[ord(x) - 97, ord(y) - 97] += 1
        H = np.bincount(L, minlength=26).astype(float); H[H == 0] = 1
        Wt = P / np.outer(H, H)
        r, c = np.arange(n) // W, np.arange(n) % W
        pairs = {}
        for dr, dc in OFF:
            I = np.arange(n); J = I + dr * W + dc
            ok = (J >= 0) & (J < n) & (c + dc >= 0) & (c + dc < W)
            pairs[(dr, dc)] = (I[ok], J[ok])
        shuf = [rng.permutation(L) for _ in range(400)]
        def stat(Lx, offs): return sum(Wt[Lx[pairs[o][0]], Lx[pairs[o][1]]].sum() for o in offs)
        for o in OFF:
            real_o = stat(L, [o]); nul = np.array([stat(s, [o]) for s in shuf])
            Z[o].append((real_o - nul.mean()) / (nul.std() or 1))
        real_h = stat(L, HOP); nul = np.array([stat(s, HOP) for s in shuf])
        hopz.append(float((real_h - nul.mean()) / nul.std()))
    comb = {o: float(np.sum(v) / np.sqrt(len(v))) for o, v in Z.items()}
    for dr in (-1, 0, 1, 2):
        say(f"   {'row ' + format(dr, '+d'):7s}" + " ".join(f"{('·' if (dr, dc) == (0, 0) else format(comb[(dr, dc)], '+.1f')):>5s}" for dc in range(-4, 5)))
    say(f"   columns: {' '.join(format(dc, '+d').rjust(5) for dc in range(-4, 5))}")
    say("   2-3 cells along the row or into the next row, per square: " + "  ".join(f"S{k+1} {z:+.1f}" for k, z in enumerate(hopz))
        + f";  combined {sum(hopz) / np.sqrt(6):+.1f}")
    out["hops"] = dict(grid=[[None if (dr, dc) == (0, 0) else round(comb[(dr, dc)], 2) for dc in range(-4, 5)] for dr in (-1, 0, 1, 2)],
                       rows=[-1, 0, 1, 2], cols=list(range(-4, 5)), per_square=[round(z, 1) for z in hopz],
                       combined=round(sum(hopz) / np.sqrt(6), 1))

(ROOT / "results" / "structure.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
(ROOT / "results" / "structure.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
