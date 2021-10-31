#!/usr/bin/env python3

from pathlib import Path

import numpy as np

encoded_image_data: list[int] = []
with open(Path("data", "08", "input.txt"), "r") as file:
    for line in file:
        encoded_image_data += [int(x) for x in line.strip()]


# ---- Part 1 ----


def convert_digital_sending_network_to_layered_image(
    dsn_values: list[int], height: int, width: int
) -> np.ndarray:
    img = np.array(dsn_values, dtype=np.int32).reshape((-1, height, width))
    return img


# Test image to confirm getting right shape of image.
test_input = [int(x) for x in "123456789012"]
test_img = convert_digital_sending_network_to_layered_image(test_input, 2, 3)

IMAGE_HEIGHT = 6
IMAGE_WIDTH = 25

img = convert_digital_sending_network_to_layered_image(
    encoded_image_data, height=IMAGE_HEIGHT, width=IMAGE_WIDTH
)
print(img.shape)
num_zeros = np.sum(img == 0, axis=(1, 2))
idx = np.where(num_zeros == np.min(num_zeros))[0][0]
num_ones = np.sum(img[idx] == 1)
num_twos = np.sum(img[idx] == 2)
ans = num_ones * num_twos
print(f"(part 1) layer {idx} -> {num_ones} x {num_twos} = {ans}")
assert ans == 1206


# ---- Part 2 ----


class NoVisibilePixelFound(BaseException):
    ...


def first_visible_value(ary: np.ndarray) -> int:
    for x in ary.flatten():
        if x != 2:
            return x
    raise NoVisibilePixelFound(ary)


def decode_image(img: np.ndarray, height: int, width: int) -> np.ndarray:
    compressed_img = np.zeros((height, width))

    for i in range(height):
        for j in range(width):
            compressed_img[i, j] = first_visible_value(img[:, i, j].flatten())

    assert np.sum(compressed_img == 2) == 0
    final_img = np.full(compressed_img.shape, fill_value="◻︎")
    final_img[compressed_img == 0] = "◼︎"
    return final_img


def develop_image(img: np.ndarray) -> str:
    assert img.ndim == 2
    dev_img = ""
    for row in img:
        dev_img += "".join(row) + "\n"
    return dev_img


decoded_img = decode_image(img, height=IMAGE_HEIGHT, width=IMAGE_WIDTH)
print(develop_image(decoded_img))  # "EJRGP"
