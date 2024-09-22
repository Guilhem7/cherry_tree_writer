"""
This file allows to add beautify text to cherrytree
"""
import xml.etree.ElementTree as ET
import re
from ctb_writer.styles import styles


COLOR_RE = re.compile(r"#[0-9a-f]{6}", re.I)

def color(func):
    """
    Check that args given is a color
    """
    def check_color(color):
        if re.match(COLOR_RE, color):
            return True
        raise ValueError("A color with the format '#af45df' is expected") from None

    def wrapper_is_color(*args, **kwargs):
        new_args = []
        for i, arg in enumerate(args):
            if isinstance(arg, bytes):
                arg = arg.decode()

            if isinstance(arg, str):
                resolved_color = styles.get(arg.lower())
                if resolved_color:
                    arg = resolved_color
                else:
                    check_color(arg)

            new_args.append(arg)


        for key, arg in kwargs.items():
            if isinstance(arg, bytes):
                arg = arg.decode()

            if isinstance(arg, str):
                resolved_color = styles.get(arg.lower())
                if resolved_color:
                    kwargs[i] = resolved_color
                else:
                    check_color(arg)

        return func(*new_args, **kwargs)
    return wrapper_is_color


class CherryTreeRichtext:
    """
    Class allowing some operations on text, such as:
     - Adding bold
     - Colors
     - Other style
    """
    def __init__(self, text, bold=False, fg=None, bg=None):
        self.text = text
        self.bold = bold
        self.fg = fg
        self.bg = bg

    @property
    def fg(self):
        return self._fg

    @fg.setter
    @color
    def fg(self, color):
        """
        Check if the value given is a color

        :raises ValueError: If colors does not match a regex

        :param color: The color to check
        :type color: str
        """
        self._fg = color

    @property
    def bg(self):
        return self._bg

    @bg.setter
    @color
    def bg(self, color):
        """
        Check if the value given is a color
        """
        self._bg = color

    def get_xml(self):
        """
        Get the text on cherry tree format
        """
        text_attributes = {}
        if self.bold:
            text_attributes["weight"] = "heavy"

        if self.fg:
            text_attributes["foreground"] = self.fg

        if self.bg:
            text_attributes["background"] = self.bg

        richtext = ET.Element("rich_text", attrib=text_attributes)
        richtext.text = self.text
        return richtext

    @classmethod
    def from_attributes(cls, text, attributes):
        """
        Build a class instance from the attributes

        :param text: The text to use
        :type text: str

        :param attributes: The attributes for the text style
        :type attributes: Dict[str, str]
        """
        return cls(text,
                   bold=attributes.get("bold", False),
                   fg=attributes.get("fg"),
                   bg=attributes.get("bg"))
