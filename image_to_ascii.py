"""Convert an image to ASCII art, print it, and save it as an image.

Usage:
    python image_to_ascii.py input.jpg
    python image_to_ascii.py input.jpg -o ascii.png --width 120
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError as exc:
    raise SystemExit(
        "Pillow is required. Install it with: python -m pip install pillow"
    ) from exc


ASCII_RAMP = "@%#*+=-:. "


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Convert an image to ASCII art, print it, and save it as PNG."
    )
    parser.add_argument("image", type=Path, help="Path to the input image.")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=Path("ascii_art.png"),
        help="Output image path. Default: ascii_art.png",
    )
    parser.add_argument(
        "-w",
        "--width",
        type=int,
        default=120,
        help="ASCII output width in characters. Default: 120",
    )
    parser.add_argument(
        "--invert",
        action="store_true",
        help="Invert brightness mapping for dark terminal backgrounds.",
    )
    parser.add_argument(
        "--font-size",
        type=int,
        default=12,
        help="Font size used for the saved image. Default: 12",
    )
    return parser.parse_args()


def load_monospace_font(font_size: int) -> ImageFont.ImageFont:
    candidates = [
        "C:/Windows/Fonts/consola.ttf",
        "C:/Windows/Fonts/cour.ttf",
        "C:/Windows/Fonts/lucon.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
        "/System/Library/Fonts/Menlo.ttc",
    ]

    for candidate in candidates:
        if Path(candidate).exists():
            return ImageFont.truetype(candidate, font_size)

    return ImageFont.load_default()


def image_to_ascii(image_path: Path, width: int, invert: bool = False) -> str:
    if width <= 0:
        raise ValueError("width must be greater than 0")

    with Image.open(image_path) as image:
        gray_image = image.convert("L")
        source_width, source_height = gray_image.size

        # Characters are taller than they are wide, so reduce height for balance.
        aspect_ratio = source_height / source_width
        target_height = max(1, int(width * aspect_ratio * 0.5))
        resized = gray_image.resize((width, target_height))

        ramp = ASCII_RAMP[::-1] if invert else ASCII_RAMP
        pixels = list(resized.getdata())
        chars = [ramp[pixel * (len(ramp) - 1) // 255] for pixel in pixels]

    lines = [
        "".join(chars[row_start : row_start + width])
        for row_start in range(0, len(chars), width)
    ]
    return "\n".join(lines)


def save_ascii_image(ascii_art: str, output_path: Path, font_size: int) -> None:
    lines = ascii_art.splitlines() or [""]
    font = load_monospace_font(font_size)

    left, top, right, bottom = font.getbbox("M")
    char_width = right - left
    char_height = bottom - top
    padding = max(8, font_size)

    image_width = max(1, max(len(line) for line in lines) * char_width + padding * 2)
    image_height = max(1, len(lines) * char_height + padding * 2)

    output_image = Image.new("RGB", (image_width, image_height), "white")
    draw = ImageDraw.Draw(output_image)

    y = padding
    for line in lines:
        draw.text((padding, y), line, fill="black", font=font)
        y += char_height

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_image.save(output_path)


def main() -> int:
    args = parse_args()

    if not args.image.exists():
        print(f"Input image not found: {args.image}", file=sys.stderr)
        return 1

    try:
        ascii_art = image_to_ascii(args.image, args.width, args.invert)
        print(ascii_art)
        save_ascii_image(ascii_art, args.output, args.font_size)
    except Exception as exc:
        print(f"Failed to convert image: {exc}", file=sys.stderr)
        return 1

    print(f"\nSaved ASCII image to: {args.output.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
