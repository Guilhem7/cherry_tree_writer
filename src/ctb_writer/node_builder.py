"""
Class that allow to build a node given the parameters wanted
"""
from os.path import expanduser
from .assets import get_icon
from .cherry_tree_node import CherryTreeNode, CherryTreeImage
import xml.etree.ElementTree as ET

class CherryTreeNodeBuilder:
    """
    Builder for a cherry tree node
    """
    def __init__(self, name, color=None, bold=False):
        self.node = CherryTreeNode(name)

        if bold:
            self.node.set_bold_title()

        if color:
            self.node.set_title_color(color)

    def icon(self, name):
        """
        Add Icon to the given node
        """
        self.node.icon = get_icon(name)
        return self

    def text(self, text, style={}):
        """
        Add the Text to a node
        """
        self.node.add_text(text, attrib=style)
        return self

    def image(self, filename, position=-1):
        """
        Insert an image in the node, at the given position, default position is
        "-1" that refers to the end of text

        :param filename: The path to the images to insert
        :type filename: str

        :param position: The position of the images in the text
        :type position: int (default: -1)
        """
        self.node.add_image(filename, position=position)
        return self

    def set_read_only(self):
        """
        Set the node as read only
        """
        self.node.is_ro = 1
        return self

    def get_node(self):
        """
        Return the associated node
        """
        return self.node
