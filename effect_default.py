from typing import Any
import math
import colorsys

length = 72


def run(storage: Any, positions: list[dict], frame: int) -> (Any, list[dict]):
    rgb = []
    # calculate rgb for each light
    for i, led in enumerate(positions):
        # get distance from origin to led
        distance_percent = math.sqrt(math.pow(led['x'], 2) + math.pow(led['y'], 2) + math.pow(led['z'], 2))
        # scale down to preference
        distance_percent /= 3.3
        # add some offset based on current frame
        # hsv_to_hue expects normalized values so mod 1
        hue = (distance_percent + frame / length) % 1
        r, g, b = colorsys.hsv_to_rgb(hue, 1, 0.8)
        rgb.append({'r': r, 'g': g, 'b': b})
    return storage, rgb


def frame_max() -> int:
    # var length is used in hue calculation, so the animation loops
    return length


def frame_rate() -> int:
    return 30
