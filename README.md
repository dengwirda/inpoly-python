## `INPOLY: Fast point(s)-in-polygon queries`

A fast 'point(s)-in-polygon' routine for `Python`.

`INPOLY` returns the "inside/outside" status for a set of vertices `VERT` and a general polygon (`PSLG`) embedded in the two-dimensional plane. General non-convex and multiply-connected polygonal regions can be handled.

<p align="center">
  <img src = "../master/img/query.png">
</p>

`INPOLY` is based on a 'crossing-number' test, counting the number of times a line extending from each point past the right-most region of the polygon intersects with the polygonal boundary. Points with odd counts are 'inside'. A simple implementation requires that each edge intersection be checked for each point, leading to (slow) `O(N*M)` overall complexity.

This implementation seeks to improve these bounds. Query points are sorted by `y-value` and candidate intersection sets are determined via binary-search. Given a configuration with `N` test points, `M` edges and an average point-edge 'overlap' of `H`, the overall complexity scales like `O(M*H + M*LOG(N) + N*LOG(N))`, where `O(N*LOG(N))` operations are required for the initial sorting, `O(M*LOG(N))` operations are required for the set of binary-searches, and `O(M*H)` operations are required for the actual intersection tests. `H` is typically small on average, such that `H << N`. Overall, this leads to fast `O((N+M)*LOG(N))` complexity for average cases.

### `Quickstart`

    Clone/download + unpack this repository.
    python3 setup.py install
    python3 example.py --IDnumber=1
    python3 example.py --IDnumber=2
    python3 example.py --IDnumber=3

### `Demo problems`

The following set of example problems are available in `example.py`: 

    example: 1 # a simple box-type geometry to get started
    example: 2 # random queries using a common geographic dataset
    example: 3 # speed test vs existing inpolygon implementations

Run `python3 example.py --IDnumber=N` to call the `N-th` example.

### `Fast kernels`

`INPOLY` relies on `Cython` to compile the core "inpolygon" tests into a fast kernel. `inpoly_.pyx` contains the human-readable `Cython` implementation, `inpoly_.c` is the auto-generated output. For a full build:

    python3 setup.py build_ext --inplace
    python3 setup.py install

These steps should "compile" the `Cython` kernel `inpoly_.pyx` into the `Python`-compatible `c`-code `inpoly_.c`, which can then be compiled into the binary lib `inpoly_.so[pyd|dylib]`.

### `License Terms`

This program may be freely redistributed under the condition that the copyright notices (including this entire header) are not removed, and no compensation is received through use of the software.  Private, research, and institutional use is free.  You may distribute modified versions of this code `UNDER THE CONDITION THAT THIS CODE AND ANY MODIFICATIONS MADE TO IT IN THE SAME FILE REMAIN UNDER COPYRIGHT OF THE ORIGINAL AUTHOR, BOTH SOURCE AND OBJECT CODE ARE MADE FREELY AVAILABLE WITHOUT CHARGE, AND CLEAR NOTICE IS GIVEN OF THE MODIFICATIONS`. Distribution of this code as part of a commercial system is permissible `ONLY BY DIRECT ARRANGEMENT WITH THE AUTHOR`. (If you are not directly supplying this code to a customer, and you are instead telling them how they can obtain it for free, then you are not required to make any arrangement with me.) 

`DISCLAIMER`:  Neither I nor the University of Sydney warrant this code in any way whatsoever. This code is provided "as-is" to be used at your own risk.

### `References`

`[1]` - J. Kepner, D. Engwirda, V. Gadepally, C. Hill, T. Kraska, M. Jones, A. Kipf, L. Milechin, N. Vembar: <a href="https://arxiv.org/abs/2005.03156">Fast Mapping onto Census Blocks</a>, IEEE HPEC, 2020.
