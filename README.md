# `msh2sdf`

> `msh2sdf` is a Python package for unfitted finite element simulations that provides an implicit geometric description of a mesh using a signed distance function.

It computes a signed distance function (SDF) to a specified surface 
mesh, on the nodes of a background mesh.
This surface mesh defines the boundary of the object to be modelled.

The SDF offers an implicit representation of the surface on a fixed 
background mesh facilitating unfitted finite element methodologies.

> [!WARNING]
> This package is currently under active development and is not yet stable.
> The APIs may undergo significant changes in future releases. See [ROADMAP](./ROADMAP.md) for more details.

## Installation
You can install the package using `pip`:
```python
pip install -i https://test.pypi.org/simple/ msh2sdf
```

## Usage
Compute the SDF for a circular boundary of radius 2 having 1000 points.
```python
import msh2sdf as ms

X, T = ms.get_circle_example()
sdf, XB = ms.compute_sdf(X,T,)
ms.plot_sdf(sdf,XB,X)
```

## Development
### Setup 
1. Clone the repository:
    ```bash
    git clone https://github.com/tennets/msh2sdf.git
    cd msh2sdf
    ```
2. Install development dependencies:
    ```bash
    pip install -r requirements.txt
    ```
### Running Tests
To run the tests, execute:
```bash
pytest tests/
```
Ensure all tests pass before submitting changes.

## Contributing
Contributions and feedback are welcome! Please submit a pull request or open an issue for discussion.

## Licence
This package is licensed under the MIT License. See the [LICENSE](./LICENSE) file for more details.
