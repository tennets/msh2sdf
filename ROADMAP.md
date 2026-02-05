# ROADMAP for `msh2sdf`

> [!IMPORTANT]
> For the moment, `msh2sdf` supports only 2D triangular meshes.

- [ ] **Vectorize** the loop over the background mesh in `compute_sdf`.
- [ ] Add a submodule **`create`** to handle the generation of different background meshes. For example:
    ```python
    >>> import msh2sdf as ms
    >>> X, T = ms.create.<mesh-generator-name>()
    ```
    - `<mesh-generator-name>` should return a coordinate (`X`) and connectivity (`T`) matrix.
    - Examples of functions that can be implemented in the `create` module:
        * `square(side, np,)`: generates a square background mesh.
        * `rectangle(side_x, side_y, np_x, np_y,)`: generates a rectangular background mesh.

- [ ] Add the **`Transformer`** class to `msh2sdf`. This class will change the API significantly as `compute_sdf` will now be implemented as a class method. 
    ```python
    >>> import msh2sdf as ms
    >>> tr = ms.Transformer(X, T, XB,)
    >>> sdf = tr.compute_sdf()
    ```
    The `Transformer(X, T, XB, center=True, align=True)` class implements methods to:
    * Automatically check if arguments are 2D triangular meshes.
    * Automatically validate arguments and throw errors if invalid.
    * Center and align `X` to its principal axes of inertia.
    * Check if `XB` embeds `X`, throwing an error if it doesn't. If either `center` or `align` is `True`, checks are performed before and after the transformation to inform the user whether to skip transformation for the geometry to pass this check.
    * Compute the signed distance function as `tr.compute_sdf()` and return it as a vector.
    * Plot the signed distance function as `tr.plot_sdf()`.

- [ ] Implement **lazy import dynamics** to import methods and classes only when needed.

- [ ] Implement an **exception wrapper during import** (similar to [this](https://trimesh.org/trimesh.exceptions.html)). This will provide users with clearer error messages instead of just import errors.

> **NOTE:** 
> In future releases, we would like to pass a `mesh` object similar to [**trimesh.Trimesh**](https://trimesh.org/trimesh.base.html#trimesh.base.Trimesh) instead of `X` and `T`.
