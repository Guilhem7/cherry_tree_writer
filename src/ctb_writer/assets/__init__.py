"""
Gather some assets of the cherry tree doc
"""
import warnings
from .node_icon import icons

def get_icon(icon_name, read_only=False):
	"""
	Return the icon associated to a string

	:param icon_name: The name of the icon
	:type icon_name: Union[str, int]

	:param read_only: Whether or not to set the node as read_only
	:type read_only: boolean (default: False)

	:return: The value of the icon for cherry tree
	"""
	prefix_icon = "ct_"
	if isinstance(icon_name, int):
		value = icon_name
	else:
		if not icon_name.startswith(prefix_icon):
			icon_name = prefix_icon + icon_name
		value = icons.get(icon_name.lower())
		if not value:
			warnings.warn(f"Icon {icon_name} not found, refers to:\n"
						  "https://github.com/Guilhem7/cherry_tree_writer/blob/main/src/ctb_writer/assets/node_icon.py",
						  )
			value = 0

	if read_only:
		return value + 1
	return value

