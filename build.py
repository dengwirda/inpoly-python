from Cython.Build import build_ext, cythonize
from setuptools import Extension
from setuptools.dist import Distribution
import Cython.Compiler.Options
import numpy as np
import os
import shutil
import logging

logger = logging.getLogger(__name__)

def build():
    ext_modules = cythonize(Extension(
        "inpoly.inpoly_",
        sources=[os.path.join("inpoly", "inpoly_.pyx")],
        include_dirs=[np.get_include()])
    )
    distribution = Distribution({"name": "extended", "ext_modules": ext_modules})
    distribution.package_dir = "extended"
    cmd = build_ext(distribution)
    cmd.ensure_finalized()
    cmd.run()
    # Copy built extensions back to the project
    for output in cmd.get_outputs():
        relative_extension = os.path.relpath(output, cmd.build_lib)
        shutil.copyfile(output, relative_extension)
        mode = os.stat(relative_extension).st_mode
        mode |= (mode & 0o444) >> 2
        os.chmod(relative_extension, mode)

try:
    build()
except Exception as e:
    logger.warning('Could not build cython extensions, using pure Python implementtation.\nThe error was:\n{e}')


