from MLnode_conf import *
from MLnode_node_base import *
from PyQt5.QtCore import *
from utility import print_traceback


@register_node(OP_NODE_ADD)
class MLNode_Add(MLnode_node):
    icon = "icons/add.png"
    op_code = OP_NODE_ADD
    op_title = "Matrix Addition"
    content_label = "+"
    content_label_objname = "mlnode_node_bg"

@register_node(OP_NODE_MATMUL)
class MLNode_Matmul(MLnode_node):
    icon = "icons/matmul.png"
    op_code = OP_NODE_MATMUL
    op_title = "Matrix Multiplication"
    content_label = "X"
    content_label_objname = "mlnode_node_mul"

@register_node(OP_NODE_TRANSPOSE)
class MLNode_Transpose(MLnode_node):
    icon = "icons/transpose.png"
    op_code = OP_NODE_TRANSPOSE
    op_title = "Matrix Transpose"
    content_label = "X"
    content_label_objname = "mlnode_node_transpose"

    def __init__(self, scene):
        super().__init__(scene, inputs=[1], outputs=[1])

@register_node(OP_NODE_SCALAR)
class MLNode_Scalar(MLnode_node):
    icon = "icons/scalar.png"
    op_code = OP_NODE_SCALAR
    op_title = "Scalar"
    content_label = "1"
    content_label_objname = "mlnode_node_scalar"
    
    def __init__(self, scene):
        super().__init__(scene, inputs=[1], outputs=[1])