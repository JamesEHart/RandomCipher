import matplotlib.pyplot as plt
import matplotlib.patches as patches
import random

METHOD_COLORS = [
    (1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 1, 0),
    (1, 0, 1), (0, 1, 1), (0.5, 0, 0), (0, 0.5, 0),
    (0, 0, 0.5), (0.5, 0.5, 0), (0.5, 0, 0.5), (0, 0.5, 0.5),
    (0.25, 0.25, 0.25), (0.75, 0.75, 0.75), (1, 0.5, 0), (0, 0.5, 1)
]

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
    plt.show()

input_string = input()
method_index = int(input())
if method_index == 16:
    method_index = random.randrange(16)

encoded_colors = encode_string_with_method(input_string, method_index)
plot_color_grid_with_method(encoded_colors, method_index)
