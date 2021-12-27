# import effect file
import tree_effect

# import required libraries
import tkinter
import matplotlib as mpl
mpl.use('TkAgg', force=True)
import matplotlib.pyplot as plot

# read GIFT coordinates
x_values = []
y_values = []
z_values = []
with open('coordinates.csv', mode='r', encoding='utf-8-sig') as csv_f:
    lines = csv_f.readlines()
    for i in range(len(lines)):
        line = lines[i].split(',')
        x_values.append(line[0])
        y_values.append(line[1])
        z_values.append(line[2])
# change strings to floats
x_values = [float(val) for val in x_values]
y_values = [float(val) for val in y_values]
z_values = [float(val) for val in z_values]
# concatenate coordinates
positions = [{'x': x_values[i], 'y': y_values[i], 'z': z_values[i]} for i, v in enumerate(x_values)]


# create visualizer
def gui():
    # measure screen
    screen_measurer = tkinter.Tk()
    dpi = screen_measurer.winfo_fpixels('1i')
    screen_height = screen_measurer.winfo_screenheight()
    # compute a sensible size for the visualizer
    top = int(0.05 * screen_height)
    height = int(0.8 * screen_height)
    left = 100
    width = int(0.9 * height)
    screen_measurer.update()
    screen_measurer.destroy()
    # create window
    mpl.rcParams['toolbar'] = 'None'
    window = plot.figure(num='Christmas Tree Visualiser')
    # move and resize window
    window.canvas.manager.window.wm_geometry(f'+{left}+{top}')
    window.set_size_inches(width / dpi, height / dpi)
    # listen to closing
    window.canvas.mpl_connect('close_event', lambda e: plot.close(window))
    # create 3d plot
    graph = window.add_subplot(111, projection='3d')
    # set preferences
    graph.view_init(elev=15, azim=5)
    graph.set_xlabel('X')
    graph.set_xlim3d(-1, 1)
    graph.set_xticks([-1, 1])
    graph.set_ylabel('Y')
    graph.set_ylim3d(-1, 1)
    graph.set_yticks([-1, 1])
    graph.set_zlabel('Z')
    graph.set_zlim3d(0, max(z_values))
    graph.set_zticks([0, max(z_values)])
    # plot wires
    graph.plot(x_values, y_values, z_values, color=(0, 0, 0, 0.07))
    # set correct aspect ratio
    graph.set_box_aspect([ub - lb for lb, ub in (getattr(graph, f'get_{a}lim')() for a in 'xyz')])
    plot.tight_layout()
    return graph


# update plot
def draw(graph, colors):
    # if the window was closed, don't draw
    if not plot.fignum_exists(1):
        return
    # clear the previous frame
    for dot in plot.gca().collections:
        dot.remove()
    # plot current values
    graph.scatter3D(x_values, y_values, z_values, c=colors, cmap='rgb')
    plot.draw()
    # limit to 30 fps
    plot.pause(1/30)


# the csv needs 0-255 values
def denormalize_rgb(rgb):
    for i, v in enumerate(rgb):
        for j, w in enumerate(v):
            rgb[i][j] = round(255*w)
    return rgb


if __name__ == '__main__':
    with open('tree_effect.csv', mode='w') as effect_file:
        # construct the header string
        string = 'FRAME_ID'
        for i in range(500):
            for j in range(3):
                color = 'R' if j % 3 == 0 else 'G' if j % 3 == 1 else 'B'
                string += f',{color}_{i}'
        effect_file.write(f'{string}\n')
    graph_r = gui()
    frame = 1
    frame_max = tree_effect.frame_max()
    with open('tree_effect.csv', mode='a') as effect_file:
        storage = None
        while frame <= frame_max:
            string = f'{frame-1}'
            storage, colors = tree_effect.effect(storage, positions, frame)
            draw(graph_r, colors)
            for led in denormalize_rgb(colors):
                for rgb in led:
                    string += f',{rgb}'
            effect_file.write(f'{string}\n')
            frame += 1
    plot.show()
