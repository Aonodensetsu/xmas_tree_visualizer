# Christmas Tree Visualizer
A python wrapper for viewing and creating effects for Matt Parker's christmas tree.
Displays a csv effect file or creates one from a python script.

To use it you need to do a few simple things:
- have *python3* and module *matplotlib* installed
- get *GIFT* format coordinates for the tree you want to create an effect for ([official 2021](https://www.dropbox.com/s/lmccfutftplhh3b/coords_2021.csv))
- rename the GIFT to coordinates.csv
- download the [visualizer.py](https://raw.githubusercontent.com/Aonodensetsu/xmax-tree-visualizer/main/visualiser.py)
- download an already-made effect to view, the [default](https://raw.githubusercontent.com/Aonodensetsu/xmas-tree-visualizer/main/effect_default.py) pythom effect to compile, or create your own from the effect [template](https://raw.githubusercontent.com/Aonodensetsu/xmas-tree-visualizer/main/effect_template.py)
- rename the effect to tree_effect (.csv or .py)
- put all 3 files into the same folder
- run visualizer.py

If no tree_effect.csv is found, the program will generate one and then display it. Otherwise, it will display the file you provided immediately. The generated effects are compliant with [GSD6338/XmasTree](https://github.com/GSD6338/XmasTree). All files available for downloads have comments within them so you can check that they are not malicious.
