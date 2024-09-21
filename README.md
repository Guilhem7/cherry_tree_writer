# Cherrytree Writer
Simple library to write a **Cherrytree** document

## Usage
```python
from ctb_writer import CherryTree, CherryTreeNodeBuilder

ctb_document = CherryTree("my_notes.ctb") # Init the cherry tree document
root_id = ctb_document.add_child("Root node") # Add a node with a name

ctb_document.add_child("child node1", parent_id=root_id) # Add a child to the root node
ctb_document.add_child("Root node 2", text="Content of this node", icon="plus") # Add another root node, with some meta_infos

# Can also use .image("path_to_image")
new_node = CherryTreeNodeBuilder("New node").icon("execute")\
                                            .text("Content of the node\n")\
                                            .text("Text append to the node again")\
                                            .get_node() # build the node from the previous infos

ctb_document.add_child(new_node, parent_id=root_id) # Add this node as the child of the first root node
ctb_document.save() # Save your CherryTree in "my_notes.ctb"

```

## Installation
```bash
git clone https://github.com/Guilhem7/cherry_tree_writer.git
cd cherry_tree_writer
pip3 install .
```

## Icons
List icons
```bash
python3 -m ctb_writer.assets 
```

## Other properties
**Nodes** can be created with the following properties:
 - Icon: The icon to use for the node (with or without the prefix **_ct__**)
 - Text: The text inside the node (no formatting available by now)
 - Images: The images inside the node
 - Read-Only: Whether or not the node can be edited

## TODO
1. Manage codebox
2. Manage Tables
3. Manage text formatting

