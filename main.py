#!/usr/bin/env python3
"""Entrypoint for the 24 November 2026 news-image entry.

Validates an image file (a whole PNG or JPEG file, at most 1 MiB and at
most 1024x1024 pixels) and copies its exact bytes to /output/entry.png.

Usage: main.py [input-image]
The input image defaults to entry.png next to this script when no
argument is given.

Standard library only. Exit 0 on success, exit 1 on any invalid input.
"""
import os
import struct
import sys

MAX_BYTES = 1048576
MAX_DIM = 1024

PNG_SIG = b"\x89PNG\r\n\x1a\n"
JPEG_SOI = b"\xff\xd8"


def png_dims(data):
    """Return (width, height) from a PNG, or None if not a valid PNG."""
    if len(data) < 33 or not data.startswith(PNG_SIG):
        return None
    # First chunk must be IHDR: length 13, type "IHDR", then width/height.
    length = struct.unpack(">I", data[8:12])[0]
    if length != 13 or data[12:16] != b"IHDR":
        return None
    width, height = struct.unpack(">II", data[16:24])
    return width, height


def jpeg_dims(data):
    """Return (width, height) from a JPEG SOF0/SOF2 frame, else None."""
    if len(data) < 4 or not data.startswith(JPEG_SOI):
        return None
    pos = 2
    while pos + 4 <= len(data):
        if data[pos] != 0xFF:
            return None
        marker = data[pos + 1]
        if marker == 0xD8:  # SOI (again)
            pos += 2
            continue
        if marker in (0xD9, 0xDA):  # EOI / SOS: no frame header after this
            return None
        if pos + 4 > len(data):
            return None
        seg_len = struct.unpack(">H", data[pos + 2:pos + 4])[0]
        if seg_len < 2 or pos + 2 + seg_len > len(data):
            return None
        if marker in (0xC0, 0xC1, 0xC2):  # SOF0, SOF1, SOF2
            if seg_len < 7:
                return None
            height, width = struct.unpack(">HH", data[pos + 5:pos + 9])
            return width, height
        pos += 2 + seg_len
    return None


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    if len(argv) > 1:
        print("usage: main.py [input-image]", file=sys.stderr)
        return 1
    here = os.path.dirname(os.path.abspath(__file__))
    if argv:
        src = argv[0]
    else:
        src = os.path.join(here, "entry.png")
    try:
        with open(src, "rb") as fh:
            data = fh.read()
    except OSError as exc:
        print(f"error: cannot read {src}: {exc}", file=sys.stderr)
        return 1

    if len(data) > MAX_BYTES:
        print(f"error: file is {len(data)} bytes, over the "
              f"{MAX_BYTES} byte limit", file=sys.stderr)
        return 1

    dims = png_dims(data)
    kind = "PNG"
    if dims is None:
        dims = jpeg_dims(data)
        kind = "JPEG"
    if dims is None:
        print(f"error: {src} is neither a valid PNG nor a valid JPEG",
              file=sys.stderr)
        return 1

    width, height = dims
    if width <= 0 or height <= 0:
        print(f"error: invalid dimensions {width}x{height}",
              file=sys.stderr)
        return 1
    if width > MAX_DIM or height > MAX_DIM:
        print(f"error: dimensions {width}x{height} exceed "
              f"{MAX_DIM}x{MAX_DIM}", file=sys.stderr)
        return 1

    out_dir = "/output"
    try:
        os.makedirs(out_dir, exist_ok=True)
        with open(os.path.join(out_dir, "entry.png"), "wb") as fh:
            fh.write(data)
    except OSError as exc:
        print(f"error: cannot write output: {exc}", file=sys.stderr)
        return 1

    print(f"ok: {kind} {width}x{height}, {len(data)} bytes -> "
          f"/output/entry.png")
    return 0


if __name__ == "__main__":
    sys.exit(main())
