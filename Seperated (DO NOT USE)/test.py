from PIL import Image
import argparse
import math

cellSize = int(100)

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

def closest_method_color(rgb):
    def dist(c1, c2):
        return math.sqrt(sum((a - b) ** 2 for a, b in zip(c1, c2)))
    distances = [dist(rgb, color) for color in METHOD_COLORS]
    return distances.index(min(distances))

def decode_method_0(rgb):
    val = round(rgb[0] * 255)
    return chr(val)

def decode_method_1(rgb):
    val = round(rgb[0] * 255)
    return chr(val)

def decode_method_2(rgb):
    val = round(rgb[1] * 255)
    return chr(val)

def decode_method_3(rgb):
    val = round(rgb[2] * 255)
    return chr(val)

def decode_method_4(rgb):
    r = (round(rgb[0] * 255) >> 5) & 0x07
    g = (round(rgb[1] * 255) >> 5) & 0x07
    b = (round(rgb[2] * 255) >> 6) & 0x03
    code = (r << 5) + (g << 2) + b
    return chr(code)

def decode_method_5(rgb):
    val = 255 - round(rgb[0] * 255)
    return chr(val)

DECODING_METHODS = [
    decode_method_0,
    decode_method_1,
    decode_method_2,
    decode_method_3,
    decode_method_4,
    decode_method_5,
] * 3

def decode_image_from_tiles(image_path, cell_size=cellSize, border=1):
    img = Image.open(image_path).convert("RGB")
    width, height = img.size

    cols = width // cell_size
    rows = height // cell_size

    cx = cell_size // 2
    cy = cell_size // 2
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

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Decode bordered tile RGB image.")
    parser.add_argument("image", help="Path to encoded tile image.")
    parser.add_argument("--cell", type=int, default=cellSize, help="Tile cell size including border.")
    args = parser.parse_args()

    message = decode_image_from_tiles(args.image, cell_size=args.cell)
    print("\nDecoded message:\n", message)
