
import io
import os
from setuptools import setup, find_packages

NAME = "inpoly"
DESCRIPTION = "Fast point(s)-in-polygon queries."
AUTHOR = "Darren Engwirda and Keith Roberts"
AUTHOR_EMAIL = "d.engwirda@gmail.com; krober@usp.br"
URL = "https://github.com/dengwirda/"
VERSION = "0.1.0"
REQUIRES_PYTHON = ">=3.1.0"
KEYWORDS = "Point-in-Polygon Geometry GIS"

REQUIRED = [
    "numpy"
]

CLASSIFY = [
    "Development Status :: 4 - Beta",
    "Operating System :: OS Independent",
    "Intended Audience :: Science/Research",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Topic :: Scientific/Engineering",
    "Topic :: Scientific/Engineering :: Mathematics",
    "Topic :: Scientific/Engineering :: Physics",
    "Topic :: Scientific/Engineering :: Visualization",
    "Topic :: Scientific/Engineering :: GIS"
]

HERE = os.path.abspath(os.path.dirname(__file__))

try:
    with io.open(os.path.join(
            HERE, "README.md"), encoding="utf-8") as f:
        LONG_DESCRIPTION = "\n" + f.read()

except FileNotFoundError:
    LONG_DESCRIPTION = DESCRIPTION

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    license="custom",
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    python_requires=REQUIRES_PYTHON,
    keywords=KEYWORDS,
    url=URL,
    packages=find_packages(),
    install_requires=REQUIRED,
    classifiers=CLASSIFY
)
