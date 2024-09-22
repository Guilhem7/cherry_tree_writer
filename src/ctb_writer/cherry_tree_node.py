"""
Class representing a cherry tree node
"""
from os.path import expanduser
from dataclasses import dataclass
from .beautify import CherryTreeRichtext, color
import xml.etree.ElementTree as ET

@dataclass
class CherryTreeImage:
    """Class holding image information"""
    data: bytes
    position: int

class CherryTreeNode:
    """
    Class holding node data
    """
    def __init__(self, name, xml=None, father_id=0, icon=0, is_ro=0, images=None, children=None):
        self.node_id = None
        self.name = name
        self.title_style = {"color": None, "bold": False}

        self.is_ro = is_ro
        self.icon = icon

        self.father_id = father_id
        self.images = [] if images is None else images
        self.children = [] if children is None else children

        self.xml = ET.fromstring(self.get_base_xml()) if xml is None else xml

    @color
    def set_title_color(self, color):
        """
        Set the color of the title
        """
        self.title_style["color"] = color

    def set_bold_title(self):
        """
        Set the Node title as bold
        """
        self.title_style["bold"] = True

    def get_title_style(self):
        """
        Used to access the style of the title
        """
        return self.title_style

    @staticmethod
    def get_base_xml():
        return '<?xml version="1.0" encoding="UTF-8"?>\n<node/>'

    def __str__(self):
        return f"CherryTreeNode(node_id={self.node_id},name=\"{self.name}\",icon={self.icon}" +\
               f",father_id={self.father_id},children={len(self.children)})"

    def __repr__(self):
        return f"CherryTreeNode(node_id={self.node_id},name=\"{self.name}\",icon={self.icon}" +\
               f",father_id={self.father_id},children={len(self.children)})"

    def extend(self, children):
        """Add a list of children to the current Node"""
        if not isinstance(children, list):
            raise ValueError("add_children method expect a list as parameter")
        self.children.extend(children)

    def add_text(self, text, attrib={}):
        """
        Add rich text to the node

        :param text: The text to add to the node
        :type text: str
        """
        richtext = CherryTreeRichtext.from_attributes(text, attrib).get_xml()
        self.xml.append(richtext)

    def add_image(self, image_name, position=-1):
        """
        Add an image to the text

        :param image_name: The name of the image to add
        :type image_name: str

        :param position: The position of the images in the text
        :type position: int (default: -1)
        """
        image = None
        with open(expanduser(image_name), "rb") as file_image:
            image = file_image.read()

        if not image:
            return

        if position < 0:
            # In this case, append the image at the end of the text
            position = self._get_text_length()

        self.images.append(CherryTreeImage(image, position=position))
        return self

    def _get_text_length(self):
        """
        Recover the length of the text inside the xml
        """
        length = 0
        for text in self.xml.itertext():
            length += len(text)
        return length

    def append(self, child):
        """Add a children to the list"""
        self.children.append(child)

    def get_all_children_recurse(self):
        """
        return the list of all children of the current node
        recursively, and include the root node as the first element
        """
        all_children = [self]
        for child in self.children:
            all_children.extend(child.get_all_children_recurse())
        return all_children

    def __iter__(self):
        """Iter through all child nodes"""
        for node in self.get_all_children_recurse():
            yield node

    @property
    def is_root_node(self):
        """Check if a node is the root node"""
        return self.father_id == 0

    @property
    def is_last_node(self):
        """Check if a node is the last one"""
        return len(self.children) == 0    

    @property
    def has_image(self):
        """
        Check if a node contains images or not

        :rtype: int
        """
        return 0 if len(self.images) == 0 else 1

    def get_xml(self):
        """Return the xml containing in the node which is xml by default"""
        if self.xml is None:
            return self.get_base_xml()
        return ET.tostring(self.xml, encoding="UTF-8", xml_declaration=True)



