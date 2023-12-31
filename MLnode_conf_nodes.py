from MLnode_conf import *
from MLnode_node_base import *

@register_node(OP_NODE_ADD)
class MLNode_Add(MLnode_node):
    # def __init__(self, scene):
        # super().__init__(scene, OP_NODE_ADD, "Matrix Addition", "+")
    icon = "icons/add.png"
    op_code = OP_NODE_ADD
    op_title = "Matrix Addition"
    content_label = "+"

@register_node(OP_NODE_MATMUL)
class MLNode_Matmul(MLnode_node):
    # def __init__(self, scene):
    #     super().__init__(scene, OP_NODE_MATMUL, "Mat-Multiplication", "X")
    icon = "icons/matmul.png"
    op_code = OP_NODE_MATMUL
    op_title = "Matrix Multiplication"
    content_label = "X"

@register_node(OP_NODE_TRANSPOSE)
class MLNode_Transpose(MLnode_node):
    # def __init__(self, scene):
    #     super().__init__(scene, OP_NODE_TRANSPOSE, "Transpose", "T", inputs=[1], outputs=[1])
    icon = "icons/transpose.png"
    op_code = OP_NODE_TRANSPOSE
    op_title = "Matrix Transpose"
    content_label = "X"

@register_node(OP_NODE_SCALAR)
class MLNode_Scalar(MLnode_node):
    # def __init__(self, scene):
    #     super().__init__(scene, OP_NODE_SCALAR, "Scalar", "1", inputs=[1], outputs=[1])
    icon = "icons/scalar.png"
    op_code = OP_NODE_SCALAR
    op_title = "Scalar"
    content_label = "1"

@register_node(OP_NODE_INPUT)
class MLNode_Input(MLnode_node):
    icon = "icons/tensorinput.png"
    op_code = OP_NODE_INPUT
    op_title = "Input Tensor"
    def __init__(self, scene):
        super().__init__(scene, inputs=[], outputs=[3])

@register_node(OP_NODE_OUTPUT)
class MLNode_Output(MLnode_node):
    icon = "icons/tensoroutput.png"
    op_code = OP_NODE_INPUT
    op_title = "Output Tensor"
    def __init__(self, scene):
        super().__init__(scene, inputs=[1], outputs=[])

