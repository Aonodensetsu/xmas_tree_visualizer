from x_zipper import Coordinates, PY, CSV, XTREE
from contextlib import suppress
import matplotlib
import tkinter
import os

matplotlib.use('TkAgg', force=True)
import matplotlib.pyplot as plot


def _plot(window, leds):
    # create a plot
    graph = window.add_subplot(111, projection='3d')
    graph.view_init(elev=15, azim=5)
    window.patch.set_facecolor('#4c4a48')
    graph.set(fc='#4c4a48')
    graph.xaxis.pane.set_alpha(0)
    graph.yaxis.pane.set_alpha(0)
    graph.zaxis.pane.set_alpha(0)
    graph.set_xlabel('X', color='white', labelpad=-5)
    graph.set_ylabel('Y', color='white', labelpad=-5)
    graph.set_zlabel('Z', color='white', labelpad=5)
    min_x = min_y = min_z = max_x = max_y = max_z = None
    for led in leds:
        x, y, z = led['x'], led['y'], led['z']
        if min_x is None or x < min_x: min_x = x
        if min_y is None or y < min_y: min_y = y
        if min_z is None or z < min_z: min_z = z
        if max_x is None or x > max_x: max_x = x
        if max_y is None or y > max_y: max_y = y
        if max_z is None or z > max_z: max_z = z
    graph.set(xlim3d=(min_x, max_x), ylim3d=(min_y, max_y), zlim3d=(min_z, max_z))
    graph.set(xticks=[min_x, max_x], yticks=[min_y, max_y], zticks=[min_z, max_z])
    graph.margins(x=0, y=0, z=0, tight=True)
    graph.tick_params(which='both', color='None', labelcolor='white')
    graph.tick_params(axis='both', pad=5)
    graph.tick_params(axis='z', pad=15)
    return graph


def gui(leds):
    # gather screen information
    screen_measurer = tkinter.Tk()
    dpi = screen_measurer.winfo_fpixels('1i')
    screen_height = screen_measurer.winfo_screenheight()
    # calculate a reasonable window size
    top = int(0.05 * screen_height)
    left = 200
    height = int(0.75 * screen_height)
    width = int(0.75 * height)
    screen_measurer.update()
    screen_measurer.destroy()
    # set window parameters
    matplotlib.rcParams['toolbar'] = 'None'
    matplotlib.rc('grid', color='None')
    window = plot.figure(num='Christmas Tree Visualiser')
    window.canvas.manager.window.wm_geometry(f'+{left}+{top}')
    window.set_size_inches(width / dpi, height / dpi)
    window.canvas.mpl_connect('close_event', lambda e: plot.close(window))
    graph = _plot(window, leds)
    # plot the initial points
    graph.plot([p['x'] for p in leds], [p['y'] for p in leds], [p['z'] for p in leds], color=(0, 0, 0, 0.08))
    graph.set_box_aspect([ub - lb for lb, ub in (getattr(graph, f'get_{a}lim')() for a in 'xyz')])
    plot.tight_layout()
    return graph


def draw(gui, leds, frame):
    # do not draw if the window was closed
    if not plot.fignum_exists(1): return
    # remove previously drawn points
    for dot in plot.gca().collections: dot.remove()
    # draw new points
    gui.scatter3D(
        [p['x'] for p in leds],
        [p['y'] for p in leds],
        [p['z'] for p in leds],
        c=[(color['r'], color['g'], color['b']) for color in frame['c']]
    )
    plot.draw()
    plot.pause(frame['t'])


def main():
    state = 0
    # calculate program state -> found extension files
    # exception on read if file not found
    xyz = Coordinates()
    try:
        xyz.read()
        state += 1 << 3
    except EnvironmentError:
        xyz.make()  # generate a fake tree if the real one not found
    xtree = XTREE()
    with suppress(EnvironmentError):
        xtree.read()
        state += 1 << 2
    csv = CSV()
    with suppress(EnvironmentError):
        csv.read()
        state += 1 << 1
    py = PY(coordinates=xyz)
    # only compile python if going to preview it
    match state:
        case 0 | 2 | 4 | 6 | 8:
            with suppress(EnvironmentError):
                py.read()
                state += 1 << 0
    # create other file formats
    # XTREE -> CSV (if CSV not present)
    if state & (1 << 2) and not state & (1 << 1):
        xtree.convert(CSV).write()
        csv.read()
        state += 1 << 1
    # CSV -> XTREE (if XTREE not present)
    elif state & (1 << 1) and not state & (1 << 2):
        xtree = csv.convert(XTREE).write()
        state += 1 << 2
    # PY -> XTREE, CSV (if both not present)
    elif state == 9:
        xtree = py.convert(XTREE).write()
        xtree.convert(CSV).write()
    match state:
        # the conversions merge states 2 and 4 into 6
        # 0   ()             fake tree, black LEDs
        # 6   (csv, xtree)   ->  0
        # 8   (coordinates)  real tree, black LEDs
        case 0 | 6 | 8:
            # write a frame of black LEDs
            py.data = [{'t': 1 / 30, 'c': [{'r': 0, 'g': 0, 'b': 0} for _ in xyz.data]}]
            use = py
        # py file present
        # the conversions merge states 3 and 5 into 7
        # 1   ()            fake tree, preview PY
        # 7   (csv, xtree)  ->  1
        case 1 | 7:
            use = py
        # coordinate file present
        # the conversions merge states 9, 10, 11, 12, 13 and 14 into 15
        # 15  (py, csv, xtree)  real tree, preview XTREE
        case _:
            use = xtree
    frame = 1
    graph = gui(xyz.data)
    while plot.fignum_exists(1):
        if frame >= len(use.data): frame = 1
        draw(graph, xyz.data, use.data[frame - 1])
        frame += 1


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.realpath(__file__)))  # fix running by left click
    main()
