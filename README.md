# Cherrytree Writer
Simple library to write a **Cherrytree** document

## Usage
```python
import os
from ctb_writer import CherryTree, CherryTreeNodeBuilder as NodeBuilder

if os.path.exists("my_notes.ctb"):
    print("The file <my_notes.ctb> already exists")
    exit(0)

ctb_document = CherryTree("my_notes.ctb") # Init the cherry tree document
root_id = ctb_document.add_child("Root node") # Add a node with a name

ctb_document.add_child("child node1", parent_id=root_id) # Add a child to the root node
ctb_document.add_child("Root node 2", text="Content of this node", icon="plus") # Add another root node, with some meta_infos

# Can also use .image("path_to_image")
new_node = NodeBuilder("New node").icon("execute")\
                                  .text("Content of the node\n")\
                                  .text("Text append to the node again")\
                                  .get_node() # build the node from the previous infos

# Add node with formatting
other_node = NodeBuilder("Other node", color='#fg4895', bold=True)\
                                                    .text("", style={"bold":True, "fg":"#fg4895","bg": "#ffffff"})\
                                                    .get_node()

ctb_document.add_child(new_node, parent_id=root_id) # Add this node as the child of the first root node
ctb_document.add_child(other_node, parent_id=new_node)
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

## Colors
By now colors can be applied on text and on node title.
However, each colors must match the following regex:
```
#[0-9a-fA-F]{6}
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
3. Manage text formatting | Done
4. Add alias for color

