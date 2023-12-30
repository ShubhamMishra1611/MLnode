from MLnode_conf import *
from MLnode_node_base import *

@register_node(OP_NODE_ADD)
class MLNode_Add(MLnode_node):
    def __init__(self, scene):
        super().__init__(scene, OP_NODE_ADD, "Matrix Addition", "+")

@register_node(OP_NODE_MATMUL)
class MLNode_Matmul(MLnode_node):
    def __init__(self, scene):
        super().__init__(scene, OP_NODE_MATMUL, "Mat-Multiplication", "X")

@register_node(OP_NODE_TRANSPOSE)
class MLNode_Transpose(MLnode_node):
    def __init__(self, scene):
        super().__init__(scene, OP_NODE_TRANSPOSE, "Transpose", "T")

@register_node(OP_NODE_SCALAR)
class MLNode_Scalar(MLnode_node):
    def __init__(self, scene):
        super().__init__(scene, OP_NODE_SCALAR, "Scalar", "1", inputs=[1], outputs=[1])

@register_node(OP_NODE_INPUT)
class MLNode_Input(MLnode_node):
    def __init__(self, scene):
        super().__init__(scene, OP_NODE_INPUT, "Tensor Input", inputs=[], outputs=[3])

@register_node(OP_NODE_OUTPUT)
class MLNode_Output(MLnode_node):
    def __init__(self, scene):
        super().__init__(scene, OP_NODE_OUTPUT, "Output", inputs=[1], outputs=[])

