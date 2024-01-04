# Project Name

MLNode is a project that aims to provide a no-code environment and a platform similar to a node editor for developing numerical mathematics, deep learning models, testing models, and developing deep learning/machine learning pipelines.
## Motivation

Major motivation is to provide a more visual and provide a no-code platform for developing deep learning models. This project is inspired by Blender's Geometry Nodes and aims to provide a similar experience for developing deep learning models.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Contributing](#contributing)
- [License](#license)

## Installation

Project is still in project phase, so there is no installation guide for now. But you can clone the project and run it on your local machine by following the steps below.

1. Clone the project
2. Install the required libraries
3. Run the main.py file

```sh
git clone https://github.com/ShubhamMishra1611/MLnode.git
cd MLnode
pip install -r requirements.txt # Please install pytorch as per your system configuration
python main.py
```
## Usage

!image[SimpleMatrix](res\Simple_matrix_calc.png)

This project is inspired by Blender's Geometry Nodes, and its usage is quite similar. To get started, follow the steps below:

1. Create a new project: Click on `File -> New` or press `Ctrl+N`.
2. Open an existing project: Click on `File -> Open` or press `Ctrl+O`.
3. Add a node: Drag from the dockable list widget on the right side or right-click on the canvas.
4. Connect the nodes: Drag from the output port of one node to the input port of another node.

The aim is to provide an interface similar to Blender's Geometry Nodes.

## Features

The features of this project are mainly the nodes available for development. The following nodes are currently available:

1. **Input Node**: Outputs a `np.ndarray` of shape `(input_value, input_value+1)`.
2. **Output Node**: Displays the shape and `ndtype` of the tensor after all operations.
3. **Add Node**: Adds two tensors.
4. **Matmul Node**: Performs matrix multiplication of two tensors.
5. **Trig Node**: Applies trigonometric functions on a tensor.
6. **Transpose Node**: Transposes a tensor.
7. **Scalar Multiplication Node**: Multiplies a tensor with a scalar.

## Contributing

There are various ways to contribute to the project:

1. Contribute to the UI of the project.
2. Contribute to handling node connections and functioning.
3. [Contribute to adding new nodes](https://github.com/ShubhamMishra1611/MLnode/tree/898a2a794ac8b970090046d4a2d15dbacc407a42/MLnodes_nodes).

