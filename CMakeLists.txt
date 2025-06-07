cmake_minimum_required(VERSION 3.23)
project(two VERSION 0.0.1 LANGUAGES CXX)

# ------------------------------------------------------------------
include(cmake/Vars.cmake)
include(cmake/Functions.cmake)
include(cmake/CompilerFlags.cmake)
include(cmake/Targets.cmake)

# Test
option(BUILD_TESTS "Build unit tests" OFF)
if(BUILD_TESTS)
    enable_testing()
    add_subdirectory(tests)
endif()

# Benchmark
option(BUILD_BENCHMARKS "Build benchmarks" OFF)
if(BUILD_BENCHMARKS)
    add_subdirectory(benchmarks)
endif()

# Example
option(BUILD_EXAMPLES "Build examples" OFF)
if(BUILD_EXAMPLES)
    add_subdirectory(examples)
endif()


