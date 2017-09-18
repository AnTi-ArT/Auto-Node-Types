# Auto-Node-Types
Inkscape extension that automatically sets the right type (cusp/smooth/symmetry) to handles of the selected path/s.

Maybe there is a bug in Inkscape or maybe my workflow sucks (unlikely...), but I noticed that the handles sometimes lose their correct type.
For Example after path operations or smoothing.
If your handles look smooth, but somehow are cusp - just run this extension.

# Installation
Copy AutoNodeTypes.py and AutoNodeTypes.inx to your Inkscape extensions Folder.
Linux e.g. /home/you/.config/inkscape/extensions/

# Options
- Minimum Angle to smooth: Is a threshold or buffer. The maximum angle between handles is 180 degrees (aka "a line"). Due to rounding and human error sometimes handles end up with a slightly lower value. You can still force them to become smooth. They will, however, not change their actual position to a line until you manually change the handle a bit.
- Handles with same length will be: Smooth, Symmetric, Cusp or Auto Smooth. If you draw with the pen tool, you will generate a lot of handles that look symmetric (same lengths), but are in fact of type smooth (could be different lengths) - which is likely what you want for further editing. With this setting you can keep those "smooth" or change them to any other type. Defaults to smooth.
- Zero handles will be: Cusp, Smooth, Symmetric or Auto Smooth. Default is Cusp and you better leave it that way, because unexpected behaviour can happen ;-) ... or just go ahead and experiment. But make a backup of your artwork first...
- Debug? Prints some Debug messages.

# Credits
- Based on this extension that prints out XY Coordinates of nodes and handles: http://www.inkscapeforum.com/viewtopic.php?t=8826#p32088
- Angle of vectors code is from here: https://stackoverflow.com/questions/2827393/angles-between-two-n-dimensional-vectors-in-python#13849249
