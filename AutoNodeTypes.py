#!/usr/bin/env python

# Automatically sets node types to corresponding type

# c = cusp node
# s = smooth node
# z = symmetric
# a = auto smooth
#
# cubicsuperpath: path[subpath][tupel of data: 0=HandleA, 1=Node, 2=HandleB][0=X, 1=Y]

import inkex
import sys
import numpy as np
import math

import simpletransform
import cubicsuperpath


def enum(**enums):
    return type('Enum', (), enums)


POS = enum(X=0, Y=1)
T = enum(HA=0, NODE=1, HB=2)


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
                                     dest="symmetry", default="",
                                     help="What node type to use for lined up handles with same lenght.")
        self.OptionParser.add_option("--zero",
                                     action="store", type="string",
                                     dest="zero", default="",
                                     help="What node type to use for no handles")

    def cleanPath(self, path):
        # See if the node xy-positions of the first and the two last nodes are the same
        if (path[0][T.NODE][POS.X] == path[-1][T.NODE][POS.X] == path[-2][T.NODE][POS.X] and
           path[0][T.NODE][POS.Y] == path[-1][T.NODE][POS.Y] == path[-2][T.NODE][POS.Y]):

            path.pop()  # remove last, additional 0,0 node
            path[0][T.HA] = path[-1][T.HA]  # get A Handle data from last item
            path[-1][T.HB] = path[0][T.HB]  # get B Handle data from first item

        return path

    def effect(self):

        debugmsg = 0  # set to 1 for output
        threshold = math.radians(self.options.threshold)

        # Iterate through all the selected objects in Inkscape
        for id, node in self.selected.iteritems():

            # Check if the node is a path ( "svg:path" node in XML )
            if node.tag == inkex.addNS('path', 'svg'):

                # get the string of all nodetypes
                types = node.get("{http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd}nodetypes")
                if debugmsg:
                    sys.stderr.write("Old Nodetypes: " + str(types) + "\n\n")

                # bake (or fuse) transform
                simpletransform.fuseTransform(node)
                # turn into cubicsuperpath
                d = node.get('d')
                p = cubicsuperpath.parsePath(d)

                new_types = ""  # new nodetype string, all subpaths added together

                for subpath in p:  # there may be several paths joined together (e.g. holes)

                    subpath = self.cleanPath(subpath)

                    output_all = "----=== Path " + node.get('id') + " ===----\n\n"

                    for i, csp in enumerate(subpath):  # groups of three to handle control points.

                        output_all += "Node: " + str(i) + "\n"
                        # get clean vector data for both handles
                        # we need to round them pretty much to pass 0,0 and symmetry tests
                        # I guess that's okay, since we don't *change* that path data

                        vec_a = np.array([round(csp[T.HA][POS.X] - csp[T.NODE][POS.X], 2), round(csp[T.HA][POS.Y] - csp[T.NODE][POS.Y], 2)])  # numpy vectors
                        vec_b = np.array([round(csp[T.HB][POS.X] - csp[T.NODE][POS.X], 2), round(csp[T.HB][POS.Y] - csp[T.NODE][POS.Y], 2)])

                        # check for 0,0 handles
                        if ((vec_a[POS.X] == vec_a[POS.Y] == 0.0) or
                           (vec_b[POS.X] == vec_b[POS.Y] == 0.0)):

                            output_all += "at least one zero handle... "
                            output_all += str(vec_a) + " <- a or b -> " + str(vec_b) + "\n"
                            new_types += self.options.zero
                        else:
                            # pure Symmetry check, will do some heavy lifting with simple math
                            if (vec_a[POS.X] == -vec_b[POS.X] and
                               vec_a[POS.Y] == -vec_b[POS.Y]):

                                output_all += "!!! Symmetry: " + str(vec_a[POS.X]) + " == (-) " + str(vec_b[POS.X]) + " and " + str(vec_a[POS.Y]) + " == (-) " + str(vec_b[POS.Y]) + "\n"
                                new_types += self.options.symmetry
                            else:
                                # now that we are rid of zero handles, let's do vector magic (thanks copypaste)
                                output_all += "Vec A: " + str(vec_a) + " & Vec B: " + str(vec_b) + " are ... \n"
                                vec_au = vec_a / np.linalg.norm(vec_a)  # to unit vectors
                                vec_bu = vec_b / np.linalg.norm(vec_b)
                                angle = round(np.arccos(np.clip(np.dot(vec_au, vec_bu), -1.0, 1.0)), 3)  # the angle between them in radians. 180 = Pi

                                if angle >= threshold:
                                    output_all += "Smooth: " + str(angle) + " angle >= threshold " + str(threshold) + "\n"
                                    new_types += "s"  # smooth
                                else:
                                    output_all += "not in line... \n"
                                    new_types += "c"  # cusp

                        output_all += "\n"

                    output_all += "New Types: " + str(new_types) + "\n"
                    if new_types == types:
                        output_all += ("Same as old...\n")

                    # apply the changes
                    node.set("{http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd}nodetypes", new_types)

                    if debugmsg:
                        sys.stderr.write(output_all)
                        sys.stderr.write("\n\n\n")


# Create effect instance and apply it.
effect = TemplateEffect()
effect.affect()
