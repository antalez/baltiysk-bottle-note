"""Download the lyrics of the "Einheitslied" (Freundschaftskantate der Jugend; words Herbert Keller,
music André Asriel) from lieder-aus-der-ddr.de and save them to data/song.txt.

The lyrics are not redistributed in this repository (copyright); this script fetches them from the public page.
"""
import html, json, re, sys, urllib.request
from pathlib import Path

URL = "https://lieder-aus-der-ddr.de/wp-json/wp/v2/posts?slug=einheitslied"
OUT = Path(__file__).resolve().parent.parent / "data" / "song.txt"


def fetch() -> str:
    req = urllib.request.Request(URL, headers={"User-Agent": "baltiysk-bottle-note/1.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        post = json.load(r)[0]
    raw = post["content"]["rendered"]
    raw = re.sub(r"\[/?et_pb[^\]]*\]", "\n", raw)          # page-builder shortcodes
    raw = re.sub(r"<br\s*/?>", "\n", raw)
    raw = re.sub(r"</p>", "\n\n", raw)
    raw = re.sub(r"<[^>]+>", "", raw)
    text = html.unescape(raw)
    lines = [l.strip() for l in text.splitlines()
             if "adsbygoogle" not in l and not re.fullmatch(r"\d+\.\s*Strophe:?", l.strip())]
    text = "\n".join(lines)
    text = re.sub(r"\n{3,}", "\n\n", text).strip()
    # keep only the three stanzas (they start with Freundschaft!, Einheit!, Frieden!)
    start = text.find("Freundschaft!")
    return text[start:] if start >= 0 else text


if __name__ == "__main__":
    song = fetch()
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(song + "\n", encoding="utf-8")
    print(f"saved {len(song)} characters to {OUT}")
