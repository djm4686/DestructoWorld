__author__ = 'daniel.madden'
import node


# Unused
class PXNode(node.Node):

    def __init__(self, pos, ide, val):
        node.Node.__init__(self, pos, ide)
        self.val = val