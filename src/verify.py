"""Verify the solution: each square's letters against the best consecutive stretch of the Einheitslied.

For every square, every stretch of the song (any start, length within a few letters of the square) is compared by
letter counts only - the order of letters inside a square is scrambled, the counts are not. Prints the best stretch,
how many letters are off, and S2's full letter table.
"""
from collections import Counter
from common import ALPHABET, letters_off, song_letters
from squares import load, letters
from windows import best_windows

song, _ = song_letters()
squares = load()
print(f"song: {len(song)} letters; note: {sum(len(s) for s in squares)} cells in {len(squares)} squares\n")
print("square  cells  best stretch of the song        letters off  stretch starts / ends")
best = {}
for k, sq in enumerate(squares, start=1):
    have = Counter(letters(sq)); n = len(sq)
    cands = []
    for start in range(len(song)):
        for length in range(n - 6, n + 7):
            if start + length <= len(song):
                cands.append((letters_off(have, Counter(song[start:start + length])), start, length))
    off, start, length = min(cands)
    best[k] = (start, start + length)
    print(f"  S{k}   {n:4d}   song[{start:4d}:{start + length:4d}]  ({length} letters)   {off:3d}        "
          f"\"{song[start:start + 12]}…\" / \"…{song[start + length - 12:start + length]}\"")
# S2 in full
start, end = best[2]
have, want = Counter(letters(squares[1])), Counter(song[start:end])
order = sorted(ALPHABET, key=lambda c: -(have[c] + want[c]))
order = [c for c in order if have[c] or want[c]]
print("\nS2 letter by letter (square vs song stretch):")
print("  letter " + " ".join(f"{c:>3}" for c in order))
print("  square " + " ".join(f"{have[c]:>3}" for c in order))
print("  song   " + " ".join(f"{want[c]:>3}" for c in order))
same = sum(have[c] == want[c] for c in order)
print(f"  {same} of {len(order)} letters have identical counts; letters off: {letters_off(have, want)}")
