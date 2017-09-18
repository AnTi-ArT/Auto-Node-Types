# Auto Node Types
Inkscape extension that automatically sets the right type (cusp/smooth/symmetry) to handles of the selected path/s.

Maybe there is a bug in Inkscape ~~or maybe my workflow sucks~~ (unlikely...), but I noticed that the handles sometimes lose their correct type.
For Example after deleting a node (A) or smoothing (B).
If your handles look smooth, but for some reason are cusp - just run this extension.

![a-n-types](https://user-images.githubusercontent.com/6949092/30559727-e8be8f74-9cb5-11e7-94fc-c0f601bd901c.png)

## Installation
Copy `AutoNodeTypes.py` and `AutoNodeTypes.inx` to your Inkscape Extensions Folder.
Linux e.g. /home/you/.config/inkscape/extensions/

Open the extension with `Inkscape -> Extensions -> Modify Path -> Auto Node Types`

## Options
- _Minimum Angle to smooth_: Is a threshold. Everything bigger as the value will be recognized as directly opposite. The maximum angle between handles is `180` degrees (aka "a line"). Due to rounding and human error handles often end up with a slightly lower value and will not be smoothed. That's why the default is set to 178. You can force *any* angle between handles to become smooth. The handles will, however, not change their actual position to a line until you manually change the handle a bit.
- _Handles with same length will be_: `Smooth`, `Symmetric`, `Cusp` or `Auto Smooth`. If you draw with the pen tool, you will generate a lot of handles that look symmetric (same lengths), but are in fact of type smooth (could be different lengths) - which is likely what you want for further editing. With this setting you can keep those "smooth" or change them to any other type. Defaults to **Smooth**.
- _Zero handles will be_: `Cusp`, `Smooth`, `Symmetric` or `Auto Smooth`. Default is **Cusp** and you better leave it that way, because unexpected behaviour can happen :dancers: ... or just go ahead and experiment. But make a backup of your artwork first...
- _Debug?_ Prints some Debug messages.

## Credits
- [Based on this extension that prints out XY Coordinates of nodes and handles.](http://www.inkscapeforum.com/viewtopic.php?t=8826#p32088)
- [Angle of two vectors code is from here.](https://stackoverflow.com/questions/2827393/angles-between-two-n-dimensional-vectors-in-python#13849249)
