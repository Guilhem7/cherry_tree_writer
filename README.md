# Cherrytree Writer
Simple library to **Create**, **Read** or **Update** a **Cherrytree** document

## Usage
```python
import os
from ctb_writer import CherryTree, CherryTreeNodeBuilder as NodeBuilder

if os.path.exists("my_notes.ctb"):
    print("The file <my_notes.ctb> already exists")
    exit(0)

ctb_document = CherryTree() # Init the cherry tree document
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
                                                    .text("Highlited text\n", style={"bold":True, "fg":"darkorange","bg": "#ffffff"})\
                                                    .get_node()

ctb_document.add_child(new_node, parent_id=root_id) # Add this node as the child of the first root node
ctb_document.add_child(other_node, parent_id=new_node)
ctb_document.save("my_notes.ctb") # Save your CherryTree in "my_notes.ctb"

```

It is also possible to add other type of nodes:
```python
from ctb_writer import CherryTree, CherryTreeNodeBuilder as NodeBuilder

ctb_document = CherryTree() # Init the cherry tree document
root_id = ctb_document.add_child("Root node") # Add a node with a name

python_code = NodeBuilder("script", type="code", syntax="python", color="goldenrod")\
                         .icon("python")\
                         .text("print('I am a python code')\n")\
                         .get_node()

ctb_document.add_child(python_code, parent_id=root_id)
ctb_document.save("my_notes.ctb")
```

Load an existing document
```python
from ctb_writer import CherryTree

ctb_document = CherryTree.load("my_notes.ctb")
# Change a text in a node
node = ctb_document.get_node_by_id(3)
node.replace("Content", "CONTENT", {"bold": True}) # Set a part of the text node to bold
```

## Add other items and text beautified
```python
from ctb_writer import CherryTree, CherryTreeNodeBuilder as NodeBuilder

ctb_document = CherryTree() # Init the cherry tree document
root_id = ctb_document.add_child("Root node") # Add a node with a name

# Tables in cherry tree contain HEADER at the END of a table
table = [["Content1", "C2"], ["Content2", "C3"], ["Col1", "Col2"]]

# Add codebox, local images or table
other_node = CherryTreeNodeBuilder("New node", bold=True, color='darkorange').icon("python")\
                                   .text("tests\n", style={"underline": True, "size":"h1"})\
                                   .codebox("import os\nprint('test')\n", syntax='python')\
                                   .image("images/ghost.png", justification="center")\
                                   .table(content=table)\
                                   .get_node()

# Add text that will be formatted
text_content = """
[(bold|underline)]Title:[/]
 - [(fg:orange)]orange[/]
 - [(bg:sun)]yellow background[/]
 - [(fg:blue|underline)]blue underlined[/]

[(bg:sun|fg:orange)]##############################################################################################[/]

"""

text_colored_node = CherryTreeNodeBuilder("Colored node").texts(text_content).get_node()

ctb_document.add_child(other_node, parent_id=root_id)
ctb_document.save("my_notes.ctb")
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
python3 -m ctb_writer.icons 
```

## Colors
By now colors can be applied on text and on node title.
However, each colors must match the following regex:
```
#[0-9a-fA-F]{6}
```

Or be a predefined style:
```bash
python3 -m ctb_writer.styles
```


## Other properties
**Nodes** can be created with the following properties:
 - Icon: The icon to use for the node (with or without the prefix **_ct__**)
 - Text: The text inside the node (no formatting available by now)
 - Images: The images inside the node
 - Read-Only: Whether or not the node can be edited

## TODO
1. :white_check_mark: Manage codebox
2. :white_check_mark: Manage Tables
3. :white_check_mark: Manage text formatting
4. :white_check_mark: Add alias for color
5. :white_check_mark: Parse an existing Cherry tree document
6. Allows to save with password
7. :white_check_mark: Add an easiest way to prettify text
