import torch
import torch.nn as nn
import torch.optim as optim
from MLnode_conf import *
import sys
import logging
import time
logging.basicConfig(level=logging.WARNING, format=':%(message)s')

logger = logging.getLogger(__name__)

obj_map = {
    1200: nn.Linear,
    1201: nn.Conv2d,
    1500: nn.ReLU,
}


################## Rough ##################
# from model_registeration import Graph, GraphEdge, GraphNode

# def conv_to_type(value, type_):
#     try:
#         return eval(f'{type_}({value})')
#     except (ValueError, TypeError) as e:
#         raise TypeError(f'Error converting to {type_}: {e}')

def conv_to_type(value, type_):
    type_mapping = {
        'int': int,
        'float': float,
        'str': str,
        'bool': bool,
    }

    if type_ in type_mapping:
        return type_mapping[type_](value)
    else:
        raise TypeError(f'Unknown type: {type_}')

class Model(nn.Module):
    def __init__(self, graph):
        super(Model, self).__init__()
        self.graph = graph
        self.layers = nn.ModuleDict()
        for node_id, node in self.graph.nodes.items():
            obj = obj_map[node.opcode] if node.opcode in obj_map.keys() else None
            if obj is not None:
                content = node.content
                content_safe = {x: conv_to_type(*y) for x, y in content.items()}
                self.layers[str(node_id)] = obj_map[node.opcode](**content_safe)

    def topological_sort(self):
        visited = set()
        result = []

        def dfs(node_id):
            visited.add(node_id)
            children_nodes = self.graph.getChildrenNodes(node_id)

            for child_node in children_nodes:
                child_id = self.find_node(child_node)
                if child_id is None:
                    continue# TODO: child node is returned as None
                node = self.graph.nodes[child_id]
                if node not in visited:
                    dfs(node.id)

            result.append(node_id)

        for node_id in self.graph.nodes.keys():
            if node_id not in visited:
                dfs(node_id)

        return result[::-1]
    
    def find_node(self, input_id, inputoroutput='input'):
        for nodeid, node in self.graph.nodes.items():
            if inputoroutput == 'input':
                for i in range(len(node.inputs)):
                    if node.inputs[i]['id'] == input_id:
                        return nodeid
            elif inputoroutput == 'output':
                for i in range(len(node.outputs)):
                    if node.outputs[i]['id'] == input_id:
                        return nodeid
        return None 
    
    def reset_node_eval_and_value(self):
        for node in self.graph.nodes.values():
            node.evaluated = False
            node.value = None

    def forward(self, x):
        self.reset_node_eval_and_value()
        sorted_node_id = self.topological_sort()
        sorted_node_dic = {x:x for x in sorted_node_id}
        sorted_node_id_no_rep = list(sorted_node_dic.keys())
        logger.info(f'Sorted Node ID: {sorted_node_id},\nsorted_node_id_no_rep:{sorted_node_id_no_rep}\nlen: {len(sorted_node_id)}')
        
        current_node_id = sorted_node_id[0]
        if self.graph.nodes[current_node_id].title == 'getdata':
            self.graph.nodes[current_node_id].value = x
            self.graph.nodes[current_node_id].evaluated = True
        Nodes = self.graph.nodes
        depth = 0
        while current_node_id != self.graph.end_node:
            if depth >= len(sorted_node_id):
                logger.info(f'Breaking at depth {depth} as sorted nodes have ended')
                break
            current_node_id = sorted_node_id[depth]
            current_node = self.graph.nodes[current_node_id]
            logger.info(f'[INFO]::ID: {current_node.id} Current Node: {current_node.title} depth:{depth} Evaluated: {current_node.evaluated}')
            if str(current_node_id) in self.layers.keys():
                if not self.graph.nodes[current_node_id].evaluated:
                    parents = self.graph.getParentNodes(current_node_id)
                    # NOTE: for any nn node the parent node will be singleton list
                    parent_node_id = self.find_node(parents[0], inputoroutput='output')
                    parent_value = Nodes[parent_node_id].value
                    if parent_value is not None:
                        self.graph.nodes[current_node_id].value = self.layers[str(current_node_id)](parent_value)
                        x = self.graph.nodes[current_node_id].value
                        self.graph.nodes[current_node_id].evaluated = True
            else:
                if not self.graph.nodes[current_node_id].evaluated:
                    parent_nodes = self.graph.getParentNodes(current_node_id)
                    #NOTE: for general node the parent nodes need not to be singleton list
                    parent_values = []
                    for parent_node in parent_nodes:
                        parent_id = self.find_node(parent_node, inputoroutput='output')
                        parent_values.append(Nodes[parent_id].value)
                    if all([x is not None for x in parent_values]):
                        req_class = get_class_from_opcode(self.graph.nodes[current_node_id].opcode)
                        x = req_class.evalMethod(*parent_values)
                        self.graph.nodes[current_node_id].value = x
                        self.graph.nodes[current_node_id].evaluated = True
            depth += 1
        return x

    def eval_node(self, node):
        parents = self.graph.getParentNodes(node)
        values = []
        for parent in parents:
            parent_id = self.find_node(parent)
            values.append(self.graph.nodes[parent_id].value if self.graph.nodes[parent_id].value is not None else self.eval_node(parent_id)) #TODO: this line could contain a lot of bugs
        req_class = get_class_from_opcode(self.graph.nodes[node].opcode)
        value = req_class.evalMethod(*values)
        self.graph.nodes[node].value = value
        self.graph.nodes[node].evaluated = True
        return value
    
# from torch.utils.data import Dataset, DataLoader

# class seqof_dataset(Dataset):
#   def __init__(self, num_samples = 1000, seq_len = 10):
#     self.num_samples = num_samples
#     self.seq_len = seq_len
#     self.data = torch.randint(1, 10, (num_samples,  seq_len))
#     self.dum = 2 * self.data + 1
#     self.targets = torch.flip(self.dum, [1])

#   def __len__(self):
#     return self.num_samples

#   def __getitem__(self, idx):
#     return self.data[idx], self.targets[idx]


# test_data =  seqof_dataset(10, 10)
# dataloader = DataLoader(test_data, batch_size=1, shuffle=True)

# for _, (x, y) in enumerate(dataloader):
#   print(f'{x = }')
#   print(f'{y = }')

if __name__ == '__main__':
    import json
    with open(r'samples\some_model.json', 'r') as f:
        structure = json.load(f)

    # Create the graph and the model
    graph = Graph(structure)
    model = Model(graph)

    # look if all var have req_grad as True
    # for param in model.parameters():
    #     print(param.requires_grad) 

    logger.info(f'{graph = }')
    logger.info(f'{model = }')

    random_tensor = torch.randn(10)
    output = model(random_tensor)
    logger.info(f'{output = }')

    print("*"*100)
        
    num_epochs = 4000
    learning_rate = 0.0001

    # Create the dataset and dataloader
    dataset = seqof_dataset(10, 10)
    dataloader = DataLoader(dataset, batch_size=32, shuffle=True)

    # training loop
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)
    for epoch in range(num_epochs):
        for i, (seq, tar) in enumerate(dataloader):
            outputs = model(seq.float())
            loss = criterion(outputs, tar.float())
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            print(f'Epoch {epoch}/{num_epochs}, Loss: {loss.item()}')
            
    # get the output of the model
    for seq, tar in dataloader:
        outputs = model(seq.float())
        print(f'{seq = }')
        print(f'{tar = }')
        print(f'{outputs = }')
        break
