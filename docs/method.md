# Method: how the note was read

The short version: the note itself showed that it was a known text with a repeated part, jumbled by hand inside squares. That ruled out finding a key and pointed to a song. Letter counts, which survive any jumbling, then found it.

## 1. Transcription
The note was re-transcribed symbol by symbol from the best available images, checked by three independent "blind" readers for page 1 and two for page 2, and finally reviewed line by line by hand. The key conventions: the writer's *z*-shaped letter is an *r*; apostrophes, *ê*, *ö*, *ü* and dotted groups are recorded as marks, not letters.

## 2. What the note showed before the text was known
- **13 × 13 squares.** The six sections (each ending on an underlined letter) have 166, 169, 162, 169, 169 and 143 letters; four fill whole rows of 13 exactly, and the invented word breaks fall on row ends far more often than chance. Each section was laid out in its own 13 × 13 square and copied out row by row.
- **A repeated part.** Sections 2–5 are more alike in their letters than pieces of ordinary German are. Simulations put the shared part at about 60 letters per section (roughly a third), while section 1 lacks it. That is the shape of stanzas with a refrain, with section 1 as the opening.
- **The register.** The letters favour German words like *wir*, *wenn* and *werden* and avoid *ich*, *auch* and *nicht*: a collective "we will …, if …" voice, as in a pledge or a song. The shared letters fit words like *Freundschaft*, *Frieden* and *Heimat*. Below the last square stands *eimat*, most likely the end of *Heimat*.
- **A hand habit, not a key.** Neighbouring letters in the copy are unrelated, but letters 2–3 cells apart are weakly linked: along the same row (either way) or into the next row down. The writer seems to have put each next letter a short hop away, skipping the adjacent cell, and moved down through the square.
- **Dotted groups** sit in reserved cells placed around each square's centre (on the middle row, or in centre-symmetric pairs).

## 3. Why decryption failed, and what that implied
Every keyed or rule-based reordering was tested on planted German text first, then on the note against shuffled controls. The list covers turning grilles (including the centre written on every turn), routes and spirals, magic squares, affine and step-key fills (millions of variants), keyword columns, double transposition, Nihilist, VIC-style disrupted transposition, letter-steered routes, and stripe and chessboard readings. All came out at chance level. Decoders following the hop habit picked up the structure but could not read text from it: each square allows on the order of 10⁶⁶ hand-chosen paths, more than any language model can resolve.

**Conclusion:** the letters were placed by hand, freely, so there was no key to find. The note could only be read by **recognising the text**. With a refrain and a "we" voice, the best candidate was a song.

## 4. The search that worked
Jumbling inside a square changes the order of the letters, not their counts. For each square, every stretch of a candidate text with the same number of letters was compared by letter counts. The test was calibrated on planted sources first.

What was searched, and what was missed for too long:
- **General German text** (no match): German Bibles, the full German Wikisource dump (297,793 pages), 475 books, 108 issues of the Soviet-German newspaper *Freundschaft*, Pioneer and school texts.
- **Songs with refrains:** 11,178 German folk songs and Russian revolutionary and Soviet songs (no match). Some time was also lost on wrong ideas: spelling habits invented to explain the odd letter mix, and a Russian "private alphabet".
- **The register the clues pointed at, searched last:** GDR youth and Pioneer songs. A collection of 1,762 songs and poems (82 gathered first, then 1,680 from the GDR song archive lieder-aus-der-ddr.de) contained the **Einheitslied**. It matched S2 to 1 letter and every other square far better than any other text.

## 5. Confirmation
- Cut once into six back-to-back pieces, the song accounts for S2 to one letter and for the other squares to 8–13 letters. The best stretches in 8.9 million letters of German news leave 20–36.
- S2 gives the same one-letter difference in a 2015 forum transcription, in Thomas Ernst's 2017 transcription and in ours (which started from Ernst's and was re-verified symbol by symbol).
- The six squares' best stretches fall in the song's own order (chance 1 in 720).
- The song explains what the note showed:
  - the repeated part of S2–S5 is the refrain (*"… werden wir erringen, wenn wir fest zusammenstehn"*);
  - S1 is the opening stanza;
  - the odd letter mix is the song's own;
  - *eimat* is most likely the end of *Heimat*, a few words after the last square's text (the exact join is not pinned down).
- The apostrophes mark word endings: in S1, S3 and S4 a square's marked letters fit its own piece of the song better than any other stretch of the song.
- With the text known, the hop habit is visible directly (`src/structure.py`): the next song letter sits 2–4 cells to the right in the same row, or in the next row down, more often than chance, and almost never back in the row above. The writer moved right and down through each square. This holds in all six squares and is clear in combination (z ≈ +4.5), though weak in each square on its own. The exact writing order cannot be recovered, because the song repeats letters too much.

## 6. Lessons
- When the structure says no key exists, stop decoding and identify the text: letter counts survive any jumbling.
- Read the structure for the kind of text. A repeated part across sections means a refrain; the voice and vocabulary give the genre. Search that genre early, with complete collections rather than shortlists.
- Distrust explanations fitted to the data: the "spelling habits" invented to explain the odd letter mix were simply the song's letters.
