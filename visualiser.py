import os
import tkinter
import matplotlib
from x_zipper import Coordinates, PY, CSV, XTREE

matplotlib.use('TkAgg', force=True)
import matplotlib.pyplot as plot

# fix running by left click
os.chdir(os.path.dirname(os.path.realpath(__file__)))


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
    graph.set(xlim3d=(-1, 1), ylim3d=(-1, 1), zlim3d=(0, max(p['z'] for p in leds)))
    graph.set(xticks=[-1, 1], yticks=[-1, 1], zticks=[0, max(p['z'] for p in leds)])
    graph.margins(x=0, y=0, z=0, tight=True)
    graph.tick_params(which='both', color='None', labelcolor='white')
    graph.tick_params(axis='both', pad=5)
    graph.tick_params(axis='z', pad=15)
    # plot the initial points
    graph.plot([p['x'] for p in leds], [p['y'] for p in leds], [p['z'] for p in leds], color=(0, 0, 0, 0.08))
    graph.set_box_aspect([ub - lb for lb, ub in (getattr(graph, f'get_{a}lim')() for a in 'xyz')])
    plot.tight_layout()
    return graph


def draw(gui, leds, frame):
    # do not draw if the window was closed
    if not plot.fignum_exists(1):
        return
    # remove previously drawn points
    for dot in plot.gca().collections:
        dot.remove()
    # draw new points
    gui.scatter3D(
        [p['x'] for p in leds],
        [p['y'] for p in leds],
        [p['z'] for p in leds],
        c=[(led['r'], led['g'], led['b']) for led in frame['c']]
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
        # generate a fake tree if the real one not found
        xyz.make()
    xtree = XTREE()
    try:
        xtree.read()
        state += 1 << 2
    except EnvironmentError:
        pass
    csv = CSV()
    try:
        csv.read()
        state += 1 << 1
    except EnvironmentError:
        pass
    py = PY(coordinates=xyz)
    try:
        py.read()
        state += 1 << 0
    except EnvironmentError:
        pass
    # create other file formats
    # XTREE -> CSV (if CSV not present)
    if state & (1 << 2) and not state & (1 << 1):
        xtree.convert(CSV).write()
    # CSV -> XTREE (if XTREE not present)
    elif state & (1 << 1) and not state & (1 << 2):
        xtree = csv.convert(XTREE).write()
    # PY -> XTREE, CSV (if both not present)
    elif state == 9:
        py.convert(CSV).write()
        xtree = py.convert(XTREE).write()
    match state:
        # 0   ()             fake tree, black LEDs
        # 2   (csv)          ->  0
        # 4   (xtree)        ->  0
        # 6   (csv, xtree)   ->  0
        # 8   (coordinates)  real tree, black LEDs
        case 0 | 2 | 4 | 6 | 8:
            use = py
            # black LEDs
            py.data = [{'t': 1 / 30, 'c': [{'r': 0, 'g': 0, 'b': 0} for _ in xyz.data]}]
        # py file present
        # 1   ()            fake tree, preview PY
        # 3   (csv)         ->  1
        # 5   (xtree)       ->  1
        # 7   (csv, xtree)  ->  1
        case 1 | 3 | 5 | 7:
            use = py
        # coordinate file present
        # 9   (py)              -> 15
        # 10  (csv)             -> 15
        # 11  (py, csv)         -> 15
        # 12  (xtree)           -> 15
        # 13  (py, xtree)       -> 15
        # 14  (csv, xtree)      -> 15
        # 15  (py, csv, xtree)  real tree, preview XTREE
        case _:
            use = xtree
    frame = 1
    graph = gui(xyz.data)
    while plot.fignum_exists(1):
        if not frame < len(use.data):
            frame = 1
        draw(graph, xyz.data, use.data[frame-1])
        frame += 1


if __name__ == '__main__':
    main()
