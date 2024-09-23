"""
This class allows to create a new CherryTree and manipulate it
"""
import xml.etree.ElementTree as ET
from .cherry_tree_node import CherryTreeNode, _CherryTreeNodeBase
from .cherry_tree_link import CherryTreeLink
from .icons import get_icon

class CherryTree:
    """
    Create a cherryTree
    """
    def __init__(self, name):
        self.nodes = []
        self.ctb_sql_link = CherryTreeLink(name)
        self.last_id = 0

    def __str__(self):
        return f"<{self.__class__.__name__}: {len(self.nodes)} children>"

    def get_node_by_id(self, node_id):
        """
        Recover a node by its id
        """
        for node in self._get_all_nodes():
            if node.node_id == node_id:
                return node
        return None

    def _get_all_nodes_recurse(self, nodes):
        """
        Return all the nodes present
        """
        all_nodes = []
        for node in nodes:
            if not node.is_last_node:
                all_nodes.extend(self._get_all_nodes_recurse(node.children))
            all_nodes.append(node)
        return all_nodes

    def _get_all_nodes(self):
        """
        Return all the nodes in a list
        """
        return self._get_all_nodes_recurse(self.nodes)

    def get_new_id(self):
        """
        Return a new id for a node, by incrementing the last one found
        """
        if not self.nodes:
            return 1
        max_node = max(self._get_all_nodes(), key = lambda node: node.node_id)
        return max_node.node_id + 1

    def _add_child_node(self, node, parent_id):
        """
        Add a child node

        :param parent_id: The parent_id on which to add the child
        :type parent_id: int

        :param node: The node to add
        :type node: class:`_CherryTreeNodeBase`
        """
        new_node_id = self.get_new_id()
        if not new_node_id:
            raise ValueError(f"Cannot find a new id")
        node.node_id = new_node_id
        if parent_id == 0:
            self.nodes.append(node)
        else:
            node.father_id = parent_id
            node_res = self.get_node_by_id(parent_id)
            node_res.append(node)
        return node.node_id

    def add_child(self, node, text="", icon="", is_ro=0, parent_id=0):
        """
        Add a child to the parent

        :param parent_id: The parent_id on which to add the child
        :type parent_id: int

        :param node: The node created
        :type node: class:`_CherryTreeNodeBase`

        :return: The id of the node added
        """
        node_id = self.get_new_id()
        if isinstance(node, _CherryTreeNodeBase):
            return self._add_child_node(node, parent_id)

        elif isinstance(node, str):
            new_node = CherryTreeNode(node, is_ro=is_ro, father_id=parent_id)
            if text:
                new_node.add_text(text)

            if icon != "":
                new_node.icon = get_icon(icon)

            return self._add_child_node(new_node, parent_id)

        raise ValueError(f"Cannot insert node with type {type(node)}")

    def save(self):
        """
        Save the nodes to a cherrytree file
        """
        self.ctb_sql_link.save(self.nodes)
