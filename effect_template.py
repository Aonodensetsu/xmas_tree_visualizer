def effect(storage, positions, frame):
    """
    storage - you can set it to whatever you want, will be returned to you next frame

    positions - are given to you as a list of dictionaries for each LED
    [ {x, y, z}, {x, y, z}, ... ]
    the length of the list is the number of LEDs in the tree

    frame - gives you the current frame number (starts at 1, ends at frame_max())

    return 2d list of normalized RGB values for each LED
    [ [r, g, b], [0.2, 0.7, 1], ... ]
    """
    rgb = [[0, 0, 0] for _ in range(len(positions))]
    return storage, rgb


def frame_max():
    """set the number of frames to render"""
    return 1


def frame_rate():
    """
    set the number of frames per second
    this is not accurate, as plotting also takes some time
    only takes effect in this visualizer and those compatible with GSD6338/XmasTree/#4
    """
    return 30
