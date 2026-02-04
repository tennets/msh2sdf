"""
msh2sdf is a Python package designed for unfitted finite element simulations.

It computes a signed distance function (SDF) to a specified surface 
mesh, on the nodes of a background mesh.
This surface mesh defines the boundary of the object to be modelled.

The SDF offers an implicit representation of the surface on a fixed 
background mesh facilitating unfitted finite element methodologies.
"""
from importlib.metadata import version


from mesh2sdf import compute_sdf, plot_sdf, get_circle_example


__version__ = version("msh2sdf")

__all__ = [
    "compute_sdf",
    "plot_sdf",
    "get_circle_example",
    ]
