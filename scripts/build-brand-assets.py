#!/usr/bin/env python3
"""Renders GluonStack's brand assets from the SVG sources in assets/brand/svg.

    python scripts/build-brand-assets.py            write every asset
    python scripts/build-brand-assets.py --check    exit 1 if a committed asset differs from a fresh render

The sources and the size ladder are the design contract's (docs/design/SPEC.md, "Mark and icons"): 16 and 20 pixels
come from the 16 form (no nodes), 24 to 40 from the 32 form, 48 and up from the full mark. Each size is rendered from
the SVG at its own pixel size, never scaled from a larger raster.

Needs the packages in scripts/requirements-icons.txt. Developer tooling: never shipped by the installer.
"""
import io
import pathlib
import sys

import resvg_py
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent.parent
SVG = ROOT / "assets" / "brand" / "svg"
OUT = ROOT / "assets" / "brand"
APP_SIZES = [16, 20, 24, 32, 40, 48, 64, 128, 256]
PNG_SIZES = [16, 24, 32, 48, 64, 128, 256, 512]
TRAY_SIZES = [16, 20, 24, 32]
TRAY_STATES = ["running", "partial", "stopped", "fault"]


def ladder(size):
    return "gluonstack-mark-16.svg" if size <= 20 else "gluonstack-mark-32.svg" if size <= 40 else "gluonstack-mark.svg"


def render(name, width, height=None):
    data = resvg_py.svg_to_bytes(svg_string=(SVG / name).read_text(encoding="utf-8"), width=width,
                                 height=height or width)
    return Image.open(io.BytesIO(bytes(data))).convert("RGBA")


def ico(images):
    """One .ico holding each image as its own PNG-compressed entry (Pillow would otherwise downscale the largest)."""
    buffer = io.BytesIO()
    largest = max(images, key=lambda i: i.width)
    largest.save(buffer, format="ICO", sizes=[(i.width, i.height) for i in images],
                 append_images=[i for i in images if i is not largest])
    return buffer.getvalue()


def png(image):
    buffer = io.BytesIO()
    image.save(buffer, format="PNG", optimize=True)
    return buffer.getvalue()


def bmp(image):
    buffer = io.BytesIO()
    image.convert("RGB").save(buffer, format="BMP")
    return buffer.getvalue()


def assets():
    """Every generated file as {path: bytes}."""
    out = {}
    app = ico([render(ladder(s), s) for s in APP_SIZES])
    out[OUT / "gluonstack.ico"] = app
    for size in PNG_SIZES:
        out[OUT / "png" / f"gluonstack-{size}.png"] = png(render(ladder(size), size))
    for state in TRAY_STATES:
        out[OUT / "tray" / f"gluonstack-tray-{state}.ico"] = ico(
            [render(f"gluonstack-tray-{state}.svg", s) for s in TRAY_SIZES])
    # Inno Setup's wizard images, at 100% and 200% scale.
    for scale in (1, 2):
        suffix = "" if scale == 1 else "@2x"
        out[OUT / "installer" / f"wizard-banner{suffix}.bmp"] = bmp(
            render("gluonstack-installer-banner.svg", 164 * scale, 314 * scale))
        out[OUT / "installer" / f"wizard-small{suffix}.bmp"] = bmp(render("gluonstack-mark-solid.svg", 55 * scale))
    # The web dashboard is served from default/, so it holds its own copies. The control panel links the files in
    # assets/ from its project file and keeps none.
    out[ROOT / "default" / "favicon.ico"] = ico([render(ladder(s), s) for s in (16, 32, 48)])
    out[ROOT / "default" / "assets" / "gluonstack-mark.svg"] = (SVG / "gluonstack-mark.svg").read_bytes()
    for font in sorted((ROOT / "assets" / "fonts").iterdir()):
        out[ROOT / "default" / "assets" / "fonts" / font.name] = font.read_bytes()
    return out


def main(argv):
    check = "--check" in argv
    stale = []
    for path, data in assets().items():
        if check:
            if not path.is_file() or path.read_bytes() != data:
                stale.append(path.relative_to(ROOT).as_posix())
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        print("wrote", path.relative_to(ROOT).as_posix())
    if stale:
        print("stale (run python scripts/build-brand-assets.py):", *stale, sep="\n  ")
        return 1
    if check:
        print("brand assets are current")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
