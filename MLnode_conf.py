LISTBOX_MIMETYPE = "application/x-item"

OP_NODE_INPUT = 1
OP_NODE_OUTPUT = 2
OP_NODE_ADD = 3
OP_NODE_MATMUL = 4
OP_NODE_TRANSPOSE = 5
OP_NODE_SCALAR = 6


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
