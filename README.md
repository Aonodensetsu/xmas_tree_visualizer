# Christmas Tree Visualizer
A python wrapper for creating and viewing effects for Matt Parker's christmas tree. Displays PY or CSV effect files and allows creating PY and CSV effects easily.

To use it you need to do a few simple things:
- have *python3* and module *matplotlib* installed
- download and run [visualizer.py](https://raw.githubusercontent.com/Aonodensetsu/xmax-tree-visualizer/main/visualiser.py)

You can extend its functionality by placing additional files in the same folder:
- coordinates.csv - *GIFT* coordinates for a tree ([official 2021](https://www.dropbox.com/s/lmccfutftplhh3b/coords_2021.csv)), will allow you to preview that tree, run CSV effects and compile PY into CSV
- tree_effect.py - a PY effect to display on the tree, you can use the [showcase](https://raw.githubusercontent.com/Aonodensetsu/xmas-tree-visualizer/main/effect_default.py) one, or create your own from a [template](https://raw.githubusercontent.com/Aonodensetsu/xmas-tree-visualizer/main/effect_template.py)
- tree_effect.csv - a CSV effect to display on the tree, requires coordinates

CSV effects are created for a specific tree, so you need *GIFT* coordinates for that tree to use them. If coordinates are not found by the program, you can still preview python effects on a default "tree" - a cone (currently). If a PY effect is supplied as well as coordinates, it will be compiled into CSV while it's previewed. The generated effects are compliant with [GSD6338/XmasTree](https://github.com/GSD6338/XmasTree). All files available for download have comments within them so you can check that they are not malicious.

The effects are simple python files that consist of the following 3 functions:
- frame_rate - specifies the framerate that you want the animation to play at
- frame_max - specifies the length of the animation before repeating from the beginning
- effect (storage, positions, frame) - the effect itself, you get information about the tree and return rgb colors and storage for the next frame
- - storage - you can keep data you might need to refer to in later parts of the animation
- - positions - a list of {x, y, z} positions of all LEDs in the tree
- - frame - the current frame

You can import visualizer.py safely due to a __name__ guard and you can compile csv by running main() after it's imported - it will not open a GUI.
