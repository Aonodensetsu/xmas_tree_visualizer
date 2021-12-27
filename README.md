# Christmas Tree Visualizer
A python wrapper for creating and viewing effects for Matt Parker's christmas tree.
Displays py or csv effect files and allows creating py effects easily.

To use it you need to do a few simple things:
- have *python3* and module *matplotlib* installed
- download the [visualizer.py](https://raw.githubusercontent.com/Aonodensetsu/xmax-tree-visualizer/main/visualiser.py)
- download the [default](https://raw.githubusercontent.com/Aonodensetsu/xmas-tree-visualizer/main/effect_default.py) python effect or create your own from the effect [template](https://raw.githubusercontent.com/Aonodensetsu/xmas-tree-visualizer/main/effect_template.py)
- rename the effect to tree_effect.py
- put all files into the same folder
- run visualizer.py

Optionally you can extend its functionality by:
- using *GIFT* coordinates for a tree ([official 2021](https://www.dropbox.com/s/lmccfutftplhh3b/coords_2021.csv)), they need to be renamed coordinates.csv
- using a premade csv effect (requires GIFT coordinates)
- creating csv effects from py effects (requires GIFT coordinates)

If no coordinates.csv file is found, the program will not work if given a csv effect, it will however display a cone as a fallback "tree" when supplied with a py effect.
If no tree_effect.csv is found, the program will generate one and then display it. Otherwise, it will display the file you provided immediately. The generated effects are compliant with [GSD6338/XmasTree](https://github.com/GSD6338/XmasTree). All files available for downloads have comments within them so you can check that they are not malicious.
