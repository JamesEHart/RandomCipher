# ---------- ENCODE TEXT -----------
# python .\combined.py encode "[text to be encoded]" [0-16]
# ---------- DECODE IMAGE ----------
# python .\combined.py decode encoded_image.png [--key 0-15]

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import random
from PIL import Image
import argparse
import math
import datetime

METHOD_COLORS = [
    (1, 0, 0),
    (0, 1, 0),
    (0, 0, 1),
    (1, 1, 0),
    (1, 0, 1),
    (0, 1, 1),
    (0.5, 0, 0),
    (0, 0.5, 0),
    (0, 0, 0.5),
    (0.5, 0.5, 0),
    (0.5, 0, 0.5),
    (0, 0.5, 0.5),
    (0.25, 0.25, 0.25),
    (0.75, 0.75, 0.75),
    (1, 0.5, 0),
    (0, 0.5, 1),
]

METHOD_NAMES = [
    "Grayscale",
    "Red Gradient",
    "Green Gradient",
    "Blue Gradient",
    "RGB Bits Encoding",
    "Inverse Grayscale",
    "Grayscale",
    "Red Gradient",
    "Green Gradient",
    "Blue Gradient",
    "RGB Bits Encoding",
    "Inverse Grayscale",
    "Grayscale",
    "Red Gradient",
    "Green Gradient",
    "Blue Gradient",
]

cellSize = 100

def encode_method_0(c): val = ord(c) / 255; return (val, val, val)
def encode_method_1(c): val = ord(c) / 255; return (val, 0, 0)
def encode_method_2(c): val = ord(c) / 255; return (0, val, 0)
def encode_method_3(c): val = ord(c) / 255; return (0, 0, val)
def encode_method_4(c):
    code = ord(c)
    r = (code & 0xE0) >> 5
    g = (code & 0x1C) >> 2
    b = (code & 0x03)
    return (r / 7, g / 7, b / 3)
def encode_method_5(c): val = 1 - (ord(c) / 255); return (val, val, val)

ENCODING_METHODS = [
    encode_method_0,
    encode_method_1,
    encode_method_2,
    encode_method_3,
    encode_method_4,
    encode_method_5,
] * 3

def encode_string_with_method(s, method_idx):
    encode_fn = ENCODING_METHODS[method_idx]
    return [encode_fn(c) for c in s]

def plot_color_grid_with_method(rgb_list, method_idx, cols=8, border_color='black', border_width=1):
    rgb_list = [METHOD_COLORS[method_idx]] + rgb_list
    total = len(rgb_list)
    rows = (total + cols - 1) // cols

    fig, ax = plt.subplots(figsize=(cols, rows))
    ax.set_xlim(0, cols)
    ax.set_ylim(0, rows)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_aspect('equal')

    for idx, color in enumerate(rgb_list):
        row = rows - 1 - (idx // cols)
        col = idx % cols
        square = patches.Rectangle((col, row), 1, 1, facecolor=color,
                                   edgecolor=border_color, linewidth=border_width)
        ax.add_patch(square)

    plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
    return fig

def closest_method_color(rgb):
    def dist(c1, c2):
        return math.sqrt(sum((a - b) ** 2 for a, b in zip(c1, c2)))
    distances = [dist(rgb, color) for color in METHOD_COLORS]
    return distances.index(min(distances))

def decode_method_0(rgb): return chr(round(rgb[0] * 255))
def decode_method_1(rgb): return chr(round(rgb[0] * 255))
def decode_method_2(rgb): return chr(round(rgb[1] * 255))
def decode_method_3(rgb): return chr(round(rgb[2] * 255))
def decode_method_4(rgb):
    r = (round(rgb[0] * 255) >> 5) & 0x07
    g = (round(rgb[1] * 255) >> 5) & 0x07
    b = (round(rgb[2] * 255) >> 6) & 0x03
    code = (r << 5) + (g << 2) + b
    return chr(code)
def decode_method_5(rgb): return chr(255 - round(rgb[0] * 255))

DECODING_METHODS = [
    decode_method_0,
    decode_method_1,
    decode_method_2,
    decode_method_3,
    decode_method_4,
    decode_method_5,
] * 3

def decode_image_from_tiles(image_path, cell_size=cellSize, border=1, method_override=None):
    img = Image.open(image_path).convert("RGB")
    width, height = img.size

    cols = width // cell_size
    rows = height // cell_size

    cx = cell_size // 2
    cy = cell_size // 2

    if method_override is not None:
        method_idx = method_override
        print(f"Using manually provided encoding method: {method_idx} - {METHOD_NAMES[method_idx]}")
    else:
        method_rgb_int = img.getpixel((cx, cy))
        method_rgb = tuple(channel / 255 for channel in method_rgb_int)
        method_idx = closest_method_color(method_rgb)
        print(f"Detected encoding method: {method_idx} - {METHOD_NAMES[method_idx]}")
        print(f"Method color (normalized): {method_rgb}")

    decode_fn = DECODING_METHODS[method_idx]
    decoded_chars = []

    first_tile_skipped = False
    for y in range(rows):
        for x in range(cols):
            if not first_tile_skipped:
                first_tile_skipped = True
                continue

            px = x * cell_size + cell_size // 2
            py = y * cell_size + cell_size // 2

            if px >= width or py >= height:
                continue

            rgb = img.getpixel((px, py))
            if rgb == (255, 255, 255):
                continue

            norm_rgb = tuple(channel / 255 for channel in rgb)

            try:
                decoded_chars.append(decode_fn(norm_rgb))
            except Exception:
                decoded_chars.append('�')

    return ''.join(decoded_chars)

def main():
    parser = argparse.ArgumentParser(description="Encode or decode color-encoded strings.")
    subparsers = parser.add_subparsers(dest='command', required=True)

    encode_parser = subparsers.add_parser('encode', help='Encode string to color grid and save image')
    encode_parser.add_argument('string', help='Input string to encode')
    encode_parser.add_argument('method', type=int, help='Encoding method index (0-15), or 16 for random')

    decode_parser = subparsers.add_parser('decode', help='Decode message from encoded image')
    decode_parser.add_argument('image', help='Path to encoded tile image')
    decode_parser.add_argument('--cell', type=int, default=cellSize, help='Tile cell size including border')
    decode_parser.add_argument('--key', type=int, choices=range(0, 16), help='Optional method index override (0-15)')

    args = parser.parse_args()

    if args.command == 'encode':
        method_index = args.method
        if method_index == 16:
            method_index = random.randrange(16)
        encoded_colors = encode_string_with_method(args.string, method_index)
        fig = plot_color_grid_with_method(encoded_colors, method_index)

        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"encoded_image.png"
        fig.savefig(filename)
        print(f"Saved encoded image as: {filename}")
        plt.close(fig)

    elif args.command == 'decode':
        message = decode_image_from_tiles(args.image, cell_size=args.cell, method_override=args.key)
        print("\nDecoded message:\n", message)

if __name__ == "__main__":
    main()
