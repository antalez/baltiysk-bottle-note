"""Shared helpers: letter normalisation, letter-count vectors, the song as a letter stream."""
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SONG = ROOT / "data" / "song.txt"
ALPHABET = "abcdefghijklmnopqrstuvwxyz"


def normalise(text: str) -> str:
    """Lower case letters only; umlauts folded (ä->a, ö->o, ü->u), ß -> ss."""
    t = text.lower().replace("ä", "a").replace("ö", "o").replace("ü", "u").replace("ß", "ss")
    return re.sub("[^a-z]", "", t)


def song_letters():
    """The song as (letters, word_final_flags). Run src/fetch_song.py first."""
    if not SONG.exists():
        raise SystemExit("data/song.txt missing - run: python src/fetch_song.py")
    letters, finals = [], []
    for w in re.findall(r"[A-Za-zÄÖÜäöüß]+", SONG.read_text(encoding="utf-8")):
        w = normalise(w)
        for i, ch in enumerate(w):
            letters.append(ch)
            finals.append(i == len(w) - 1)
    return "".join(letters), finals


def letters_off(a: Counter, b: Counter) -> int:
    """Number of letters that would have to change to turn multiset a into multiset b (plus any length difference)."""
    diff = sum(abs(a[c] - b[c]) for c in ALPHABET)
    return (diff + abs(sum(a.values()) - sum(b.values()))) // 2
