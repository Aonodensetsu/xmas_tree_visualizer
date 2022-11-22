from typing import Any


def run(storage: Any, positions: list[dict], frame: int) -> (Any, list[dict]):
    """
    storage - you can set it to whatever you want, will be returned to you next frame
        (hence the type suggestion is Any)
    it's a way of storing data you might need to access across multiple frames, or caching partial results

    positions - are given to you as a list of dictionaries for each LED
    [ {x, y, z}, {x, y, z}, ... ]
    the length of the list is the number of LEDs in the tree, as one would expect

    frame - gives you the current frame number (starts at 1, ends at frame_max(), inclusive)

    return list of normalized RGB values - one dictionary per LED
    [ {r, g, b}, {'r': 0.2, 'g': 0.7, 'b': 1}, ... ]
    """
    rgb = [{'r': 0, 'g': 0, 'b': 0} for _ in positions]  # to make sure the template is a valid effect, will set all LEDs to black
    return storage, rgb


def frame_max() -> int:
    """
    Set the number of frames to render
    """
    return 1


def frame_rate() -> int:
    """
    Set the number of frames per second
    This is not accurate in the visualizer
        (and probably won't be on the actual tree either)
    !!! Only takes effect in this visualizer and those compatible with GSD6338/XmasTree/#4
    """
    return 30
