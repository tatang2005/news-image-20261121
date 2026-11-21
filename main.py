#!/usr/bin/env python3
"""Entry point for the news-image-20261121 submission.

The artwork itself is produced ahead of time by draw.py and stored in
this repository as entry.png.  This program's only job is to deliver
that file: it copies the entry.png sitting next to it into the output
directory named by the MAKEFUN_OUTPUT_DIR environment variable
(falling back to /output).

It deliberately does no drawing and writes nothing into the repository
directory, so it works even when the repository is mounted read-only.
Only the Python standard library is used.
"""

import os
import shutil
import sys

IMAGE_NAME = "entry.png"
DEFAULT_OUTPUT_DIR = "/output"


def deliver():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, IMAGE_NAME)
    if not os.path.isfile(source):
        print("missing artwork file: %s" % source, file=sys.stderr)
        return 1

    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", DEFAULT_OUTPUT_DIR)
    os.makedirs(output_dir, exist_ok=True)
    target = os.path.join(output_dir, IMAGE_NAME)
    shutil.copyfile(source, target)
    print("copied %s -> %s" % (source, target))
    return 0


if __name__ == "__main__":
    sys.exit(deliver())
