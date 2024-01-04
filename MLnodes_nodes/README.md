# Adding a New Node

Follow these steps to add a new node:

1. **Register the Node**: Register the new node and its opcode in the [`MLnode_conf.py`](https://github.com/ShubhamMishra1611/MLnode/blob/898a2a794ac8b970090046d4a2d15dbacc407a42/MLnode_conf.py#L3) file located in the main directory.

2. **Identify the File**: Check if the new node can be added to any of the existing Python files. If not, create a new Python file.

3. **Inherit from Parent Classes**: Ensure that the new node inherits from the appropriate parent classes. If the new node has a graphics class, it should inherit from the [`MLnode_graphicNode`](https://github.com/ShubhamMishra1611/MLnode/blob/898a2a794ac8b970090046d4a2d15dbacc407a42/MLnode_node_base.py#L11) class. The `node_content` should inherit from the [`QNode_content_widget`](https://github.com/ShubhamMishra1611/MLnode/blob/898a2a794ac8b970090046d4a2d15dbacc407a42/node_content_widget.py#L10) class. Check if the `serialize` and `deserialize` methods need to be overridden.

4. **Add the New Node**: Add the new node using the `@register_node` decorator on the new node class. This class should inherit from the [`MLnode_node`](https://github.com/ShubhamMishra1611/MLnode/blob/898a2a794ac8b970090046d4a2d15dbacc407a42/MLnode_node_base.py#L51) class. Override the constructor, `evalImplementation()` methods, and any other necessary methods as required.