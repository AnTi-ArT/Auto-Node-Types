#!/usr/bin/env python

# Automatically sets node types to corresponding type

# c = cusp node
# s = smooth node
# z = symmetric
# a = auto smooth

import inkex
import sys
import numpy as np
import math

import simpletransform
import cubicsuperpath


class TemplateEffect(inkex.Effect):
    def __init__(self):
        # Call base class construtor.
        inkex.Effect.__init__(self)

        # self.options.destName
        self.OptionParser.add_option("--threshold",
                                     action="store", type="float",
                                     dest="threshold", default=178.0,
                                     help="Minimum angle to smooth out (max 180)")
        self.OptionParser.add_option("--symmetry",
                                     action="store", type="string",
                                     dest="symmetry", default='s',
                                     help="What node type to use for lined up handles with same lenght.")
        self.OptionParser.add_option("--zero",
                                     action="store", type="string",
                                     dest="zero", default='c',
                                     help="What node type to use for no handles")
        self.OptionParser.add_option("--debugmsg",
                                     action="store", type="inkbool",
                                     dest="debugmsg", default=1,
                                     help="Show Debug Messages")

    def effect(self):

        threshold = math.radians(self.options.threshold)

        # Iterate through all the selected objects in Inkscape
        for id, node in self.selected.iteritems():

            # Check if the node is a path ( "svg:path" node in XML )
            if node.tag == inkex.addNS('path', 'svg'):

                # DEBUG Create the string variable which will hold the formatted data (note that '\n' defines a line break)
                output_all = ""
                output_all += "----=== Path " + node.get('id') + " ===----\n\n"

                # get the string of all nodetypes
                types = node.get("{http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd}nodetypes")
                output_all += "Old Nodetypes: " + str(types) + "\n\n"

                # bake (or fuse) transform
                simpletransform.fuseTransform(node)
                # turn into cubicsuperpath
                d = node.get('d')
                p = cubicsuperpath.parsePath(d)

                for subpath in p:  # there may be several paths joined together (e.g. holes)

                    i = 0  # iterator for the nodetypes string
                    new_types = ""  # new nodetype string

                    for csp in subpath:  # groups of three to handle control points.

                        output_all += "Node # " + str(i) + ": \n"
                        # get clean vector data for both handles
                        vec_ax = round(csp[0][0] - csp[1][0], 2)  # we need to round them pretty much to pass 0,0 and symmetry tests
                        vec_ay = round(csp[0][1] - csp[1][1], 2)
                        vec_bx = round(csp[2][0] - csp[1][0], 2)
                        vec_by = round(csp[2][1] - csp[1][1], 2)

                        # check for 0,0 handles
                        if ((vec_ax == vec_ay == 0.0) or (vec_bx == vec_by == 0.0)):
                            output_all += "at least one zero handle... " + str(vec_ax + vec_ay) + " :a or b: " + str(vec_bx + vec_by) + "\n"
                            new_types += self.options.zero
                        else:
                            # pure Symmetry check, will do some heavy lifting with simple math
                            if (vec_ax == -vec_bx) and (vec_ay == -vec_by):
                                output_all += "!!! Symmetry: " + str(vec_ax) + " == (-) " + str(vec_bx) + " and " + str(vec_ay) + " == (-) " + str(vec_by) + "\n"
                                new_types += self.options.symmetry
                            else:
                                # now that we are rid of zero handles, let's do vector magic (thanks copypaste)
                                vec_a = np.array([vec_ax, vec_ay])  # numpy vectors
                                vec_b = np.array([vec_bx, vec_by])
                                output_all += "Vec A: " + str(vec_a) + " & Vec B: " + str(vec_b) + " are ... \n"
                                vec_au = vec_a / np.linalg.norm(vec_a)  # to unit vectors
                                vec_bu = vec_b / np.linalg.norm(vec_b)
                                angle = round(np.arccos(np.clip(np.dot(vec_au, vec_bu), -1.0, 1.0)), 3)  # the angle between them in radians. 180 = Pi

                                if angle >= threshold:
                                    output_all += "Smooth: " + str(angle) + " angle >= threshold " + str(threshold) + "\n"
                                    new_types += "s"  # smooth
                                else:
                                    output_all += "not in line... \n"
                                    if types is None:
                                        new_types += "c"
                                    else:
                                        new_types += types[i]  # get the old type.

                        output_all += "\n"
                        i += 1
                    output_all += "New Types: " + str(new_types) + "\n"
                    if new_types == types:
                        output_all += ("Same as old...\n")

                    # apply the changes
                    node.set("{http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd}nodetypes", new_types)

                    if self.options.debugmsg:
                        sys.stderr.write(output_all)
                        sys.stderr.write("\n\n\n")


# Create effect instance and apply it.
effect = TemplateEffect()
effect.affect()
