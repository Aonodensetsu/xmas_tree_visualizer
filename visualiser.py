# import required libraries
import os
import sys
import csv
import math
import tkinter
import matplotlib
# force mpl to use tkinter - it's bundled with python
matplotlib.use('TkAgg', force=True)
matplotlib.rc('grid', color='None')
import matplotlib.pyplot as plot

# fix for running via left click
os.chdir(os.path.dirname(os.path.realpath(__file__)))

# try to import PY effect
if os.path.exists('tree_effect.py'):
	import tree_effect

# create shared variables
x_positions = []
y_positions = []
z_positions = []
frame_times = []
positions = []
colors = []


# get tree coordinates
def get_tree():
	print('Fetching tree')
	# get write access to shared variables
	global x_positions
	global y_positions
	global z_positions
	global positions
	# check if GIFT available
	if os.path.exists('coordinates.csv'):
		# read GIFT coordinates
		with open('coordinates.csv', mode='r', encoding='utf-8-sig') as csv_file:
			lines = csv_file.readlines()
			for i in range(len(lines)):
				line = lines[i].split(',')
				x_positions.append(float(line[0]))
				y_positions.append(float(line[1]))
				z_positions.append(float(line[2]))
		# concatenate coordinates to send to effect
		positions = [{'x': x_positions[i], 'y': y_positions[i], 'z': z_positions[i]} for i, v in enumerate(x_positions)]
		return True
	# if GIFT file doesn't exist, make a cone as a placeholder
	else:
		print('Creating tree')
		theta = 0
		height = 0.006
		for i in range(500):
			theta_rad = math.radians(theta)
			radius = (0.006*525-height)/3.6
			x_positions.append(radius * math.cos(theta_rad))
			y_positions.append(radius * math.sin(theta_rad))
			z_positions.append(height)
			theta = (theta + 10) % 360
			height += 0.006
		# concatenate coordinates to send to effect
		positions = [{'x': x_positions[i], 'y': y_positions[i], 'z': z_positions[i]} for i, v in enumerate(x_positions)]
		return False


# create csv
def create_csv():
	print('Creating CSV')
	# create the csv with the header string
	# the string if very long, so construct it programmatically
	with open('tree_effect.csv', mode='w') as effect_file:
		string = 'FRAME_TIME'
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
	# create window
	graph = gui()
	# create effect csv
	# if interrupted will not corrupt csv and will produce a valid file
	# albeit cut in the middle (it updates the file once per frame)
	with open('tree_effect.csv', mode='a+') as effect_file:
		while frame <= frame_max:
			# get current frame from effect
			storage, l_colors = tree_effect.effect(storage, positions, frame)
			# update plot
			draw(graph, frame, l_colors)
			# create csv string for all leds
			string = f'{frame_time}'
			for led in l_colors:
				for rgb in led:
					string += f',{rgb}'
			# update CSV file
			effect_file.write(f'{string}\n')
			frame += 1
	# return created window to continue playback
	return graph


# read instructions
def read_csv():
	print('Reading CSV')
	global frame_times
	global colors
	# clear global tables to not get corrupted
	frame_times = []
	colors = []
	with open('tree_effect.csv', mode='r', encoding='utf-8-sig') as csv_instructions:
		reader = list(csv.reader(csv_instructions))
		leds = int((len(reader[0]) - 1) / 3)
		for line in reader[1:]:
			frame_times.append(float(line[0]))
			line_colors = []
			for i in range(leds):
				line_colors.append([float(line[3*i-2]), float(line[3*i-1]), float(line[3*i])])
			colors.append(line_colors)


# create visualizer
def gui():
	# don't draw if importing, but still allow creating a csv by calling main()
	if not __name__ == '__main__':
		return
	print('Creating GUI')
	# measure screen size and dpi
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
	matplotlib.rcParams['toolbar'] = 'None'
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
	# set background color
	window.patch.set_facecolor('#4c4a48')
	graph.set(fc='#4c4a48')
	graph.xaxis.pane.set_alpha(0)
	graph.yaxis.pane.set_alpha(0)
	graph.zaxis.pane.set_alpha(0)
	# set labels
	graph.set_xlabel('X', color='white', labelpad=-5)
	graph.set_ylabel('Y', color='white', labelpad=-5)
	graph.set_zlabel('Z', color='white', labelpad=5)
	graph.set(xlim3d=(-1, 1), ylim3d=(-1, 1), zlim3d=(0, max(z_positions)))
	graph.set(xticks=[-1, 1], yticks=[-1, 1], zticks=[0, max(z_positions)])
	graph.margins(x=0, y=0, z=0, tight=True)
	graph.tick_params(which='both', color='None', labelcolor='white')
	graph.tick_params(axis='both', pad=5)
	graph.tick_params(axis='z', pad=15)
	# plot wires connecting leds
	graph.plot(x_positions, y_positions, z_positions, color=(0, 0, 0, 0.08))
	# set correct aspect ratio
	graph.set_box_aspect([ub - lb for lb, ub in (getattr(graph, f'get_{a}lim')() for a in 'xyz')])
	# shrink window borders
	plot.tight_layout()
	return graph


# update plot
def draw(graph, frame, color=None):
	# ignore calls if no window exists
	if not plot.fignum_exists(1):
		return
	# if color is given, it comes from a PY effect
	color_flag = 0
	if not color:
		global colors
		color_flag = 1
		color = colors[frame-1]
	global frame_times
	# clear the previous frame
	for dot in plot.gca().collections:
		dot.remove()
	# plot current values
	graph.scatter3D(x_positions, y_positions, z_positions, c=color, cmap='rgb', norm=matplotlib.colors.Normalize(vmin=0, vmax=255))
	plot.draw()
	# draw for frame_time
	if color_flag:
		pause_for = frame_times[frame-1]
	else:
		pause_for = 1/tree_effect.frame_rate()
	plot.pause(pause_for)


# check the current state
def get_state():
	print('Getting state')
	# state is a binary value for available files
	state = 0
	# is a PY effect available?
	if 'tree_effect' in sys.modules:
		state += 1
	# is a CSV effect available?
	if os.path.exists('tree_effect.csv'):
		state += 2
	# are coordinates available?
	if get_tree():
		state += 4
	return state


# run the program
def main():
	print('Running program')
	# read shared variables
	global positions
	# check the current state of the program
	match get_state():
		# 0 - no files are loaded, show a default tree with black LEDs
		# 2 - only a CSV effect is loaded, ignore it since there is no tree
		# 4 - only the coordinates are loaded, show the tree with black LEDs
		case 0 | 2 | 4:
			# create a fake CSV with one frame
			frame_times.append(1 / 30)
			colors.append([[0, 0, 0] for _ in range(len(positions))])
			# create window
			graph = gui()
			# draw gui
			draw(graph, 1)
			plot.show()
			exit()
		# 1 - only a PY effect is loaded, show on a default tree
		# 3 - PY and CSV effects loaded, ignore CSV since there is no tree
		case 1 | 3:
			# set up frame counters
			frame = 1
			frame_max = tree_effect.frame_max()
			# give storage to the PY effect
			storage = None
			# create window
			graph = gui()
			while plot.fignum_exists(1):
				# reset from beginning
				if not frame <= frame_max:
					frame = 1
				# get current frame from effect
				storage, l_colors = tree_effect.effect(storage, positions, frame)
				draw(graph, frame, l_colors)
				frame += 1
			exit()
		# 5 - a PY effect and coordinates are loaded, play it and create csv
		case 5:
			# create a csv (also visualizes while creating)
			# return the created window to keep playback after it's done
			graph = create_csv()
			# when CSV created, read its contents
			read_csv()
			# get frames from csv
			frame = 1
			frame_max = len(frame_times)
			print('Now previewing from CSV - check if compiled correctly')
			# preview while window open
			while plot.fignum_exists(1):
				# restart from beginning
				if not frame <= frame_max:
					frame = 1
				# update plot
				draw(graph, frame)
				frame += 1
			exit()
		# 6 - coordinates and CSV effect loaded, play back the CSV
		# 7 - coordinates, CSV and PY effects are loaded, ignore PY, play back CSV
		case 6 | 7:
			# read instructions from CSV
			read_csv()
			# set up frame counters
			frame = 1
			frame_max = len(frame_times)
			# create window
			graph = gui()
			# while GUI open, update plot
			while plot.fignum_exists(1):
				# restart from beginning
				if not frame <= frame_max:
					frame = 1
				# update plot
				draw(graph, frame)
				frame += 1
			exit()


# name guard
if __name__ == '__main__':
	main()
