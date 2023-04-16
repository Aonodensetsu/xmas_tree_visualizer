# Christmas Tree Visualizer
A python wrapper for creating and viewing effects for Matt Parker's (or any other) Christmas tree. Displays PY, CSV or XTREE effect files and allows creating them effects easily.

To use it you need to do a few simple things:
- have *python* (v3.10+) and module *matplotlib* installed
  - all other modules should be installed with Python by default (except tkinter on some installations)
- download and run [visualizer.py](https://raw.githubusercontent.com/Aonodensetsu/xmax-tree-visualizer/main/visualiser.py)

You can extend its functionality by placing additional files in the same folder as the script:
- coordinates.csv - *GIFT* coordinates for a tree ([official 2021](https://www.dropbox.com/s/lmccfutftplhh3b/coords_2021.csv)), will allow you to preview CSV and XTREE effects and compile PY into CSV/XTREE
- tree_effect.py - a PY effect to display on the tree, you can use the [showcase](https://raw.githubusercontent.com/Aonodensetsu/xmas-tree-visualizer/main/effect_default.py) one, or create your own from a [template](https://raw.githubusercontent.com/Aonodensetsu/xmas-tree-visualizer/main/effect_template.py)
- tree_effect.csv - a CSV compiled effect to display on the tree, requires coordinates
- tree_effect.xtree - an XTREE compiled effect to display on the tree, requires coordinates

CSV and XTREE effects are created for a specific tree, so you need *GIFT* coordinates for that tree to use them (I do not have any means of checking if the coordinates are for the correct tree however, your results may vary if you mismatch coordinates with the effect). If coordinates are not found by the program, you can still preview python effects on a default "tree" - a mathemagical cone. 
If a PY effect is supplied as well as coordinates, it will be compiled into CSV and XTREE before it's previewed (the saving itself is nearly without performance cost, and all further repeats of the animation will run from the compiled effect in order not to recalculate the same values - meaning your python code can be very slow, but the visualization will be just fine). The generated effects are compliant with [GSD6338/XmasTree](https://github.com/GSD6338/XmasTree) (including #4).

Note: You can import visualizer.py in your script to compile effects - look at the file contents to see how the classes can be used.

# X-zipper

Now integrated into the visualizer - running any effect (given coordinates) will automatically produce an XTREE file in addition to CSV!

A tool to compress CSV effects to a much smaller size (1/3 of the CSV on average), very fast compression but no inherent* error correction.  
*There is error correction in pretty much all storage and network protocols, the chance to corrupt is negligible and *if* it happens, will only affect a single LED.

The format itself is just a binary representation of the CSV including range limits, so it is possible to read and display directly from it, as easily as it is to read from a CSV.

As with the tool above, you can import it to do your own conversions on the fly with zero cost - thanks to a unified internal representation.
