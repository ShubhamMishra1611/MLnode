LISTBOX_MIMETYPE = "application/x-item"

#RULES: 
#      Each opcode must be unique and must be a 4 digit number. The first two digit is the type of the node. All nodes with same first digit are in same python file.
#      The rest of the digits are unique for each node. The number is not important, only that it is unique.
#      Any opcode cannot be less than 1000

OP_NODE_INPUT_ONES = 1000
OP_NODE_INPUT_EYE = 1001
OP_NODE_INPUT_ARANGE = 1002

OP_NODE_TENSOR_INFO = 1100

OP_NODE_NN_LINEAR = 1200
OP_NODE_NN_CONV2D = 1201

OP_NODE_GETDATA = 1300
OP_NODE_GETIMGDATA = 1301
OP_NODE_GETXYDATA = 1302

OP_NODE_TRAINING = 1400

OP_NODE_ACTIVATION = 1500

OP_NODE_OUTPUT = 2000

OP_NODE_ADD = 3000
OP_NODE_MATMUL = 3001
OP_NODE_TRANSPOSE = 3002
OP_NODE_SCALAR = 3003
OP_NODE_RESHAPE = 3004
OP_NODE_FLATTEN = 3005
OP_NODE_NORMALIZATION = 3006
OP_NODE_CLIPPING = 3007
OP_NODE_CHANGEDTYPE = 3008

OP_NODE_TRIG = 7000








MLNODE_NODES = {
}


class ConfException(Exception): pass
class InvalidNodeRegistration(ConfException): pass
class OpCodeNotRegistered(ConfException): pass


def register_node_now(op_code, class_reference):
    if op_code in MLNODE_NODES:
        raise InvalidNodeRegistration("Duplicite node registration of '%s'. There is already %s" %(
            op_code, MLNODE_NODES[op_code]
        ))
    MLNODE_NODES[op_code] = class_reference


def register_node(op_code):
    def decorator(original_class):
        register_node_now(op_code, original_class)
        return original_class
    return decorator

def get_class_from_opcode(op_code):
    if op_code not in MLNODE_NODES: raise OpCodeNotRegistered("OpCode '%d' is not registered" % op_code)
    return MLNODE_NODES[op_code]


from MLnodes_nodes import *
