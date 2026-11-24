#!/usr/bin/env python3
"""Entry for make.fun bounty "news-image-20261124".

Copies the front-page image (entry.png, in this repository) to
/output/entry.png, byte for byte, using only the standard library.
No network is used. Every run writes identical bytes.

Run locally:
    python3 main.py
    # or, to write elsewhere:
    MAKEFUN_OUTPUT_DIR=out python3 main.py
"""
import os
import shutil
import sys

MAX_BYTES = 1 * 1024 * 1024  # 1 MiB, the bounty's image cap


def main() -> int:
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    dst = os.path.join(out_dir, "entry.png")

    with open(src, "rb") as f:
        magic = f.read(8)
    if magic != b"\x89PNG\r\n\x1a\n":
        print("error: entry.png is not a PNG file", file=sys.stderr)
        return 1
    size = os.path.getsize(src)
    if size > MAX_BYTES:
        print(f"error: entry.png is {size} bytes, over the 1 MiB cap",
              file=sys.stderr)
        return 1

    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(src, dst)
    print(f"wrote {dst} ({size} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
