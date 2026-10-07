# The Baltiysk bottle note — solved

In 2015 workers digging a gas trench by Lenin Street 64–66 in Baltiysk (Kaliningrad region, Russia; formerly Pillau) found a bottle with two exercise-book sheets covered in letter groups that nobody could read: *"en'ifvn d't'öhn'fdê elhrikiracel etê deluwrs …"*. The note became No. 19 on Klaus Schmeh's list of the most important unsolved encrypted messages.

**It is a song.** The note is the text of the GDR youth song **"Einheitslied"** from the *Freundschaftskantate der Jugend* (words: Herbert Keller, music: André Asriel) — the stanzas *Freundschaft! Allen Völkern Freundschaft …*, *Einheit! …* and the start of *Frieden! …* — cut into six consecutive pieces of about 169 letters. Each piece was written into a 13 × 13 square with its letters jumbled, and the squares were copied row by row with invented word breaks. Below the last square stands **"eimat"** followed by dots — most likely the end of *Heimat* (*"Singen soll die Heimat"*), which follows a few words after the last square's text.

## The proof

Jumbling letters inside a square changes their order, not their counts. Cutting the song **once** into six back-to-back pieces (no overlaps, no gaps; `src/partition.py`) and crossing out in each square the letters its piece uses:

| Square | Cells | Piece of the song (letters) | Left over in the square | Text letters missing |
|---|---|---|---|---|
| S1 | 166 | 0–157 — *"Freundschaft! Allen Völkern Freundschaft …"* | d e e e i l l n s s t | f u |
| **S2** | **169** | **157–325** — *"…werden wir erringen, wenn wir fest zusammenstehn …"* | **l** | **none** |
| S3 | 162 | 325–495 — *"…unser Deutschland ganz gehören … Einheit! …"* | e e | c c i i l n n r r u |
| S4 | 169 | 495–658 — *"…wollen alle guten Menschen für das deutsche Land …"* | i i l l l l n n t | e e e |
| S5 | 169 | 658–827 — *"…keine Bombe zerstören … Frieden!"* | d f n n | h i s u |
| S6 | 143 | 827–974 — *"…Völkern Frieden … wenn wir fest zusammensteh(n)"* | a d s s | c m r r t u u u |

S2, letter by letter: all 168 letters of its piece are in the square; one *l* is left over.

```
letter   e   n   s   r   i   f   h   u   w   l   d   a   o   t   m   c   g   b   k   z   p
square  28  24  16  14  13   7   7   7   7   7   6   6   5   5   4   3   3   2   2   2   1
song    28  24  16  14  13   7   7   7   7   6   6   6   5   5   4   3   3   2   2   2   1
```

What remains in the other squares: S1 and S3 have fewer cells than their text (166 and 162 instead of 169 — the writer dropped some letters), and the other squares differ by a few letters. For S4 we checked on the 2015 scans: its extra *l* are clearly written *l*, so those differences are on the paper (copying slips, or the wording of the copy the writer used). The other squares have not been re-checked letter by letter.

## Why this is not a coincidence

All numbers below use one measure: letters left over in the square plus letters of the text missing from it.

- **Chance.** In 8.9 million letters of German news (Leipzig corpus), the best window for each square, chosen freely, leaves 20–36 letters unaccounted for (S2: 24). The song, cut once into consecutive pieces, leaves S2 1 and the others 8–13 (`src/null_test.py`, `results/null_test.txt`).
- **Other transcriptions.** A transcription posted on d3.ru in July 2015 and Thomas Ernst's of 2017 give the same result for S2 as ours (all 168 letters, one extra *l*). Ours started from Ernst's and was re-verified symbol by symbol (`src/check_transcriptions.py`, `results/check_transcriptions.txt`).
- **Order.** Each square's best-matching stretch, found independently, falls in the song's own order (chance 1 in 720; `src/significance.py`).
- **The marks.** The apostrophes mark word ends. In S1, S3 and S4 no other stretch of the song matches a square's marked letters as well as its own piece (p ≈ 0.001 each); S2 p ≈ 0.01, S5 ≈ 0.07, S6 not significant (`results/significance.txt`).

## How the note was made

- **Pieces.** The song's letters (no spaces or punctuation; the writer kept *ö* and *ü*) cut into consecutive pieces of about 169 = 13 × 13. Whether S1 begins with the title *Einheitslied* is open: with the title in front the total fit improves slightly (`results/partition_with_title.txt`).
- **Filling.** Each piece written into its square letter by letter, moving right and down: the next song letter sits 2–4 cells to the right in the same row, or in the next row down, more often than chance, and almost never back in the row above — positive in every square, clearly so in combination (`results/structure.txt`). The exact writing order cannot be recovered; the song repeats letters too much.
- **Word ends marked.** An apostrophe marks the last letter of a word (*t′* ends *Freundschaft*, *Einheit*, *Welt*; *n′* ends *allen*, *wollen*, *singen* …); *ê* marks a word-final *e* (`results/marks.txt`).
- **Copied** row by row onto the two sheets with invented word breaks; each square's last letter underlined.
- **Dotted groups** (*r.s.f.d. c.f. f.t′.f.*, *r.l.b. s.n.c.*, …): letters of the song placed in reserved cells around each square's centre. Their meaning is open — see `docs/open_questions.md`.

## How it was found

The note itself pointed the way. Its sections are 13 × 13 squares filled by hand: letters 2–3 cells apart, along the row or into the next row down, are weakly linked, but no key or rule reorders them (hundreds of grilles, routes and keyed transpositions failed; see `docs/method.md`). So the text could only be **recognised**, not decrypted. Sections 2–5 share about 60 letters each that section 1 lacks — the shape of stanzas with a refrain after an opening — and the letters favour a collective German "wir werden … wenn …" voice with words like *Freundschaft*, *Frieden* and *Heimat* (*eimat* below the last square). That pointed to a song of the Pioneer/youth kind. Letter counts survive any jumbling, so every square was compared, by counts, with every window of candidate texts. Bibles, German Wikisource, books, the Soviet-German newspaper *Freundschaft*, German folk songs and Russian songs gave no match. A collection of 1,762 songs and poems, most of them from the GDR song archive *lieder-aus-der-ddr.de*, contained the Einheitslied.

## Reproduce

```bash
pip install numpy
python src/fetch_song.py           # downloads the lyrics to data/song.txt (not redistributed here)
cd src
python squares.py                  # the six squares
python partition.py                # the song cut once into six pieces; left over / missing per square
python verify.py                   # each square's best stretch, found independently
python marks.py                    # apostrophes vs word ends
python significance.py             # order and marks tests
python check_transcriptions.py     # S2 in the 2015 transcription
python null_test.py                # chance baseline (downloads ~30 MB of German news)
python sieve.py ../data/song.txt   # the letter-count search (or any folder of .txt files)
python structure.py                # what the note itself shows: rows of 13, dotted groups, the refrain, the letter mix, the hops
```

## Dashboard

An interactive page shows every square with the letters used by its piece of the song crossed out, what is left over and what is missing. Its **How it was found** tab walks through the clues, with charts, that led from the note to a song.

```bash
python src/fetch_song.py && python src/fetch_photos.py   # lyrics and the two public photos, saved locally (not redistributed)
cd src && python structure.py && python build_dashboard.py   # writes results/structure.json and dashboard/data.js
open ../dashboard/index.html                                # or double-click it (index.html#story opens the story)
```

## Files

- `transcript/transcript_v3.4.txt` — the note, line by line; `transcript/NOTATION.md` explains the notation; `transcript/earlier/` holds the 2015 forum transcription.
- `src/` — the scripts above; `results/` — their output; `dashboard/` — the interactive page.
- `docs/method.md` — what was tried, what failed and why, and how the solution was confirmed.
- `docs/open_questions.md` — the dotted groups, the remaining differences, the author.

## Credits

Solved by Anton Zaytsev (October 2026), with AI assistance (Claude, Anthropic).
Thanks to the 2015 transcriber on d3.ru and to Thomas Ernst (2017) for earlier transcriptions; to Klaus Schmeh for keeping the case alive; to *Strana Kaliningrad* for the original report; and to *lieder-aus-der-ddr.de* for preserving the song.

The song lyrics are © their rights holders and are not included in this repository. Code: MIT licence. Text and tables: CC BY 4.0.
