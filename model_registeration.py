import json
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from MLnode_conf import *
import logging
from obj_mapping import obj_map
import os
import pandas as pd
from utility import print_traceback 
import sys

DEBUG = False

logging.basicConfig(level=logging.WARNING, format=':%(message)s')

logger = logging.getLogger(__name__)

class GraphNode:
    def __init__(self, node_dict):
        self.id = node_dict['id']
        self.title = node_dict['title']
        self.inputs = node_dict['inputs']
        self.outputs = node_dict['outputs']
        self.content = node_dict['content']
        self.opcode = node_dict['op_code']
        
        self.value = None
        self.evaluated = False


class GraphEdge:
    def __init__(self, edge_dict):
        self.start = edge_dict['start']
        self.end = edge_dict['end']

class Graph:
    def __init__(self, structure):
        self.nodes = {}
        self.start_node = None
        self.end_node = None

        ignore_nodes = [
            'tensor_info'
        ]

        for node in structure['nodes']:
            if node['title'] == 'getdata':
                self.start_node = node['id']
            if node['title'] == 'Output Tensor':
                self.end_node = node['id']
            if node['outputs']:
                if node['title'] not in ignore_nodes:
                    self.nodes[node['id']] = GraphNode(node)

        # for node in structure['nodes']:
        #     # Only consider nodes with non-empty 'outputs' list
        #     if node['outputs']: # TODO: this should not be output but should be input or id of node itself
        #         self.nodes[node['id']] = GraphNode(node) 
        self.edges = [GraphEdge(edge) for edge in structure['edges']]

    def __str__(self):
        return f'{self.nodes = }\n{self.edges = }'
    
    def getParentNode(self, node_id):
        p_id = None
        try:
            for edge in self.edges:
                if edge.end == self.nodes[node_id].inputs[0]['id']:
                    return edge.start
            return None
        except IndexError as e:
            print_traceback(e)
            return None
    
    def getParentNodes(self, node_id):
        input_ids = [x['id'] for x in self.nodes[node_id].inputs]
        parents = []
        for edge in self.edges:
            if edge.end in input_ids:
                parents.append(edge.start)
            # if edge.end == self.nodes[node_id].inputs[0]['id']:
            #     parents.append(edge.start)
        return parents
        
    def getChildrenNodes(self, node_id):
        children = []
        for edge in self.edges:
            if edge.start == self.nodes[node_id].outputs[0]['id']:
                children.append(edge.end)
        return children

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


class CustomDataset(Dataset):
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = self.load_data()
        self.file_type = self.file_path.split('.')[-1]

    def load_data(self):
        if self.file_path.endswith('csv'):
            return pd.read_csv(self.file_path)
        else:
            return None
        
    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, idx):
        if self.file_type == 'csv':
            series = self.data.iloc[idx]
            x = torch.from_numpy(series.values[:len(series)//2].astype('float32'))
            y = torch.from_numpy(series.values[len(series)//2:].astype('float32'))
            # y = torch.from_numpy(series.values[-1:].astype('float32'))
            return x, y
        elif self.file_type == 'json':
            return torch.from_numpy(self.data[idx].astype('float32'))
        else:
            return None

class training_module:
    def __init__(self, model, dataset, optimizer, loss_fn):
        self.model = model
        self.dataset = dataset
        self.optimizer = torch.optim.Adam(model.parameters(), lr=1e-4)
        self.loss_fn = nn.MSELoss()

    def train(self, epochs):
        for epoch in range(epochs):
            for i, (x, y) in enumerate(self.dataset):
                y_pred = self.model(x)
                loss = self.loss_fn(y_pred, y)
                self.optimizer.zero_grad()
                loss.backward()
                self.optimizer.step()
            print(f'Epoch {epoch + 1} | Batch: {i+1} | Loss: {loss.item():.4f}')

        # save the model to disk
        torch.save(self.model.state_dict(), 'model.pth')
        print(f'Final loss: {loss.item():.4f}')
        print(f'Training complete. Model saved to: model.pth')

if __name__ == '__main__':
    # Load the JSON data
    with open(r'samples\testing_inv_model.json', 'r') as f:
        structure = json.load(f)

    # Create the graph and the model
    graph = Graph(structure)
    model = Model(graph)
    dataset = None
    for node_id, node in graph.nodes.items():
        if node.title == 'getdata':
            dataset = CustomDataset(node.content['value_file_name'])
            dataloader = DataLoader(dataset, batch_size=1, shuffle=True)

    optimizer = torch.optim.Adam(model.parameters(), lr=1e-4)
    loss_fn = nn.MSELoss()
    trainer = training_module(model, dataloader, optimizer, loss_fn)
    trainer.train(epochs=10)

