from scipy.spatial import cKDTree
import numpy as np
from numpy import ndarray
import matplotlib.pyplot as plt


def _create_square_background_mesh(side:int, nseed:int=100) -> ndarray:
    """Create uniform square background mesh.

    Args:
        side (int): Side length.
        nseed (int, optional): Number of seed points. Defaults to 100.

    Returns:
        ndarray: Coordinate matrix of the background mesh.

    Note:
    The background mesh is centered in (0,0).
    """

    XB = np.zeros((nseed * nseed, 2))

    x1  = np.linspace(-side, side, num=nseed)
    x2c = np.linspace(-side, side, num=nseed)

    for i in range(nseed):
        
        x2 = np.tile(x2c[i], (nseed, 1))
        pos = np.arange((i - 1) * nseed, i * nseed)

        XB[pos, 0], XB[pos, 1] = np.squeeze(x1), np.squeeze(x2)

    return XB


def _find_closest_faces(T:ndarray, indices:ndarray) -> list:
    """Retrieve the row indices of T where T[i, 0] matches an element in indices.

    This function identifies all row indices in T for which `T[i, 0]` equals 
    `indices[j]` for some indices `i` and `j`. It is important to note that 
    `indices` may contain duplicates, as multiple nodes in the background mesh 
    `XB` can share the same closest node defined by `X[indices[j]]`.

    Args:
        T (ndarray): Connectivity matrix of the surface.
        indices (ndarry): Indices of the closest node. Indices
                          refers to `X`.

    Returns:
        list: Row indices.
    """

    indices_flat = indices.flatten()

    sorted_T = np.sort(T[:, 0])
    original_indices = np.argsort(T[:, 0])

    indices_in_T = np.searchsorted(sorted_T, indices_flat)
    
    result_indices = original_indices[indices_in_T]

    return result_indices.tolist()


def compute_sdf(X:ndarray, T:ndarray, side:float=5, nseed:int=100) -> (ndarray, ndarray):
    """Compute the signed distance function.

    Args:
        X (ndarray): Coordinate matrix of the surface.
        T (ndarray): Connectivity matrix of the surface.
        side (float): Side length of the background mesh.
        nseed (int): Number of seed points of the background mesh.

    Returns:
        ndarray: Signed distance function over the background mesh.
        ndarray: The supporting background mesh.
    """
    
    XB = _create_square_background_mesh(side=side, nseed=nseed)
    tree = cKDTree(data=X, copy_data=False)  
    signed_distances, indices = tree.query(XB, k=1)

    # Identify the two closest nodes to XB[i] (P) and
    # establish a fixed direction using the connectivity matrix.
    # The closest node (A) is always the first on the edge, 
    # ensuring consistent direction. 
    # The second closest node (B) is the second on the edge. 
    # With the direction set, we then determine the sign based
    # on the third component of the cross product.

    idx = _find_closest_faces(T, indices)

    A, B = X[T[idx, 0]], X[T[idx, 1]]
    AB = np.hstack([B - A, np.zeros((XB.shape[0], 1))])
    AP = np.hstack([XB - A, np.zeros((XB.shape[0], 1))])

    cross_prod = np.cross(AB, AP, axis=1)
    signed_distances[cross_prod[:, 2] < 0] *= -1

    return (signed_distances, XB)


def plot_sdf(sdf:ndarray, XB:ndarray, X:ndarray) -> None:
    """Plot signed distance function over background mesh.

    Args:
        sdf (ndarray): Signed distance function over the background mesh.
        XB (ndarray): Supporting background mesh.
        X (ndarray): Coordinate matrix of the surface.
    """
    plt.tricontourf(XB[:, 0], XB[:, 1], sdf, levels=50, cmap="RdBu")
    plt.colorbar()
    plt.title("Signed Distance Field")
    plt.scatter(X[:, 0], X[:, 1], color="black", s=.5)  
    plt.axis("equal")
    plt.show()


def get_circle_example(radius:float=2, npoints:int=1000) -> (ndarray, ndarray):
    """Get coordinate and connectivity matrix of a circular boundary.

    Args:
        radius (float, optional): Radius of the circle. Defaults to 2.
        npoints (int, optional): Number of points on the boundary. Defaults to 1000.

    Return:
        ndarray: Coordinate matrix.
        ndarray: Connectivity matrix.
    """

    theta = np.linspace(0, 2 * np.pi, npoints)
    X = np.column_stack((radius * np.cos(theta), radius * np.sin(theta)), )
    T = np.array(
        np.column_stack(
            (
                np.linspace(0, npoints-1, npoints), 
                np.hstack([np.linspace(1, npoints-1, npoints-1), [0]])
            )
        ),dtype=int)

    return (X, T)