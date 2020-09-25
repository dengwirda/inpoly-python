
import time
import numpy as np
cimport numpy as np
cimport cython
@cython.boundscheck(False)  # deactivate bnds checking
@cython.wraparound(False)   # deactivate -.ve indexing
def _inpoly(np.ndarray[double, ndim=+2] vert,
            np.ndarray[double, ndim=+2] node,
            np.ndarray[int, ndim=2] edge, ftol, lbar):
    """
    _INPOLY: the local cython version of the crossing-number
    test. Loop over edges; do a binary-search for the first
    vertex that intersects with the edge y-range; crossing-
    number comparisons; break when the local y-range is met.

    Updated: 25 September, 2020

    Authors: Darren Engwirda, Keith Roberts

    """
    cdef size_t epos, jpos, inod, jnod
    cdef double feps, veps
    cdef double xone, xtwo, xmin, xmax, xdel
    cdef double yone, ytwo, ymin, ymax, ydel
    cdef double xpos, ypos, mul1, mul2

    feps = ftol * (lbar ** +2)
    veps = ftol * (lbar ** +1)

    cdef np.ndarray[np.int8_t] stat = np.full(
        vert.shape[0], +0, dtype=np.int8)

    cdef np.ndarray[np.int8_t] bnds = np.full(
        vert.shape[0], +0, dtype=np.int8)

#----------------------------------- compute y-range overlap
    YMIN = node[edge[:, 0], 1] - veps
   
    cdef np.ndarray[Py_ssize_t] HEAD = \
        np.searchsorted(vert[:, 1], YMIN, "left" )
    
#----------------------------------- loop over polygon edges
    for epos in range(edge.shape[0]):

        inod = edge[epos, 0]            # unpack *this edge
        jnod = edge[epos, 1]

        xone = node[inod, 0]
        xtwo = node[jnod, 0]
        yone = node[inod, 1]
        ytwo = node[jnod, 1]

        xmin = min(xone, xtwo)          # compute edge bbox
        xmax = max(xone, xtwo)

        xmax = xmax + veps
        ymax = ytwo + veps

        xdel = xtwo - xone
        ydel = ytwo - yone

    #------------------------------- calc. edge-intersection
        for jpos in range(HEAD[epos], vert.shape[0]):

            if bnds[jpos]: continue

            xpos = vert[jpos, 0]
            ypos = vert[jpos, 1]

            if ypos >= ymax: break      # due to the y-sort

            if xpos >= xmin:
                if xpos <= xmax:
                #------------------- compute crossing number
                    mul1 = ydel * (xpos - xone)
                    mul2 = xdel * (ypos - yone)

                    if feps >= abs(mul2 - mul1):
                #------------------- BNDS -- approx. on edge
                        bnds[jpos] = 1
                        stat[jpos] = 1

                    elif (ypos == yone) and (xpos == xone):
                #------------------- BNDS -- match about ONE
                        bnds[jpos] = 1
                        stat[jpos] = 1

                    elif (ypos == ytwo) and (xpos == xtwo):
                #------------------- BNDS -- match about TWO
                        bnds[jpos] = 1
                        stat[jpos] = 1

                    elif (mul1 < mul2) and \
                        (ypos >= yone) and (ypos < ytwo):
                #------------------- advance crossing number
                        stat[jpos] = 1 - stat[jpos]

            elif (ypos >= yone) and (ypos < ytwo):
            #----------------------- advance crossing number
                stat[jpos] = 1 - stat[jpos]

    return stat, bnds
