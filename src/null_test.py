"""How close does ordinary German come to the squares by chance?

Downloads a public German corpus (Leipzig Corpora Collection, news 2020, 100k sentences; ~13 M letters), slides a
window over it for each square, and reports the best (lowest) letters-off any window achieves, plus the share of
windows within a given distance. Measure: letters left over in the square + letters of the window missing from it (as in partition.py).
A second pass allows any window length within 25 letters of the square's size, the same freedom the song pieces get.
"""
import tarfile, urllib.request
from collections import Counter
from pathlib import Path
import numpy as np
from common import ALPHABET, normalise
from squares import load, letters

URL = "https://downloads.wortschatz-leipzig.de/corpora/deu_news_2020_100K.tar.gz"
DATA = Path(__file__).resolve().parent.parent / "data"


def corpus() -> str:
    tgz = DATA / "deu_news_2020_100K.tar.gz"
    if not tgz.exists():
        DATA.mkdir(exist_ok=True)
        print("downloading", URL); urllib.request.urlretrieve(URL, tgz)
    with tarfile.open(tgz) as t:
        m = next(x for x in t.getmembers() if x.name.endswith("sentences.txt"))
        raw = t.extractfile(m).read().decode("utf-8", "ignore")
    return normalise(" ".join(line.split("\t", 1)[-1] for line in raw.splitlines()))


def best_flexible(cum, want, n, flex=25, chunk=1_000_000):
    """Best window of ANY length n-flex..n+flex (as the song pieces are allowed in partition.py)."""
    best = 10 ** 9
    N = cum.shape[0] - 1
    for L in range(n - flex, n + flex + 1):
        for s in range(0, N - L + 1, chunk):
            e = min(s + chunk, N - L + 1)
            off = np.abs(cum[s + L:e + L] - cum[s:e] - want).sum(1)
            best = min(best, int(off.min()))
    return best


if __name__ == "__main__":
    text = corpus()
    a = np.frombuffer(text.encode(), dtype=np.uint8) - 97
    cum = np.zeros((len(a) + 1, 26), np.int32)
    np.add.at(cum, (np.arange(1, len(a) + 1), a), 1); cum = np.cumsum(cum, 0)
    print(f"corpus: {len(text):,} letters of German news\n")
    print("square  best window (letters unaccounted for)   share within 20   within 30   median")
    flexible = []
    for k, sq in enumerate(load(), start=1):
        n = len(sq); want = np.array([Counter(letters(sq))[c] for c in ALPHABET])
        off = np.abs((cum[n:] - cum[:-n]) - want).sum(1)          # letters left over + letters missing
        print(f"  S{k}         {off.min():3d}                              {np.mean(off <= 20):.1e}       {np.mean(off <= 30):.1e}     {int(np.median(off))}")
        flexible.append(best_flexible(cum, want, n))
    print("\nSame, but allowing any window length within 25 letters of the square's size (as the song pieces are):")
    for k, b in enumerate(flexible, start=1):
        print(f"  S{k}         {b:3d}")
