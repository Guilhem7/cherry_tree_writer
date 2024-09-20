"""
Gather some assets of the cherry tree doc
"""
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
	if isinstance(icon_name, int):
		return icon_name
	return icons.get(icon_name.lower(), 0)
