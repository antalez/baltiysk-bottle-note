"""Best consecutive stretch of the song for each square (letter counts only)."""
from collections import Counter
from common import letters_off
from squares import letters


def best_windows(song, squares):
    out = {}
    for k, sq in enumerate(squares, start=1):
        have = Counter(letters(sq)); n = len(sq)
        cands = [(letters_off(have, Counter(song[s:s + L])), s, L)
                 for s in range(len(song)) for L in range(n - 6, n + 7) if s + L <= len(song)]
        off, s, L = min(cands)
        out[k] = (s, s + L, off)
    return out
