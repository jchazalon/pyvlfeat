#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Installation script for the vlfeat module
"""

import sys, os, platform
from distutils.core import Extension, setup
from distutils.errors import DistutilsFileError
from distutils.command.build_ext import build_ext

__version__ = '0.1.2'

# You may edit this line to force the path to the Numpy headers
# example: 
# NUMPY_PATH = /home/alice/.virtualenvs/testpyvlfeat/local/lib/python2.7/site-packages/numpy/core/include
NUMPY_PATH = None


vlfeat_src = ['vlfeat/vl/aib.c', 'vlfeat/vl/generic.c',
              'vlfeat/vl/hikmeans.c', 'vlfeat/vl/ikmeans.c',
              'vlfeat/vl/imopv.c', 'vlfeat/vl/mathop.c',
              'vlfeat/vl/mathop_sse2.c', 'vlfeat/vl/pgm.c',
              'vlfeat/vl/rodrigues.c', 'vlfeat/vl/stringop.c',
              'vlfeat/vl/getopt_long.c', 'vlfeat/vl/host.c',
              'vlfeat/vl/imopv_sse2.c', 'vlfeat/vl/mser.c',
              'vlfeat/vl/random.c', 'vlfeat/vl/sift.c',
              'vlfeat/vl/dsift.c', 'vlfeat/vl/quickshift.c',
              'vlfeat/mser/vl_erfill.cpp', 'vlfeat/mser/vl_mser.cpp',
              'vlfeat/sift/vl_sift.cpp', 'vlfeat/sift/vl_dsift.cpp',
              'vlfeat/sift/vl_siftdescriptor.cpp', 'vlfeat/imop/vl_imsmooth.cpp',
              'vlfeat/misc/vl_binsum.cpp', 'vlfeat/kmeans/vl_hikmeans.cpp',
              'vlfeat/kmeans/vl_ikmeans.cpp', 'vlfeat/kmeans/vl_hikmeanspush.cpp',
              'vlfeat/kmeans/vl_ikmeanspush.cpp', 'vlfeat/quickshift/vl_quickshift.cpp',
              'vlfeat/py_vlfeat.cpp']

vlfeat_dep = ['vlfeat/vl/aib.h', 'vlfeat/vl/generic.h',
              'vlfeat/vl/hikmeans.h', 'vlfeat/vl/ikmeans.h',
              'vlfeat/vl/imopv.h', 'vlfeat/vl/mathop.h',   
              'vlfeat/vl/mathop_sse2.h', 'vlfeat/vl/pgm.h',
              'vlfeat/vl/rodrigues.h', 'vlfeat/vl/stringop.h',
              'vlfeat/vl/getopt_long.h', 'vlfeat/vl/host.h',
              'vlfeat/vl/imopv_sse2.h', 'vlfeat/vl/mser.h',
              'vlfeat/vl/random.h', 'vlfeat/vl/sift.h',
              'vlfeat/vl/dsift.h', 'vlfeat/vl/quickshift.h',
              'vlfeat/kmeans/vl_hikmeans.h', 'vlfeat/kmeans/vl_ikmeans.h',
              'vlfeat/quickshift/vl_quickshift.h', 'vlfeat/py_vlfeat.h'
              ]

IncludeDirs = ['vlfeat/']
LibraryDirs = None
Libraries = None
BuildExtension = build_ext

PreprocMacros = []
CompileArgs = []
LinkArgs = []


if platform.system() == "Windows":
    print "Using Windows-specific compiler and linker flags."
    PreprocMacros = [('VL_BUILD_DLL', '1'), ('__SSE2__', 1)]
    CompileArgs = ['/O2', '/w', "/EHsc"]
    LinkArgs = []
else: # Linux and maybe Darwin
    print "Using default Unix-specific compiler and linker flags."
    CompileArgs = ['-msse2', '-O2', '-fPIC', '-w']
    LinkArgs = ['-msse', '-shared', '-lboost_python'] # '-lm', '-lpthread',


if NUMPY_PATH is not None:
    IncludeDirs.append(NUMPY_PATH)
else:
    foundNumpy = False
    for npPath in [
        os.path.join(sys.prefix, 'lib',
                        'python%d.%d' % (sys.version_info[:2]),
                        'site-packages/numpy/core/include'),
        os.path.join(sys.prefix, 'lib',
                        'site-packages/numpy/core/include'),
        os.path.join(sys.prefix, 'lib',
                        'python%d.%d' % (sys.version_info[:2]),
                        'dist-packages/numpy/core/include'),
        os.path.join(sys.prefix, 'lib',
                        'dist-packages/numpy/core/include'),
        ]:
        print "Checking for Numpy headers at '%s'" % npPath
        if os.path.exists(npPath):
            IncludeDirs.append(npPath)
            foundNumpy = True
            print "\tFound."
            break
    if not foundNumpy:
        print "Warning, could not find Numpy headers automatically."
        print ("\t You still can configure include environment variable"
                +" to provide the compiler with a suitable path.")


def mkExtension(name):
    modname = '_' + name.lower()
    src = globals()[name.lower() + '_src']
    dep = globals()[name.lower() + '_dep']
    return Extension(modname, src, libraries=Libraries, depends=dep,
                     define_macros=PreprocMacros,
                     include_dirs=IncludeDirs, library_dirs=LibraryDirs,
                     extra_compile_args=CompileArgs, extra_link_args=LinkArgs)

setup(name = 'pyvlfeat', version = __version__,
      requires = ['numpy', 'matplotlib'],
      packages = ['vlfeat'],
      package_dir = { 'vlfeat' : 'vlfeat' },
      ext_modules = [mkExtension('vlfeat')],
      py_modules  = ['vlfeat.__init__', 'vlfeat.kmeans.__init__',
                     'vlfeat.kmeans.vl_hikmeanshist', 'vlfeat.kmeans.vl_ikmeanshist',
                     'vlfeat.misc.__init__', 'vlfeat.misc.colorspaces', 
                     'vlfeat.mser.__init__', 'vlfeat.mser.vl_ertr', 
                     'vlfeat.plotop.__init__', 'vlfeat.plotop.vl_plotframe', 
                     'vlfeat.quickshift.__init__', 'vlfeat.test.__init__',
                     'vlfeat.test.vl_test_hikmeans', 'vlfeat.test.vl_test_ikmeans',
                     'vlfeat.test.vl_test_pattern'],
      cmdclass = { "build_ext" : BuildExtension },
      description = 'Python interface to the VLFeat library',
      author = 'Andrea Vedaldi, Brian Fulkerson, Mikael Rousson',
      author_email = 'vedaldi@robots.ox.ac.uk',
      maintainer = 'Peter Le Bek',
      maintainer_email = 'peter@hyperplex.net',
      url = 'http://launchpad.net/pyvlfeat',
      license = 'GPL',
      platforms = ['Unix', 'Linux', 'Windows'],
      long_description = """
* Scale-Invariant Feature Transform (SIFT)
* Dense SIFT (DSIFT)
* Integer k-means (IKM)
* Hierarchical Integer k-means (HIKM)
* Maximally Stable Extremal Regions (MSER)
* Quick shift image segmentation
* http://vlfeat.org

Dependencies:

* Boost.Python (libboost-python-dev on Debian systems)
* NumPy
* Matplotlib
""",
      classifiers=[
        'Operating System :: Unix',
        'Operating System :: Windows',
        'Programming Language :: C',
        'Programming Language :: C++',
        'Programming Language :: Python',
        'Development Status :: 1 - Planning',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Scientific/Engineering :: Image Recognition',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Developers',
        'License :: OSI Approved'
        ],
     )
