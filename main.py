#!/usr/bin/env python3
"""Ship the finished front page for make.fun news-image-20261124.

The judged artifact is entry.png, which already lives in this repository.
This script does not draw anything: it only checks the file is a real PNG
under the bounty's 1 MiB cap and copies it, byte for byte, to the grading
location. No network is touched, and every run writes identical bytes.

Usage:
    python3 main.py
    MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import os
import shutil
import sys

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
# The bounty caps the delivered image at 1 MiB; anything bigger is rejected
# before any copy happens.
IMAGE_LIMIT = 1024 * 1024


def fail(message):
    print(f"error: {message}", file=sys.stderr)
    return 1


def run():
    repo_root = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(repo_root, "entry.png")
    target_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    target = os.path.join(target_dir, "entry.png")

    with open(source, "rb") as handle:
        signature = handle.read(len(PNG_SIGNATURE))
    if signature != PNG_SIGNATURE:
        return fail("entry.png is not a PNG file")

    size = os.path.getsize(source)
    if size > IMAGE_LIMIT:
        return fail(f"entry.png is {size} bytes, over the 1 MiB cap")

    os.makedirs(target_dir, exist_ok=True)
    shutil.copyfile(source, target)
    print(f"wrote {target} - {size} bytes")
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
