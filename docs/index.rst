Welcome to @two@ Documentation!
==========================================

.. meta::
   :description: Complete documentation for @two@, a modern C++ library
   :keywords: C++, library, documentation, API

@two@ is a modern C++ library designed for high performance and ease of use.

.. note::
   This documentation is generated automatically from the source code using Doxygen and Sphinx.

Quick Start
-----------

Installation
~~~~~~~~~~~~

.. code-block:: bash

   git clone https://github.com/yourusername/@two@.git
   cd @two@
   mkdir build && cd build
   cmake ..
   make

Basic Usage
~~~~~~~~~~~

.. code-block:: cpp

   #include "@two@/@two@.hpp"
   
   int main() {
       // Your code here
       return 0;
   }

Table of Contents
-----------------

.. toctree::
   :maxdepth: 2
   :caption: User Guide
   
   installation
   quickstart
   tutorial
   examples

.. toctree::
   :maxdepth: 2
   :caption: API Reference
   
   api/index
   api/classes
   api/functions
   api/namespaces

.. toctree::
   :maxdepth: 2
   :caption: Development
   
   development/building
   development/contributing
   development/testing
   development/benchmarks

.. toctree::
   :maxdepth: 1
   :caption: Additional Information
   
   changelog
   license
   faq

API Documentation
-----------------

The complete API documentation is generated from source code comments:

.. doxygenindex::
   :project: @two@

Core Classes
~~~~~~~~~~~~

.. doxygenclass:: YourMainClass
   :project: @two@
   :members:
   :undoc-members:

Core Functions
~~~~~~~~~~~~~~

.. doxygenfunction:: your_main_function
   :project: @two@

Features
--------

* 🚀 **High Performance**: Optimized for speed and efficiency
* 🛡️ **Type Safety**: Modern C++ features for compile-time safety
* 📚 **Well Documented**: Comprehensive API documentation
* 🧪 **Thoroughly Tested**: Extensive unit and integration tests
* 🔧 **Easy Integration**: CMake support and package managers
* 📦 **Header Only**: Simple inclusion in your projects

Requirements
------------

* C++17 or later
* CMake 3.23+
* Supported compilers:
  
  * GCC 9+
  * Clang 10+
  * MSVC 2019+

Dependencies
------------

* `fmt <https://fmt.dev/>`_ - Modern formatting library
* `spdlog <https://github.com/gabime/spdlog>`_ - Fast logging library

Examples
--------

Browse our :doc:`examples` section for practical usage examples.

Contributing
------------

We welcome contributions! Please see our :doc:`development/contributing` guide.

License
-------

This project is licensed under the MIT License - see the :doc:`license` file for details.

Support
-------

* 📖 Documentation: You're reading it!
* 🐛 Bug Reports: `GitHub Issues <https://github.com/yourusername/@two@/issues>`_
* 💬 Discussions: `GitHub Discussions <https://github.com/yourusername/@two@/discussions>`_
* 📧 Contact: your.email@example.com

Indices and Tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

----

.. note::
   Documentation built on |today| for @two@ version |version|.