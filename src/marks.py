"""The apostrophes mark the last letter of a word; ê marks a word-final e.

For each square: the marked letters (by letter) against the word-final consonants in the square's piece of the
song (the single back-to-back cut of partition.py), and ê against words ending in e.
"""
from collections import Counter
from common import song_letters
from squares import load
from partition import partition

song, finals = song_letters()
squares = load()
_, cuts, _ = partition("")
fmt = lambda c: " ".join(f"{k}{v}" for k, v in sorted(c.items(), key=lambda x: (-x[1], x[0])))
for k, sq in enumerate(squares, start=1):
    s, e = cuts[k - 1], cuts[k]
    marked = Counter(c.letter for c in sq if c.marked)
    ends = Counter(song[i] for i in range(s, e) if finals[i] and song[i] != "e")
    e_hat = sum(c.glyph == "ê" for c in sq)
    e_end = sum(1 for i in range(s, e) if finals[i] and song[i] == "e")
    print(f"S{k}: marked {sum(marked.values()):3d}  {fmt(marked)}")
    print(f"     word ends {sum(ends.values()):3d}  {fmt(ends)}")
    print(f"     ê {e_hat}  vs  words ending in e {e_end}\n")
