
import os
import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.path as mpltPath

from inpoly import inpoly2
from msh import jigsaw_msh_t, loadmsh

import argparse


def ex_1():

#-- Example 1: set up simple boxes and run points-in-polygon
#-- queries. Boxes defined as a "collection" of polygons and
#-- query points include "exact" matches.

    node = np.array([
        [4, 0], [8, 4], [4, 8], [0, 4], [3, 3],
        [5, 3], [5, 5], [3, 5]])

    edge = np.array([
        [0, 1], [1, 2], [2, 3], [3, 0], [4, 5],
        [5, 6], [6, 7], [7, 4]])

    xpos, ypos = np.meshgrid(
        np.linspace(-1, 9, 51), np.linspace(-1, 9, 51))

    points = np.concatenate((
        np.reshape(xpos, (xpos.size, 1)),
        np.reshape(ypos, (ypos.size, 1))), axis=1)

    IN, ON = inpoly2(points, node, edge)

    fig, ax = plt.subplots()
    plt.plot(points[IN==1, 0], points[IN==1, 1], "b.")
    plt.plot(points[IN==0, 0], points[IN==0, 1], "r.")
    plt.plot(points[ON==1, 0], points[ON==1, 1], "ms")

    ax.set_aspect('equal', adjustable='box')
    plt.show()

    return


def ex_2():

#-- Example 2: load the lake superior geometry and test wrt.
#-- random query points, input nodes + edge centres.

    geom = jigsaw_msh_t()
    loadmsh(os.path.join("dat", "lakes.msh"), geom)

    node = geom.point["coord"]
    edge = geom.edge2["index"]

    emid = (
        0.5 * node[edge[:, 0], :] +
        0.5 * node[edge[:, 1], :]
    )

    rpts = np.random.rand(2500, 2)

    nmax = np.max(node, axis=0)
    nmin = np.min(node, axis=0)
    diff = (nmax - nmin)
    half = (nmin + nmax) / 2.0

    rpts[:, 0] = (rpts[:, 0] - .5) * diff[0] + half[0]
    rpts[:, 1] = (rpts[:, 1] - .5) * diff[1] + half[1]

    points = np.concatenate((node, emid, rpts))

    IN, ON = inpoly2(points, node, edge)

    fig, ax = plt.subplots()
    plt.plot(points[IN==1, 0], points[IN==1, 1], "b.")
    plt.plot(points[IN==0, 0], points[IN==0, 1], "r.")
    plt.plot(points[ON==1, 0], points[ON==1, 1], "ms")

    ax.set_aspect('equal', adjustable='box')
    plt.show()

    return


def ex_3():

#-- Example 3: load geom. from geographic data and test wrt.
#-- random query points, input nodes + edge centres.

#-- Compare run-times against the matplotlib implementation.

    geom = jigsaw_msh_t()
    loadmsh(os.path.join("dat", "coast.msh"), geom)

    node = geom.point["coord"]
    edge = geom.edge2["index"]

    emid = (
        0.5 * node[edge[:, 0], :] +
        0.5 * node[edge[:, 1], :]
    )

    rpts = np.random.rand(25000, 2)

    nmax = np.max(node, axis=0)
    nmin = np.min(node, axis=0)
    diff = (nmax - nmin)
    half = (nmin + nmax) / 2.0

    rpts[:, 0] = (rpts[:, 0] - .5) * diff[0] + half[0]
    rpts[:, 1] = (rpts[:, 1] - .5) * diff[1] + half[1]

    points = np.concatenate((node, emid, rpts))

    ttic = time.time()

    IN, ON = inpoly2(points, node, edge)

    ttoc = time.time()
    print("INPOLY2: ", ttoc - ttic)

    ttic = time.time()

    path = mpltPath.Path(node)
    IN = path.contains_points(points)

    ttoc = time.time()
    print("PLTPATH: ", ttoc - ttic)

    fig, ax = plt.subplots()
    plt.plot(points[IN==1, 0], points[IN==1, 1], "b.")
    plt.plot(points[IN==0, 0], points[IN==0, 1], "r.")
    plt.plot(points[ON==1, 0], points[ON==1, 1], "ms")

    ax.set_aspect('equal', adjustable='box')
    plt.show()

    return


if (__name__ == "__main__"):
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument("--IDnumber", dest="IDnumber", type=int,
                        default=1,
                        required=False, help="Run example with ID = (1-3)")

    args = parser.parse_args()

    if (args.IDnumber == 1): ex_1()
    if (args.IDnumber == 2): ex_2()
    if (args.IDnumber == 3): ex_3()
