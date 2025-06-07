# Source files
file(GLOB_RECURSE SRC_FILES src/*.cpp)

# Target
# === Libraries ===

# === Executables ===
add_executable(two ${SRC_FILES})

# auto generate cmake
if(CMAKE_BUILD_TYPE STREQUAL "Release")
    file(GLOB release_cmake_files "${CMAKE_SOURCE_DIR}/cmake/build/*.Release.cmake")
    foreach(f ${release_cmake_files})
        log(DEBUG "Including ${f}")
        include(${f})
    endforeach()
else()
    file(GLOB debug_cmake_files "${CMAKE_SOURCE_DIR}/cmake/build/*.Debug.cmake")
    foreach(f ${debug_cmake_files})
        log(DEBUG "Including ${f}")
        include(${f})
    endforeach()
endif()