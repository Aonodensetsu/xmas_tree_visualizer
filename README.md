# Christmas Tree Visualizer
A python wrapper for creating effects for Matt Parker's christmas tree.
Displays a csv effect file or creates one from a python script.

To use it you need to do a few simple things:
- have *python3* and module *matplotlib* installed
- get *GIFT* format coordinates for the tree you want to create an effect for ([official 2021](https://www.dropbox.com/s/lmccfutftplhh3b/coords_2021.csv))
- rename the GIFT to coordinates.csv
- download the [visualizer.py](https://raw.githubusercontent.com/Aonodensetsu/xmax-tree-visualizer/main/visualiser.py)
- download the [default](https://raw.githubusercontent.com/Aonodensetsu/xmas-tree-visualizer/main/effect_default.py) effect generator, create your own from the [template](https://raw.githubusercontent.com/Aonodensetsu/xmas-tree-visualizer/main/effect_template.py) or use an already made effect csv
- rename the effect to tree_effect (.csv or .py)
- put all 3 files into the same folder
- run visualizer.py

The script will show you how the effect looks on a GUI and, if generating a preview from a script, generate tree_effect.csv which is compliant with [GSD6338/XmasTree](https://github.com/GSD6338/XmasTree). If your provide a tree_effect.csv, it will only preview its contents. All files available for downloads have comments within them so you can check that they are not malicious.
