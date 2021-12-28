# Christmas Tree Visualizer
A python wrapper for creating and viewing effects for Matt Parker's christmas tree.
Displays py or csv effect files and allows creating py effects easily.

To use it you need to do a few simple things:
- have *python3* and module *matplotlib* installed
- download and run [visualizer.py](https://raw.githubusercontent.com/Aonodensetsu/xmax-tree-visualizer/main/visualiser.py)

Optionally you can extend its functionality by:
- using *GIFT* coordinates for a tree ([official 2021](https://www.dropbox.com/s/lmccfutftplhh3b/coords_2021.csv)), they need to be renamed coordinates.csv
- using the [default](https://raw.githubusercontent.com/Aonodensetsu/xmas-tree-visualizer/main/effect_default.py) effect
- creating your own effect from the [template](https://raw.githubusercontent.com/Aonodensetsu/xmas-tree-visualizer/main/effect_template.py)
- using a premade csv effect (requires GIFT coordinates)
- compiling py effects into csv (requires GIFT coordinates)

Csv effects are created for a specific tree, so you need GIFT coordinates for that tree to use them. If GIFT coordinates are not found by the program, you can still preview python effects on a default "tree" - a cone. If a py effect is supplied as well as coordinates, the py code will be complied to csv and then previewed. The generated effects are compliant with [GSD6338/XmasTree](https://github.com/GSD6338/XmasTree). All files available for downloads have comments within them so you can check that they are not malicious.
