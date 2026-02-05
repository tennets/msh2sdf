import msh2sdf.msh2sdf as ms
import numpy as np


def test___find_closest_faces():
    """Test `_find_closest_faces`"""
    
    T = np.array([
        [1, 10], # 0
        [2, 20], # 1
        [3, 30], # 2
        [4, 40], # 3
        [5, 50]  # 4
    ])
    indices = np.array([2, 4, 4, 5, 1])

    expected = [1, 3, 3, 4, 0]

    actual = ms._find_closest_faces(T, indices)
    assert expected == actual, "Closest faces not computed correctly"


def test_compute_sdf():
    """Test `compute_sdf`"""

    # side = 2.5, nseed = 5
    expected = np.array(
        [
           -0.79509158,  0.23227539,  0.75000412,
            0.23223775, -0.79509603, -0.50004944,  
            0.75001648,  2.        ,  0.75      , 
           -0.5       , -0.79509158,  0.23227539,  
            0.75000412,  0.23223775, -0.79509603,
           -1.53554671, -0.79511543, -0.50001236, 
           -0.79508511, -1.53553533, -1.53554671, 
           -0.79511543, -0.50001236, -0.79508511, 
           -1.53553533,
        ])
    
    X, T = ms.get_circle_example()
    actual, _ = ms.compute_sdf(X, T, side=2.5, nseed=5)

    assert np.allclose(expected, actual, atol=1e-06), \
        "SDF not computed correctly!"

    