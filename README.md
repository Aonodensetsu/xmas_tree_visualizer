# Christmas Tree Visualizer
A python wrapper for creating and viewing effects for Matt Parker's (or any other) Christmas tree. Displays PY, CSV or XTREE effect files and allows creating effects easily.

To use it you need to do a few simple things:
- have *python* (v3.10+) and module *matplotlib* installed
  - all other modules should be installed with Python by default (except *tkinter* on some installations)
- download [visualizer.py](https://raw.githubusercontent.com/Aonodensetsu/xmax-tree-visualizer/main/visualiser.py) and [x_zipper.py](https://raw.githubusercontent.com/Aonodensetsu/xmas_tree_visualizer/main/x_zipper.py) and run the visualizer

You can extend its functionality by placing additional files in the same folder as the scripts:
- coordinates.csv - *GIFT* coordinates for a tree ([official 2021](https://www.dropbox.com/s/lmccfutftplhh3b/coords_2021.csv)), will allow you to preview CSV and XTREE effects and compile PY into CSV/XTREE
- tree_effect.py - a Python effect to display on the tree, you can use the [showcase](https://raw.githubusercontent.com/Aonodensetsu/xmas-tree-visualizer/main/effect_default.py) one, or create your own from a [template](https://raw.githubusercontent.com/Aonodensetsu/xmas-tree-visualizer/main/effect_template.py)
- tree_effect.csv - a CSV compiled effect to display on the tree, requires coordinates
- tree_effect.xtree - an XTREE compiled effect to display on the tree, requires coordinates

CSV and XTREE effects are created for a specific tree, so you need *GIFT* coordinates for that tree to use them (I do not have any means of checking if the coordinates are for the correct tree however, your results may vary if you mismatch coordinates with the effect). If coordinates are not found by the program, you can still preview PY effects on a default "tree" - a mathemagical cone.  
You can override the requirement by creating fake coordinates with `Coordinates().make(LED_NUM).write()`.

If a PY effect is supplied as well as coordinates, it will be compiled into CSV and XTREE before it's previewed (the saving itself is essentially free, and the preview will run from the compiled effect in order not to recalculate the same values - meaning your python code can be very slow, but the visualization will be just fine). The generated effects are compliant with [GSD6338/XmasTree](https://github.com/GSD6338/XmasTree) (including #4).

Note: You can import x_zipper.py in your script to compile effects without preview - look at the file contents to see how the classes can be used.

# X_zipper

Now integrated into the visualizer - running any effect (given coordinates) will automatically produce both compressed animation types! Can still be run as a standalone application to convert on the fly.

A tool to compress CSV effects to a much smaller size (~1/3 of the CSV), very fast compression but no inherent* error correction.  
*There is error correction in pretty much all storage and network protocols, the chance to corrupt is negligible and *if* it happens, will only affect a single LED for a single frame.

The format itself is just a binary representation of the CSV taking account of range limits*, so it is possible to read and display directly from it, as easily as it is to read from a CSV.  
*This puts a limit on the amount of LEDs a tree can have at just over 16 million, also limits the FPS at 65 thousand (message me if you need more :p)

You can import this tool into your code to convert between compatible formats with negligible overhead.
