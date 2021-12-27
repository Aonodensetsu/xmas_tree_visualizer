# import required libraries
import os
# fix for running via left click
os.chdir(os.path.dirname(os.path.realpath(__file__)))
import csv
import math
import tkinter as tk
import matplotlib as mpl
# force mpl to use tkinter - it's bundled with python
mpl.use('TkAgg', force=True)
import matplotlib.pyplot as plot

# import effect file
if os.path.exists('tree_effect.csv'):
	loaded_module = 0
else:
	loaded_module = 1
	import tree_effect

# create shared variables
x_positions = []
y_positions = []
z_positions = []
frame_times = []
positions = []
colors = []


# get tree coordinates
def create_tree():
	print('Creating tree')
	# get write access to shared variables
	global x_positions
	global y_positions
	global z_positions
	global positions
	if os.path.exists('coordinates.csv'):
		# read GIFT coordinates
		with open('coordinates.csv', mode='r', encoding='utf-8-sig') as csv_file:
			lines = csv_file.readlines()
			for i in range(len(lines)):
				line = lines[i].split(',')
				x_positions.append(float(line[0]))
				y_positions.append(float(line[1]))
				z_positions.append(float(line[2]))
	# if GIFT file doesn't exist, make a cone as a placeholder
	else:
		theta = 0
		radius = 0.95
		height = 0.05
		for i in range(500):
			theta = (theta + 10) % 360
			theta_rad = math.radians(theta)
			radius -= 0.00175
			height += 0.006
			x_positions.append(radius * math.cos(theta_rad))
			y_positions.append(radius * math.sin(theta_rad))
			z_positions.append(height)
	# concatenate coordinates to send to effect
	positions = [{'x': x_positions[i], 'y': y_positions[i], 'z': z_positions[i]} for i, v in enumerate(x_positions)]


# create output csv
def create_csv():
	# create the csv with the header string
	# the string if very long, so construct it programmatically
	with open('tree_effect.csv', mode='w') as effect_file:
		string = 'FRAME_ID,FRAME_TIME'
		for i in range(500):
			for j in range(3):
				color = 'R' if j % 3 == 0 else 'G' if j % 3 == 1 else 'B'
				string += f',{color}_{i}'
		effect_file.write(f'{string}\n')
	# get frame information from effect
	frame = 1
	frame_max = tree_effect.frame_max()
	frame_time = round(1 / tree_effect.frame_rate(), 5)
	# initialize empty storage for effect
	storage = None
	# create effect csv
	# if interrupted will not corrupt csv and will produce a valid file
	# albeit cut in the middle (it updates the file once per frame)
	with open('tree_effect.csv', mode='a+') as effect_file:
		while frame <= frame_max:
			# get current frame from effect
			storage, g_colors = tree_effect.effect(storage, positions, frame)
			# create csv string for all leds
			string = f'{frame - 1},{frame_time}'
			for led in denormalize_rgb(g_colors):
				for rgb in led:
					string += f',{rgb}'
			effect_file.write(f'{string}\n')
			frame += 1


# read instructions
def read_csv():
	global frame_times
	global colors
	with open('tree_effect.csv', mode='r', encoding='utf-8-sig') as csv_instructions:
		reader = list(csv.reader(csv_instructions))
		leds = int((len(reader[0]) - 2) / 3)
		for line in reader[1:]:
			frame_times.append(float(line[1]))
			line_colors = []
			for i in range(leds):
				line_colors.append([float(line[3*i-1]), float(line[3*i]), float(line[3*i+1])])
			colors.append(normalize_rgb(line_colors))


# create visualizer
def gui():
	if not draw_gui:
		return
	# measure screen size and dpi
	screen_measurer = tk.Tk()
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
	# stop plotting when window closed
	window.canvas.mpl_connect('close_event', lambda e: plot.close(window))
	# create 3d plot
	graph = window.add_subplot(111, projection='3d')
	# set camera position
	graph.view_init(elev=15, azim=5)
	# set labels
	graph.set_xlabel('X')
	graph.set_xlim3d(-1, 1)
	graph.set_xticks([-1, 1])
	graph.set_ylabel('Y')
	graph.set_ylim3d(-1, 1)
	graph.set_yticks([-1, 1])
	graph.set_zlabel('Z')
	graph.set_zlim3d(0, max(z_positions))
	graph.set_zticks([0, max(z_positions)])
	# plot wires connecting leds
	graph.plot(x_positions, y_positions, z_positions, color=(0, 0, 0, 0.08))
	# set correct aspect ratio
	graph.set_box_aspect([ub - lb for lb, ub in (getattr(graph, f'get_{a}lim')() for a in 'xyz')])
	# shrink window borders
	plot.tight_layout()
	return graph


# update plot
def draw(graph, frame):
	global colors
	global frame_times
	# clear the previous frame
	for dot in plot.gca().collections:
		dot.remove()
	# plot current values
	graph.scatter3D(x_positions, y_positions, z_positions, c=colors[frame-1], cmap='rgb')
	plot.draw()
	# draw for frame_time
	plot.pause(frame_times[frame-1])


# internally uses normalized rgb, writes 0-255 to csv
def denormalize_rgb(rgb):
	for i, v in enumerate(rgb):
		for j, w in enumerate(v):
			rgb[i][j] = round(255*w)
	return rgb


# reads 0-255 from csv, internally uses normalized
def normalize_rgb(rgb):
	for i, v in enumerate(rgb):
		for j, w in enumerate(v):
			rgb[i][j] = w/255
	return rgb


def main():
	global colors
	# get tree
	create_tree()
	# play the csv if given
	if loaded_module:
		create_csv()
	# read the instruction csv
	read_csv()
	# initialize the gui and get the plot to update later
	graph = gui()
	# get frame information from effect
	frame = 1
	frame_max = len(frame_times)
	# visualize until the visualizer is closed
	while plot.fignum_exists(1):
		# reset back to beginning
		if not frame <= frame_max:
			frame = 1
		# update the plot
		draw(graph, frame)
		frame += 1


# name guard
if __name__ == '__main__':
	draw_gui = 1
	main()
