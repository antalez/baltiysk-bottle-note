"""Two checks that do not depend on letter counts of the text itself.

1. Order: the six squares' best stretches fall in the song's own order (S1 < S2 < … < S6). If each square's best
   stretch were placed at random, all six in order happens with probability 1/720.
2. Marks: in each square, the apostrophe-marked letters are compared with the word-final consonants of its own
   piece of the song (the single back-to-back cut of partition.py), and with those of every other stretch of the
   same length. If the marks are the writer's
   word-end marks for this text, the own stretch should fit better than almost all others.
"""
from collections import Counter
import math
from common import ALPHABET, song_letters
from squares import load
from windows import best_windows
from partition import partition

song, finals = song_letters()
squares = load()
win = best_windows(song, squares)
starts = [win[k][0] for k in sorted(win)]
print("best-stretch starts:", starts)
print(f"each square's best stretch, found independently, falls in song order: {starts == sorted(starts)}   (chance: 1/{math.factorial(6)})\n")
_, cuts, _ = partition("")


def ends_vector(s, e):
    return Counter(song[i] for i in range(s, e) if finals[i] and song[i] != "e")


for k, sq in enumerate(squares, start=1):
    marks = Counter(c.letter for c in sq if c.marked and c.letter != "e")
    s, e = cuts[k - 1], cuts[k]; L = e - s
    dist = lambda v: sum(abs(marks[c] - v[c]) for c in ALPHABET)
    own = dist(ends_vector(s, e))
    others = [dist(ends_vector(o, o + L)) for o in range(0, len(song) - L) if abs(o - s) > L // 2]
    better = sum(d <= own for d in others)
    print(f"S{k}: marks vs word ends of its own stretch: distance {own:2d};  other stretches of the song as close or closer: "
          f"{better} of {len(others)}  (p ≈ {max(better, 1) / len(others):.3f})")
