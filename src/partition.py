"""Cut the song ONCE into six consecutive pieces (no overlaps, no gaps), one per square, choosing the cut points that
minimise the total letters off; optionally with a title before the song. Then cross out, in each square, the letters
its piece uses, and list exactly what is left over on both sides.
"""
import sys
from collections import Counter
from common import ALPHABET, song_letters
from squares import load, letters

def partition(title=""):
    """Cut title+song into six consecutive pieces minimising letters off. Returns (text, cuts, cost)."""
    song, _ = song_letters()
    squares = load()
    text = title + song
    need = [Counter(letters(s)) for s in squares]
    N = len(text)

    def off(k, a, b):
        got = Counter(text[a:b])
        return sum(abs(need[k][c] - got[c]) for c in ALPHABET)

    best = {0: (0, [0])}
    for k, sq in enumerate(squares):
        nb = {}
        for a, (cost, cuts) in best.items():
            for L in range(len(sq) - 25, len(sq) + 26):
                b = a + L
                if b > N:
                    break
                c = cost + off(k, a, b)
                if b not in nb or c < nb[b][0]:
                    nb[b] = (c, cuts + [b])
        best = nb
    cost, cuts = min(best.values())
    return text, cuts, cost


if __name__ == "__main__":
    TITLE = sys.argv[1] if len(sys.argv) > 1 else ""
    text, cuts, cost = partition(TITLE)
    squares = load(); need = [Counter(letters(s)) for s in squares]; N = len(text)

    print(f"title: {TITLE or '(none)'}; total letters off: {cost} (added+removed); text ends at {cuts[-1]} of {N} "
          f"(next: '{text[cuts[-1]:cuts[-1] + 25]}')\n")
    for k in range(6):
        a, b = cuts[k], cuts[k + 1]
        have, got = need[k], Counter(text[a:b])
        extra = Counter({c: have[c] - got[c] for c in ALPHABET if have[c] > got[c]})
        missing = Counter({c: got[c] - have[c] for c in ALPHABET if got[c] > have[c]})
        print(f"S{k + 1}: text[{a}:{b}] ({b - a} letters, square {sum(have.values())})  "
              f"\"{text[a:a + 18]}…{text[b - 18:b]}\"")
        print(f"     left over in the square (not used by the text): {''.join(sorted(extra.elements())) or '—'}")
        print(f"     text letters not found in the square:            {''.join(sorted(missing.elements())) or '—'}")
