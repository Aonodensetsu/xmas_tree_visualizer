from typing import Any
from math import sqrt
import colorsys


def frame_max() -> int:
    return 72


def frame_time(frame: int) -> float:
    return 1/30


def run(positions: list[dict], frame: int, storage: Any) -> (list[dict], Any):
    rgb = []
    for led in positions:
        # get distance from origin to led
        distance_percent = sqrt(led['x']**2 + led['y']**2 + led['z']**2)
        # scale down to preference
        distance_percent /= 3.3
        # add some offset based on current frame
        hue = (distance_percent + frame / frame_max())
        # hsv_to_hue expects normalized values so mod 1 (only keep the decimals)
        r, g, b = colorsys.hsv_to_rgb(hue % 1, 1, 0.8)
        rgb.append({'r': r, 'g': g, 'b': b})
    return rgb, storage
