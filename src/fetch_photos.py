"""Download the two public photographs of the note (as posted on Klaus Schmeh's blog in 2016) to data/photos/.

The photos are not redistributed in this repository; the dashboard shows them if this script has been run.
"""
import urllib.request
from pathlib import Path

BASE = "https://scienceblogs.de/klausis-krypto-kolumne/files/2016/09/"
PHOTOS = {"page1.png": "Kaliningrad-Cryptogram1.png", "page2.png": "Kaliningrad-Cryptogram-2.png"}
OUT = Path(__file__).resolve().parent.parent / "data" / "photos"

if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    for name, src in PHOTOS.items():
        req = urllib.request.Request(BASE + src, headers={"User-Agent": "Mozilla/5.0"})
        (OUT / name).write_bytes(urllib.request.urlopen(req, timeout=60).read())
        print("saved", OUT / name)
