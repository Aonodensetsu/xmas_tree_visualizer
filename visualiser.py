import os
import tkinter
import matplotlib
from x_zipper import Coordinates, PY, CSV, XTREE

matplotlib.use('TkAgg', force=True)
import matplotlib.pyplot as plot

os.chdir(os.path.dirname(os.path.realpath(__file__)))


def gui(positions):
    screen_measurer = tkinter.Tk()
    dpi = screen_measurer.winfo_fpixels('1i')
    screen_height = screen_measurer.winfo_screenheight()
    top = int(0.05 * screen_height)
    height = int(0.8 * screen_height)
    left = 100
    width = int(0.9 * height)
    screen_measurer.update()
    screen_measurer.destroy()
    matplotlib.rcParams['toolbar'] = 'None'
    matplotlib.rc('grid', color='None')
    window = plot.figure(num='Christmas Tree Visualiser')
    window.canvas.manager.window.wm_geometry(f'+{left}+{top}')
    window.set_size_inches(width / dpi, height / dpi)
    window.canvas.mpl_connect('close_event', lambda e: plot.close(window))
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
    graph.set(xlim3d=(-1, 1), ylim3d=(-1, 1), zlim3d=(0, max(p['z'] for p in positions)))
    graph.set(xticks=[-1, 1], yticks=[-1, 1], zticks=[0, max(p['z'] for p in positions)])
    graph.margins(x=0, y=0, z=0, tight=True)
    graph.tick_params(which='both', color='None', labelcolor='white')
    graph.tick_params(axis='both', pad=5)
    graph.tick_params(axis='z', pad=15)
    graph.plot([p['x'] for p in positions], [p['y'] for p in positions], [p['z'] for p in positions],
               color=(0, 0, 0, 0.08))
    graph.set_box_aspect([ub - lb for lb, ub in (getattr(graph, f'get_{a}lim')() for a in 'xyz')])
    plot.tight_layout()
    return graph


def draw(graph, positions, frame):
    if not plot.fignum_exists(1):
        return
    for dot in plot.gca().collections:
        dot.remove()
    graph.scatter3D(
        [p['x'] for p in positions],
        [p['y'] for p in positions],
        [p['z'] for p in positions],
        c=[(float(led['r'])/255, float(led['g'])/255, float(led['b'])/255) for led in frame['c']]
    )
    plot.draw()
    plot.pause(1/float(frame['t']))


if __name__ == '__main__':
    state = 0
    xyz = Coordinates().read()
    xtree = XTREE()
    csv = CSV()
    py = PY(xyz)
    state += 0 if xyz.generated else 1 << 3
    try:
        xtree.read()
        state += 1 << 2
    except EnvironmentError:
        pass
    try:
        csv.read()
        state += 1 << 1
    except EnvironmentError:
        pass
    try:
        py.read()
        state += 1 << 0
    except EnvironmentError:
        pass
    graph = gui(xyz.data)
    frame = 0
    match state:
        # 15 - (py, csv, xtree, coordinates) ignore PY and CSV -> 12
        # 14 - (csv, xtree, coordinates)     ignore CSV -> 12
        # 13 - (py, xtree, coordinates)      ignore PY -> 12
        # 12 - (xtree, coordinates)          play back the XTREE, generate CSV
        case 15 | 14 | 13 | 12:
            use = xtree
            xtree.convert(CSV).write()
        # 11 - (py, csv, coordinates loaded) ignore PY -> 10
        # 10 - (csv, coordinates loaded)     play back the CSV, generate XTREE
        case 11 | 10:
            use = csv
            csv.convert(XTREE).write()
        # 9 - (py, coordinates loaded) play the PY effect and generate static files
        case 9:
            use = py
            py.convert(CSV).write()
            py.convert(XTREE).write()
        # 8 - (coordinates loaded) show the tree with black LEDs
        # 6 - (csv, xtree loaded)  ignore CSV and XTREE -> 0
        # 4 - (xtree loaded)       ignore XTREE -> 0
        # 2 - (csv loaded)         ignore CSV -> 0
        # 0 - (nothing loaded)     show a placeholder tree with black LEDs
        case 8 | 6 | 4 | 2 | 0:
            use = py
            py.data = [{'t': 1/30, 'c': [{'r': 0, 'g': 0, 'b': 0} for _ in xyz.data]}]
        # 7 - (py, csv, xtree loaded) ignore CSV & XTREE -> 1
        # 5 - (py, xtree loaded)      ignore XTREE -> 1
        # 3 - (py, csv loaded)        ignore CSV -> 1
        # 1 - (py loaded)             show on a placeholder tree
        case _:
            use = py
    while plot.fignum_exists(1):
        if not frame < len(use.data):
            frame = 0
        draw(graph, xyz.data, use.data[frame])
        frame += 1
