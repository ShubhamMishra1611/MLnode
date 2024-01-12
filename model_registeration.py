import json
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
import os
import pandas as pd
from utility import print_traceback 

class GraphNode:
    def __init__(self, node_dict):
        self.title = node_dict['title']
        self.inputs = node_dict['inputs']
        self.outputs = node_dict['outputs']
        self.content = node_dict['content']


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
                # self.nodes[node['outputs'][0]['id']] = GraphNode(node) # this is assuming the fact that only one socket is there for output
                self.nodes[node['id']] = GraphNode(node) 
        self.edges = [GraphEdge(edge) for edge in structure['edges']]

    def __str__(self):
        return f'{self.nodes = }\n{self.edges = }'
    
    def getParentNode(self, node_id):
        for edge in self.edges:
            if edge.end == self.nodes[node_id].inputs[0]['id']:
                return edge.start
        return None

class Model(nn.Module):
    def __init__(self, graph):
        super(Model, self).__init__()
        self.graph = graph
        self.layers = nn.ModuleDict()
        for node_id, node in self.graph.nodes.items():
            if node.title == 'nn.Linear':
                self.layers[str(node_id)] = nn.Linear(int(node.content['value_inchannel']), int(node.content['value_outchannel']))

    def find_node(self, input_id):
        for nodeid, node in self.graph.nodes.items():
            if node.inputs[0]['id'] == input_id:
                return nodeid#TODO: try expect daal de 
        
    
    def forward(self, x):
        # get the node that has not input node and is not getdata node
        current_id = None
        for node_id, node in self.graph.nodes.items():
            if node.title == 'getdata':
                continue
            if self.graph.getParentNode(node_id) is None:
                current_id = node_id
                break

        # print(f'{current_id = } and node is {self.graph.nodes[current_id].title}')

        # current_id = next(node_id for node_id, node in self.graph.nodes.items() if not node.inputs and not node.title.startswith('getdata'))
        try:
            while True:
                x = self.layers[str(current_id)](x)
                # next_edges = [edge for edge in self.graph.edges if edge.start == current_id]# TODO: Error found here the node id should be checked for input and output and not node id
                next_edges = [edge for edge in self.graph.edges if edge.start == self.graph.nodes[current_id].outputs[0]['id']]# TODO: Error found here the node id should be checked for input and output and not node id
                if not next_edges:  # No more edges, stop
                    break
                current_id = self.find_node(next_edges[0].end)
                # print(f'second time {current_id = }')
                # current_id = next_edges[0].end  # Follow the edge to the next node
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
    with open(r'temp\temp.json', 'r') as f:
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

    for (x, y) in enumerate(dataloader):
        print(x, y)
    print(f'{model = }')

    # x = torch.ones(64)
    # print(f'got value as {model(x).size()}')

    # test for custom dataset
    # make a model of 
    dataset = CustomDataset('deleted_files/fake_data.csv')
    dataloader = DataLoader(dataset, batch_size=3, shuffle=True)
    # for (x, y) in enumerate(dataloader):
    #     print(x, y)

    # train the model
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-5)
    loss_fn = nn.MSELoss()
    trainer = training_module(model, dataloader, optimizer, loss_fn)
    trainer.train(epochs=100)

