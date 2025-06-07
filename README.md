# two

[![License: GPL](https://img.shields.io/badge/License-GPL-yellow.svg)](https://opensource.org/licenses/GPL)
[![Documentation Status](https://readthedocs.org/projects/two/badge/)](https://.readthedocs.io/)
[![CI](https://github.com/theSprog/two/actions/workflows/ci.yml/badge.svg)](https://github.com/theSprog/two/actions)
[![codecov](https://codecov.io/gh/theSprog/two/branch/master/graph/badge.svg)](https://codecov.io/gh/theSprog/two)

# Prerequisites

Building one requires the following software installed:

* A C++-compliant compiler
* CMake `>= 3.23`
* Doxygen (optional, documentation building is skipped if missing)

# Building

The following sequence of commands builds `two`. It assumes that your current working directory is the top-level directory of the freshly cloned repository:

```shell
mkdir build
cd build
cmake -DCMAKE_BUILD_TYPE=Release ..
cmake --build .
```

The build process can be customized with the following CMake variables, which can be set by adding `-D<var>={ON, OFF}` to the `cmake` call:

* `BUILD_TESTING`: Enable building of the test suite (default: `ON`)
* `BUILD_DOCS`: Enable building the documentation (default: `ON`)


# Quick Start


# Testing

When built according to the above explanation (with `-DBUILD_TESTING=ON`), the C++ test suite of `two` can be run using `ctest` from the build directory:

```
cd build
ctest
```


# Documentation

`two` provides a Sphinx-based documentation, that can be browsed [online at readthedocs.org](https://two.readthedocs.io). 
To build it locally, first ensure the requirements are installed by running this command from the top-level source directory:

```
pip install -r doc/requirements.txt
```

Then build the sphinx documentation from the top-level build directory:

```
cmake --build . --target sphinx-doc
```

The web documentation can then be browsed by opening `doc/sphinx/index.html` in your browser.


If you like this project, don't forget to ✨ this repo! Happy coding! 🚀