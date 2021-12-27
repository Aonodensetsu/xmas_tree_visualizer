import math
import colorsys

length = 72


def effect(storage, positions, frame):
    rgb = []
    # calculate rgb for each light
    for i, led in enumerate(positions):
        # get distance from origin to led
        distance_percent = (math.sqrt(math.pow(led['x'], 2)+math.pow(led['y'], 2)+math.pow(led['z'], 2)))/math.sqrt(11)
        # add some offset based on current frame
        # hsv_to_hue expects normalized values so mod 1
        hue = (distance_percent + frame / length) % 1
        rgb.append(list(colorsys.hsv_to_rgb(hue, 1, 0.8)))
    return storage, rgb


def frame_max():
    # length of the animation
    # var length is used in hue calculation so it loops
    return length
