from typing import Any


def frame_max() -> int:
    """
    Set the number of frames to generate
    """
    return 1


def frame_time(frame: int) -> float:
    """
    !!! Only takes effect in visualizers compatible with GSD6338/XmasTree/#4 (including this one)
    Set the frame time of this effect (1/frame rate)
        you can vary this number to make some frames last longer
    This may not be perfectly accurate in the visualizer
        (and probably won't be on the actual tree either)
    """
    return 1/30


def run(positions: list[dict], frame: int, storage: Any) -> (list[dict], Any):
    """
    positions - are given to you as a list of dictionaries for each LED
                [ {x, y, z}, {'x': 0.2, 'y': 1.3, 'z': 0.8}, ... ]
                the length of the list is the number of LEDs in the tree

    frame - gives you the current frame number
            starts at 1, ends at frame_max(), inclusive

    storage - you can set it to whatever you want, will be returned to you next frame
              it's a way of storing data you might need to access across multiple frames

    return a list of normalized RGB values
           [ {r, g, b}, {'r': 0.2, 'g': 0.7, 'b': 1}, ... ]
           one dictionary per LED - the same length as positions
    """
    rgb = [{'r': 0, 'g': 0, 'b': 0} for _ in positions]  # this template is a valid effect, will set all LEDs to black
    return rgb, storage
