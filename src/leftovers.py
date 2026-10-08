"""Where do the leftover letters come from? (the few letters per square that differ from the song)

Three explanations leave different fingerprints; each is tested against random copying slips of the same size.

  1. A skipped, added or swapped word (or a different wording of the song): the best single word-level edit of a
     square's piece (delete a run of 1-4 words, add a run of 1-4 words from anywhere in the song, or both).
  2. A square boundary misplaced on the paper: move each boundary between two squares by up to 13 letters.
  3. Handwriting look-alikes: extra and missing letters pairing as letters that look alike in cursive. The pairs are
     fixed in advance: e/l, e/i, e/c, i/l, n/u, v/u, a/o.

Uses the cut with the title "Einheitslied" in front (as the dashboard). Needs data/song.txt (fetch_song.py).
Writes results/leftovers.txt.
"""
import random, re
from collections import Counter
from pathlib import Path
import numpy as np
from common import ALPHABET, normalise, song_letters
from squares import load, letters
from partition import partition

ROOT = Path(__file__).resolve().parent.parent
TITLE = "Einheitslied"
PAIRS = {frozenset(p) for p in ["el", "ei", "ec", "il", "nu", "vu", "ao"]}
rng = random.Random(2026)
out = []


def say(s=""):
    print(s); out.append(s)


vec = lambda s: np.array([s.count(c) for c in ALPHABET])
squares = load()
text, cuts, cost = partition(normalise(TITLE))
words, pos = [], 0
for w in [TITLE] + re.findall(r"[A-Za-zÄÖÜäöüß]+", (ROOT / "data" / "song.txt").read_text(encoding="utf-8")):
    n = normalise(w); words.append((w, pos, pos + len(n), n)); pos += len(n)

say("Leftovers per square (song cut once, title in front):")
extra, missing = [], []
for k, sq in enumerate(squares):
    need, got = Counter(letters(sq)), Counter(text[cuts[k]:cuts[k + 1]])
    extra.append(need - got); missing.append(got - need)
    say(f"  S{k+1}: extra {''.join(sorted(extra[k].elements())) or '-':12s} missing {''.join(sorted(missing[k].elements())) or '-'}")

# 1. word-level edits ------------------------------------------------------------------------------------------
grams = {}
for i in range(len(words)):
    for n in range(1, 5):
        if i + n <= len(words):
            ws = words[i:i + n]
            grams.setdefault("".join(sorted("".join(x[3] for x in ws))), (" ".join(x[0] for x in ws), vec("".join(x[3] for x in ws))))
G = list(grams.values()); GV = np.array([g[1] for g in G])


def best_edit(need, pw):
    got = sum((vec(x[3]) for x in pw), np.zeros(26, int))
    best = (int(np.abs(need - got).sum()), "", "")
    runs = [("", np.zeros(26, int))] + [(" ".join(x[0] for x in pw[i:i + n]), sum((vec(x[3]) for x in pw[i:i + n]), np.zeros(26, int)))
                                        for i in range(len(pw)) for n in range(1, 5) if i + n <= len(pw)]
    for name, dv in runs:
        base = got - dv
        d = int(np.abs(need - base).sum())
        if d < best[0]: best = (d, name, "")
        ds = np.abs(need - (base + GV)).sum(1); j = int(ds.argmin())
        if ds[j] < best[0]: best = (int(ds[j]), name, G[j][0])
    return int(np.abs(need - got).sum()), best


say("\n1. Best single word-level edit vs the same on random letter slips of the same size (60 runs per square)")
freq = "eeeeeeeeeeeeeeeennnnnnnnniiiiiiissssssrrrrrrrtttttaaaaaadddddhhhhuuuulllgggocmbwfkzpv"
for k, sq in enumerate(squares):
    a, b = cuts[k], cuts[k + 1]
    pw = [w for w in words if w[1] >= a and w[2] <= b]
    core = vec("".join(x[3] for x in pw))
    need = vec(letters(sq)) - (vec(text[a:b]) - core)          # letters of words cut at the edges stay fixed
    d0, (d1, dele, add) = best_edit(need, pw)
    gains = []
    for _ in range(60):
        fake = core.copy()
        while np.abs(fake - core).sum() < d0:
            i, j = ALPHABET.index(rng.choice(freq)), ALPHABET.index(rng.choice(freq)); op = rng.random()
            if op < .34: fake[i] += 1
            elif op < .67 and fake[i] > 0: fake[i] -= 1
            elif fake[i] > 0 and i != j: fake[i] -= 1; fake[j] += 1
        e0, (e1, _, _) = best_edit(fake, pw); gains.append(e0 - e1)
    g = np.array(gains)
    say(f"  S{k+1}: {d0} -> {d1} (delete [{dele}] add [{add}]); random slips gain {g.mean():.1f} on average, "
        f"as much or more in {np.mean(g >= d0 - d1):.0%}")

# 2. square boundaries ----------------------------------------------------------------------------------------
song, _ = song_letters(); full = normalise(TITLE) + song
pre = [Counter()]
for ch in full:
    c = pre[-1].copy(); c[ch] += 1; pre.append(c)


def best_cut(sqs):
    need = [Counter(s) for s in sqs]
    best = {0: 0}
    for k, s in enumerate(sqs):
        nb = {}
        for a, cst in best.items():
            for L in range(len(s) - 25, len(s) + 26):
                b = a + L
                if b > len(full): break
                c = cst + sum(abs(need[k][ch] - (pre[b][ch] - pre[a][ch])) for ch in ALPHABET)
                if b not in nb or c < nb[b]: nb[b] = c
        best = nb
    return min(best.values())


say("\n2. Moving each square boundary on the paper by up to 13 letters (total letters off for all six squares)")
base = [letters(s) for s in squares]; c0 = best_cut(base)
for k in range(5):
    joined, n = base[k] + base[k + 1], len(base[k])
    res = min((best_cut(base[:k] + [joined[:n + m], joined[n + m:]] + base[k + 2:]), m) for m in range(-13, 14))
    say(f"  S{k+1}|S{k+2}: as written {c0}; best shift {res[1]:+d} letters gives {res[0]}")

# 3. look-alikes ----------------------------------------------------------------------------------------------
def pairs(ex, mi):
    ex, mi, best = list(ex.elements()), list(mi.elements()), [0]
    def rec(i, used, n):
        if i == len(ex): best[0] = max(best[0], n); return
        rec(i + 1, used, n)
        for j, m in enumerate(mi):
            if not used[j] and m != ex[i] and frozenset(ex[i] + m) in PAIRS:
                used[j] = True; rec(i + 1, used, n + 1); used[j] = False
    rec(0, [False] * len(mi), 0); return best[0]


real = [pairs(extra[k], missing[k]) for k in range(6)]
sims = []
for _ in range(4000):
    t = 0
    for k, sq in enumerate(squares):
        ne, nm = sum(extra[k].values()), sum(missing[k].values())
        t += pairs(Counter(rng.sample(letters(sq), ne)), Counter(rng.sample(text[cuts[k]:cuts[k + 1]], nm)))
    sims.append(t)
sims = np.array(sims)
say("\n3. Extra and missing letters pairing as cursive look-alikes (e/l, e/i, e/c, i/l, n/u, v/u, a/o)")
say(f"  observed {sum(real)} pairs (per square {real}); random slips {sims.mean():.1f} ± {sims.std():.1f}; "
    f"as many or more: p = {np.mean(sims >= sum(real)):.3f}")

(ROOT / "results" / "leftovers.txt").write_text("\n".join(out) + "\n", encoding="utf-8")
