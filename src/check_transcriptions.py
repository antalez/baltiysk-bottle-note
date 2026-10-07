"""S2 against the song in transcriptions made by other people.

transcript/earlier/d3ru_2015.txt (a 2015 forum transcription, made the week the note was published) is read and S2
(the letters from "emnh" to "np.") compared with the song stretch used by partition.py. Thomas Ernst's 2017
transcription gave the same result (it is not reproduced here; see results/check_transcriptions.txt).
"""
import re
from collections import Counter
from pathlib import Path
from common import ALPHABET, song_letters
from squares import load, letters
from partition import partition

ROOT = Path(__file__).resolve().parent.parent
text, cuts, _ = partition("")
piece = Counter(text[cuts[1]:cuts[2]])


def s2_from(raw):
    t = raw[raw.index("emnh"):]; t = t[:t.index("np.") + 3]
    return Counter({"ê": "e", "ö": "o", "ü": "u", "x": "r"}.get(c, c) for c in re.findall(r"[a-zäöüêx]", t.lower()))


def report(name, c):
    diff = {ch: c[ch] - piece[ch] for ch in ALPHABET if c[ch] != piece[ch]}
    print(f"{name:28s} S2 letters {sum(c.values())}; vs song piece ({sum(piece.values())}): differences {diff or 'none'}")


report("ours (v3.4)", Counter(letters(load()[1])))
d3 = (ROOT / "transcript" / "earlier" / "d3ru_2015.txt").read_text(encoding="utf-8").split("\n", 3)[3]
report("d3.ru, July 2015", s2_from(d3))
