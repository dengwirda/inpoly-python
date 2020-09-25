
import numpy as np
cimport numpy as np


def _inpoly(np.ndarray[double, ndim=+2] vert,
            np.ndarray[double, ndim=+2] node,
            np.ndarray[int, ndim=2] edge, ftol, lbar):
    """
    _INPOLY: the local cython version of the crossing-number
    test. Loop over edges; do a binary-search for the first
    vertex that intersects with the edge y-range; crossing-
    number comparisons; break when the local y-range is met.

    """
    cdef size_t epos, jpos, inod, jnod
    cdef double feps, veps
    cdef double xone, xtwo, xmin, xmax, xdel
    cdef double yone, ytwo, ymin, ymax, ydel
    cdef double xpos, ypos, mul1, mul2

    feps = ftol * (lbar ** +2)
    veps = ftol * (lbar ** +1)

    cdef np.ndarray[np.int8_t] stat = np.full(
        vert.shape[0], 0, dtype=np.int8)

    cdef np.ndarray[np.int8_t] bnds = np.full(
        vert.shape[0], 0, dtype=np.int8)

#----------------------------------- compute y-range overlap
    YMIN = node[edge[:, 0], 1] - veps
    YMAX = node[edge[:, 1], 1] + veps

    cdef np.ndarray[long] HEAD = \
        np.searchsorted(vert[:, 1], YMIN, "left" )

    cdef np.ndarray[long] TAIL = \
        np.searchsorted(vert[:, 1], YMAX, "right")

#----------------------------------- loop over polygon edges
    for epos in range(edge.shape[0]):

        inod = edge[epos, 0]            # unpack *this edge
        jnod = edge[epos, 1]

        xone = node[inod, 0]
        xtwo = node[jnod, 0]
        yone = node[inod, 1]
        ytwo = node[jnod, 1]

        xmin = min(xone, xtwo)
        xmax = max(xone, xtwo)

        xmax = xmax + veps
        xdel = xtwo - xone
        ydel = ytwo - yone

    #------------------------------- calc. edge-intersection
        for jpos in range(HEAD[epos], TAIL[epos]):

            if bnds[jpos]: continue

            xpos = vert[jpos, 0]
            ypos = vert[jpos, 1]

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
