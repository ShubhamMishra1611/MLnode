import json
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
import os
import pandas as pd
from utility import print_traceback 
import sys

DEBUG = False

class GraphNode:
    def __init__(self, node_dict):
        self.title = node_dict['title']
        self.inputs = node_dict['inputs']
        self.outputs = node_dict['outputs']
        self.content = node_dict['content']
        self.opcode = node_dict['op_code']


class GraphEdge:
    def __init__(self, edge_dict):
        self.start = edge_dict['start']
        self.end = edge_dict['end']

class Graph:
    def __init__(self, structure):
        self.nodes = {}
        for node in structure['nodes']:
            # Only consider nodes with non-empty 'outputs' list
            if node['outputs']: # TODO: this should not be output but should be input or id of node itself
                self.nodes[node['id']] = GraphNode(node) 
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

class Model(nn.Module):
    def __init__(self, graph):
        super(Model, self).__init__()
        self.graph = graph
        self.layers = nn.ModuleDict()
        for node_id, node in self.graph.nodes.items():
            if node.title == 'nn.Linear':
                self.layers[str(node_id)] = nn.Linear(int(node.content['value_inchannel']), int(node.content['value_outchannel']))

    def find_node(self, input_id, inputoroutput='input'):
        for nodeid, node in self.graph.nodes.items():
            if inputoroutput == 'input':
                if node.inputs[0]['id'] == input_id:
                    return nodeid
            elif inputoroutput == 'output':
                if node.outputs[0]['id'] == input_id:
                    return nodeid
        return None 
        
    
    def forward(self, x):
        # get the node that has not input node and is not getdata node
        current_id = None
        for node_id, node in self.graph.nodes.items():
            if node.opcode % 100 == 13:
                if DEBUG: print(f'node.title = {node.title}')
            # if node.title == 'getdata':
                continue
            if DEBUG: print(f'{node_id = }')
            parent_node = self.graph.getParentNode(node_id)
            if DEBUG: print(f'{parent_node = }')
            parentnodeid = self.find_node(self.graph.getParentNode(node_id), inputoroutput="output")
            if DEBUG: print(f'{parentnodeid = }')
            if parentnodeid is None: continue
            parent_node_title = self.graph.nodes[parentnodeid].title
            parent_node_opcode = self.graph.nodes[parentnodeid].opcode
            if DEBUG: print(f'{parent_node_title = }')
            if DEBUG: print(f'{parent_node_opcode = }')
            if parent_node_opcode // 100 == 13:
            # if parent_node_title == 'getdata':
                current_id = node_id
                break
        if DEBUG: print(f'{current_id = }')
        try:
            while True:
                x = self.layers[str(current_id)](x)
                next_edges = [edge for edge in self.graph.edges if edge.start == self.graph.nodes[current_id].outputs[0]['id']]
                if not next_edges: break # No more edges, stop
                current_id = self.find_node(next_edges[0].end)
                if current_id is None: break
            return x
        except Exception as e:
            print_traceback(e)


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
            x = torch.from_numpy(series.values[:-1].astype('float32'))
            y = torch.from_numpy(series.values[-1:].astype('float32'))
            return x, y
        elif self.file_type == 'json':
            return torch.from_numpy(self.data[idx].astype('float32'))
        else:
            return None

class training_module:
    def __init__(self, model, dataset, optimizer, loss_fn):
        self.model = model
        self.dataset = dataset
        self.optimizer = optimizer
        self.loss_fn = loss_fn

    def train(self, epochs):
        for epoch in range(epochs):
            for i, (x, y) in enumerate(self.dataset):
                y_pred = self.model(x)
                loss = self.loss_fn(y_pred, y)
                print(f'Epoch {epoch + 1} | Batch: {i+1} | Loss: {loss.item():.4f}')
                self.optimizer.zero_grad()
                loss.backward()
                self.optimizer.step()

        # save the model to disk
        torch.save(self.model.state_dict(), 'model.pth')
        print(f'Final loss: {loss.item():.4f}')
        print(f'Training complete. Model saved to: model.pth')

if __name__ == '__main__':
    # Load the JSON data
    with open(r'samples\training_test.json', 'r') as f:
        structure = json.load(f)

    # Create the graph and the model
    graph = Graph(structure)
    model = Model(graph)
    dataset = None
    for node_id, node in graph.nodes.items():
        if node.title == 'getdata':
            dataset = CustomDataset(node.content['value_file_name'])
            dataloader = DataLoader(dataset, batch_size=1, shuffle=True)

    # for (x, y) in enumerate(dataloader):
    #     print(x, y)
    print(f'{model = }')
    dataset = CustomDataset('deleted_files/fake_data.csv')
    dataloader = DataLoader(dataset, batch_size=3, shuffle=True)
    # train the model
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-5)
    loss_fn = nn.MSELoss()
    trainer = training_module(model, dataloader, optimizer, loss_fn)
    trainer.train(epochs=100)

