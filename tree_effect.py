import math
import colorsys


def effect(storage, positions, frame):
    # return 2d array of RGB values (normalized) for each LED
    # [ [r, g, b], [r, g, b] ]
    # you can write custom data to storage, it will be returned to you next frame
    rgb = []
    for i, led in enumerate(positions):
        distance_to_0 = math.sqrt(math.pow(led['x'], 2)+math.pow(led['y'], 2)+math.pow(led['z'], 2))
        distance_max = math.sqrt(11)
        hue = ((distance_to_0 / distance_max) * 360 + frame * 5) / 360
        rgb.append(list(colorsys.hsv_to_rgb(hue, 1, 0.8)))
    return storage, rgb


def frame_max():
    # return the number of frames to render
    return 100
