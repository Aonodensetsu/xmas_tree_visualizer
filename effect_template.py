def effect(storage, positions, frame):
    #
    # storage - you can write custom data into it, will be returned to you next frame
    #
    # positions - are given to you as a list of dictionaries for each LED
    # [ {x, y, z}, {x, y, z}, ... ]
    # get an led as positions[led number]
    # and then coordinates as led['x'], led['y'] or led['z']
    #
    # frame - gives you the current frame number (starts at 1, ends at frame_max())
    #
    # return 2d array of normalized RGB values for each LED
    # [ [r, g, b], [0.2, 0.7, 1], ... ]
    #
    rgb = [[0, 0, 0] for _ in range(len(positions))]
    return storage, rgb


def frame_max():
    # return the number of frames to render
    return 1


def frame_rate():
    # return the number of frames per second
    # this is not accurate, as plotting also takes some time
    return 30
