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


def compute_sdf(X:ndarray, T:ndarray, side:float=5) -> (ndarray, ndarray):
    """Compute the signed distance function.

    Args:
        X (ndarray): Coordinate matrix of the surface.
        T (ndarray): Connectivity matrix of the surface.
        side (float): Side length of the background mesh.

    Returns:
        ndarray: Signed distance function over the background mesh.
        ndarray: The supporting background mesh.
    """
    
    XB = _create_square_background_mesh(side=side)
    tree = cKDTree(data=X, copy_data=False)  
    distances, indices = tree.query(XB, k=1,)

    signed_distances = np.zeros(XB.shape[0],)

    for i, idx in enumerate(indices):
        # Identify the two closest nodes to XB[i] (P) and
        # establish a fixed direction using the connectivity matrix.
        # The closest node (A) is always the first on the edge, 
        # ensuring consistent direction. 
        # The second closest node (B) is the second on the edge. 
        # With the direction set, we then determine the sign based
        # on the third component of the cross product.
        signed_distance = np.linalg.norm(XB[i] - X[idx])
 
        idx_closest = np.flatnonzero((T[:, 0] == idx))[0]

        A, B = X[T[idx_closest, 0]], X[T[idx_closest, 1]]
        P = XB[i]
        AB = B - A
        AP = P - A

        CPV = np.cross(np.hstack([AB, 0]),  np.hstack([AP, 0]))
        if CPV[-1] < 0:
            signed_distance *= -1

        signed_distances[i] = signed_distance

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