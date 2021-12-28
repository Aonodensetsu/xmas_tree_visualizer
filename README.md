# Christmas Tree Visualizer
A python wrapper for creating and viewing effects for Matt Parker's christmas tree. Displays PY or CSV effect files and allows creating PY and CSV effects easily.

To use it you need to do a few simple things:
- have *python3* and module *matplotlib* installed
- download and run [visualizer.py](https://raw.githubusercontent.com/Aonodensetsu/xmax-tree-visualizer/main/visualiser.py)

Optionally you can extend its functionality by placing additional files in the same folder:
- get *GIFT* coordinates for a tree ([official 2021](https://www.dropbox.com/s/lmccfutftplhh3b/coords_2021.csv)), rename to coordinates.csv
- load the [default](https://raw.githubusercontent.com/Aonodensetsu/xmas-tree-visualizer/main/effect_default.py) effect as a showcase, rename to tree_effect.py
- create your own effect from the [template](https://raw.githubusercontent.com/Aonodensetsu/xmas-tree-visualizer/main/effect_template.py), rename to tree_effect.py

Some additional features become available when supplied with *GIFT* coordinates:
- preview a CSV effect, rename to tree_effect.csv
- compile PY effects into CSV with ease

CSV effects are created for a specific tree, so you need *GIFT* coordinates for that tree to use them. If coordinates are not found by the program, you can still preview python effects on a default "tree" - a cone (currently). If a PY effect is supploed as well as coordinates, it will be compiled into CSV and then previewed. The generated effects are compliant with [GSD6338/XmasTree](https://github.com/GSD6338/XmasTree). All files available for downloads have comments within them so you can check that they are not malicious.
