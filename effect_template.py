def effect(storage, positions, frame):
    #
    # storage - you can write custom data into it, will be returned to you next frame
    #
    # positions - are given to you as a 2d array for each LED
    # [ [x, y, z], [x, y, z], ... ]
    #
    # frame - gives you the current frame number (starts at 1, ends at frame_max())
    #
    # return 2d array of normalized RGB values for each LED
    # [ [r, g, b], [0.2, 0.7, 1], ... ]
    #
    rgb = [[0, 0, 0] for i in range(len(positions))]
    return storage, rgb


def frame_max():
    # return the number of frames to render
    # the visualizer runs at roughly 30 frames per second
    return 1
