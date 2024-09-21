"""
Link cherry tree instance to the database
"""
import sqlite3
import os
from time import time

class CherryTreeLink:
    def __init__(self, name):
        self.name = name
        if os.path.exists(self.name):
            raise ValueError(f"File {self.name} already exists, aborting") from None
        self.con = sqlite3.connect(self.name)
        self.cursor = self.con.cursor()
        self.init()

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, val):
        """
        Checks that the extension is a valid CherryTree one. On
        empty extensions, it will add '.ctb'

        :raises ValueError: If the extension is not .ctb and not empty
        """
        fname, ext = os.path.splitext(val)

        if ext == "":
            self._name = f"{val}.ctb"

        elif ext != ".ctb":
            raise ValueError(f"Extension {val} is not supported "
                             "for creating a cherry tree document")
        else:
            self._name = val

    def save(self, nodes):
        """
        Save a node to the database

        :param node: The node to save
        :type node: class:`CherryTreeNode`
        """
        self._save_children_recurse(nodes)
        self._save_node_recurse(nodes)

    def _save_images(self, node):
        """
        Save images of a node
        """
        for image in node.images:
            self.cursor.execute(
                            """INSERT INTO image
                            (node_id, offset, justification, png)
                            VALUES (?, ?, ?, ?)
                            """,
                            (node.node_id, image.position, "left", image.data)
                            )

    def _save_node_recurse(self, nodes):
        """
        Save the nodes recursively

        :param nodes: The list of nodes to save
        :type nodes: List[class:`CherryTreeNode`]
        """
        for node in nodes:
            if not node.is_last_node:
                self._save_node_recurse(node.children)
            self.cursor.execute(
                            """INSERT INTO node
                            (node_id,
                             name,
                             txt,
                             syntax,
                             tags,
                             is_ro,
                             is_richtxt,
                             has_codebox,
                             has_table,
                             has_image,
                             level,
                             ts_creation,
                             ts_lastsave)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                            """,
                            (node.node_id,
                             node.name,
                             node.get_xml(),
                             "custom-colors",
                             None,
                             node.icon | node.is_ro,
                             1,
                             0,
                             0,
                             node.has_image,
                             0,
                             int(time())-2,
                             int(time()))
                            )
            if node.has_image:
                self._save_images(node)
            self.con.commit()

    def _save_children_recurse(self, nodes):
        """
        Save the children of nodes recursively

        :param nodes: The list of nodes to save
        :type nodes: List[class:`CherryTreeNode`]
        """
        for seq, node in enumerate(nodes):
            self.cursor.execute(
                        """INSERT INTO children
                        (node_id, father_id, sequence, master_id)
                        VALUES (?, ?, ?, ?)
                        """,
                        (node.node_id, node.father_id, seq + 1, 0)
                        )
            self.con.commit()
            if not node.is_last_node:
                self._save_children_recurse(node.children)

    def init(self):
        """
        Init the document with the default tables and all
        """
        self.cursor.execute(
            """CREATE TABLE bookmark (
            node_id INTEGER UNIQUE,
            sequence INTEGER
            )
            """)

        self.cursor.execute(
            """CREATE TABLE children (
            node_id INTEGER UNIQUE,
            father_id INTEGER,
            sequence INTEGER,
            master_id INTEGER
            )
            """)

        self.cursor.execute(
            """CREATE TABLE codebox (
            node_id INTEGER,
            offset INTEGER,
            justification TEXT,
            txt TEXT,
            syntax TEXT,
            width INTEGER,
            height INTEGER,
            is_width_pix INTEGER,
            do_highl_bra INTEGER,
            do_show_linenum INTEGER
            )
            """
            )

        self.cursor.execute(
            """CREATE TABLE grid (
            node_id INTEGER,
            offset INTEGER,
            justification TEXT,
            txt TEXT,
            col_min INTEGER,
            col_max INTEGER
            )
            """
            )

        self.cursor.execute(
            """CREATE TABLE image (
            node_id INTEGER,
            offset INTEGER,
            justification TEXT,
            anchor TEXT,
            png BLOB,
            filename TEXT,
            link TEXT,
            time INTEGER
            )
            """)

        self.cursor.execute(
            """CREATE TABLE node (
            node_id INTEGER UNIQUE,
            name TEXT,
            txt TEXT,
            syntax TEXT,
            tags TEXT,
            is_ro INTEGER,
            is_richtxt INTEGER,
            has_codebox INTEGER,
            has_table INTEGER,
            has_image INTEGER,
            level INTEGER,
            ts_creation INTEGER,
            ts_lastsave INTEGER
            )
            """)

