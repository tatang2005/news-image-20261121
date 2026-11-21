"""main.py -- entry program for the make.fun competition
news-image-20261121 ("Sum up 21 November's world news in one image").

Renders the front page drawn by draw.py and writes it as entry.png:
next to this file (for local inspection) and into the output
directory ($MAKEFUN_OUTPUT_DIR, default /output) when it can be
created. The render is deterministic -- running this program twice
produces byte-identical files.
"""

import os

import draw


def main():
    img = draw.render()
    here = os.path.dirname(os.path.abspath(__file__))
    local_path = os.path.join(here, "entry.png")
    img.save(local_path)
    print("wrote", local_path)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    try:
        os.makedirs(out_dir, exist_ok=True)
        out_path = os.path.join(out_dir, "entry.png")
        img.save(out_path)
        print("wrote", out_path)
    except OSError as exc:
        print("output dir unavailable:", exc)


if __name__ == "__main__":
    main()
