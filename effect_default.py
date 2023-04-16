from typing import Any
import math
import colorsys


def frame_max() -> int:
    return 72


def frame_time(frame: int) -> float:
    return 1/30


def run(positions: list[dict], frame: int, storage: Any) -> (list[dict], Any):
    rgb = []
    # calculate rgb for each light
    for i, led in enumerate(positions):
        # get distance from origin to led
        distance_percent = math.sqrt(math.pow(led['x'], 2) + math.pow(led['y'], 2) + math.pow(led['z'], 2))
        # scale down to preference
        distance_percent /= 3.3
        # add some offset based on current frame
        # hsv_to_hue expects normalized values so mod 1
        hue = (distance_percent + frame / frame_max()) % 1
        r, g, b = colorsys.hsv_to_rgb(hue, 1, 0.8)
        rgb.append({'r': r, 'g': g, 'b': b})
    return rgb, storage
