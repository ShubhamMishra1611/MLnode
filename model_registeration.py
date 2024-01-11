import json
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
import os
import pandas as pd

class Node:
    def __init__(self, node_dict):
        self.title = node_dict['title']
        self.inputs = node_dict['inputs']
        self.outputs = node_dict['outputs']
        self.content = node_dict['content']

class Edge:
    def __init__(self, edge_dict):
        self.start = edge_dict['start']
        self.end = edge_dict['end']

class Graph:
    def __init__(self, structure):
        self.nodes = {}
        for node in structure['nodes']:
            # Only consider nodes with non-empty 'outputs' list
            if node['outputs']:
                self.nodes[node['outputs'][0]['id']] = Node(node) # this is assuming the fact that only one socket is there for output
        self.edges = [Edge(edge) for edge in structure['edges']]

class Model(nn.Module):
    def __init__(self, graph):
        super(Model, self).__init__()
        self.graph = graph
        self.layers = nn.ModuleDict()
        # self.layers = {}
        for node_id, node in self.graph.nodes.items():
            if node.title == 'nn.Linear':
                self.layers[str(node_id)] = nn.Linear(int(node.content['value_inchannel']), int(node.content['value_outchannel']))

    def forward(self, x):
        current_id = next(node_id for node_id, node in self.graph.nodes.items() if not node.inputs)
        try:
            while True:
                x = self.layers[current_id]
                next_edges = [edge for edge in self.graph.edges if edge.start == current_id]
                if not next_edges:  # No more edges, stop
                    break
                current_id = next_edges[0].end  # Follow the edge to the next node
            return x
        except Exception as e:
            print(e)

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
            return torch.from_numpy(series.values.astype('float32'))
        elif self.file_type == 'json':
            return torch.from_numpy(self.data[idx].astype('float32'))
        else:
            return None

if __name__ == '__main__':
    # Load the JSON data
    with open(r'deleted_files\nn_linear_model_register_data.json', 'r') as f:
    # with open(r'deleted_files\stuff_delete.json', 'r') as f:
        structure = json.load(f)

    # Create the graph and the model
    graph = Graph(structure)
    model = Model(graph)
    dataset = None
    for node_id, node in graph.nodes.items():
        if node.title == 'getdata':
            dataset = CustomDataset(node.content['value_file_name'])
            dataloader = DataLoader(dataset, batch_size=1, shuffle=True)

    print("printing the dataset")
    for (x, y) in enumerate(dataloader):
        print(x, y)
    print(model)

