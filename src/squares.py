"""Parse the transcript into the note's six squares.

Each square is a list of cells (in copy order: rows of 13, left to right). A cell records the glyph as written,
the letter it stands for (ê -> e, ö -> o, ü -> u), whether it carries the word-end mark (apostrophe), and whether it
belongs to a dotted group (r.s.f.d. etc.). Squares end at the underlined last letters (followed by a full stop).
"""
import re
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TRANSCRIPT = ROOT / "transcript" / "transcript_v3.4.txt"
# ending of the last copied word of squares 1-5, by line number (square 6 runs to the end of line 25;
# "eimat" lies outside the squares)
SQUARE_ENDS = {5: "nenet'se.", 9: "np.", 13: "ngwsaetme.", 17: "eamdemn.", 22: "êain."}
LETTER = {"ê": "e", "ö": "o", "ü": "u"}


@dataclass
class Cell:
    glyph: str      # as written (lower case except the one capital A)
    letter: str     # plain letter a-z
    marked: bool    # apostrophe (or double tick) after the letter
    dotted: bool    # part of a dotted group
    line: int       # transcript line (1-25)
    word: str       # the written word it belongs to
    wend: bool = False  # last letter of a written word (a word break follows)


def load(path=TRANSCRIPT):
    text = path.read_text(encoding="utf-8")
    text = text[: text.index("eimat")]
    squares = [[]]
    for n, line in enumerate((l for l in text.splitlines() if l.strip()), start=1):
        for word in line.split():
            dotted = word.count(".") >= 2
            core = (word.replace(".", "") if dotted else word).replace("f2", "f")
            for tok in re.findall(r"[A-Za-zäöüê]['\"]*", core):
                g = tok[0]
                squares[-1].append(Cell(g, LETTER.get(g.lower(), g.lower()), "'" in tok or '"' in tok, dotted, n, word))
            squares[-1][-1].wend = True
            if n in SQUARE_ENDS and word.endswith(SQUARE_ENDS[n]):
                squares.append([])
    return [s for s in squares if s]


def letters(square):
    return "".join(c.letter for c in square)


if __name__ == "__main__":
    for k, s in enumerate(load(), start=1):
        print(f"S{k}: {len(s)} cells ({len(s) / 13:.2f} rows of 13)")
