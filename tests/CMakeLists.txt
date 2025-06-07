# Find Catch2, or else you needed
find_package(Catch2 REQUIRED CONFIG)

# Test executable name
set(TEST_TARGET ${PROJECT_NAME}_tests)

# Collect test source files
file(GLOB_RECURSE TEST_SOURCES 
    "${CMAKE_CURRENT_SOURCE_DIR}/*.cpp"
    "${CMAKE_CURRENT_SOURCE_DIR}/*.cxx"
)

# Create test executable
add_executable(${TEST_TARGET} ${TEST_SOURCES})

# Link libraries
target_link_libraries(${TEST_TARGET} 
    PRIVATE 
        ${PROJECT_NAME}              # Link to main library/executable
        Catch2::Catch2WithMain       # Catch2 with main function
        fmt::fmt                     # Same dependencies as main target
        spdlog::spdlog
)

# Include directories
target_include_directories(${TEST_TARGET} 
    PRIVATE 
        ${CMAKE_SOURCE_DIR}/include  # Main project headers
        ${CMAKE_SOURCE_DIR}/src      # Access to implementation if needed
)

# Compiler options (inherit from main target but with some adjustments)
target_compile_options(${TEST_TARGET} 
    PRIVATE
        $<$<CXX_COMPILER_ID:MSVC>:${MSVC_FLAGS}>
        $<$<NOT:$<CXX_COMPILER_ID:MSVC>>:${GNU_FLAGS}>
        # Remove some strict warnings that might be problematic in tests
        $<$<NOT:$<CXX_COMPILER_ID:MSVC>>:-Wno-unused-function>
        $<$<NOT:$<CXX_COMPILER_ID:MSVC>>:-Wno-missing-declarations>
)

# Set C++ standard (should match main project)
target_compile_features(${TEST_TARGET} PRIVATE cxx_std_${CMAKE_CXX_STANDARD})

# Test discovery and registration
include(CTest)
include(Catch)
catch_discover_tests(${TEST_TARGET}
    TEST_PREFIX "${PROJECT_NAME}::"
    REPORTER XML
    OUTPUT_DIR ${CMAKE_BINARY_DIR}/test_results
    OUTPUT_PREFIX "${PROJECT_NAME}_"
    OUTPUT_SUFFIX .xml
)

# Custom test target for running tests
add_custom_target(run_tests
    COMMAND ${TEST_TARGET}
    DEPENDS ${TEST_TARGET}
    WORKING_DIRECTORY ${CMAKE_BINARY_DIR}
    COMMENT "Running ${PROJECT_NAME} tests"
)

# Coverage target (optional, for GCC/Clang)
if(CMAKE_BUILD_TYPE STREQUAL "Debug" AND 
   (CMAKE_CXX_COMPILER_ID STREQUAL "GNU" OR CMAKE_CXX_COMPILER_ID STREQUAL "Clang"))
    
    option(ENABLE_COVERAGE "Enable coverage reporting" OFF)
    
    if(ENABLE_COVERAGE)
        target_compile_options(${TEST_TARGET} PRIVATE --coverage -fprofile-arcs -ftest-coverage)
        target_link_options(${TEST_TARGET} PRIVATE --coverage)
        
        # Coverage report target
        find_program(GCOV_PATH gcov)
        find_program(LCOV_PATH lcov)
        find_program(GENHTML_PATH genhtml)
        
        if(GCOV_PATH AND LCOV_PATH AND GENHTML_PATH)
            add_custom_target(coverage
                COMMAND ${LCOV_PATH} --directory . --zerocounters
                COMMAND ${TEST_TARGET}
                COMMAND ${LCOV_PATH} --directory . --capture --output-file coverage.info
                COMMAND ${LCOV_PATH} --remove coverage.info 'tests/*' '/usr/*' --output-file coverage.info.cleaned
                COMMAND ${GENHTML_PATH} -o coverage coverage.info.cleaned
                DEPENDS ${TEST_TARGET}
                WORKING_DIRECTORY ${CMAKE_BINARY_DIR}
                COMMENT "Generating code coverage report"
            )
        endif()
    endif()
endif()

# Valgrind target (optional, for memory checking)
find_program(VALGRIND_PATH valgrind)
if(VALGRIND_PATH)
    add_custom_target(memcheck
        COMMAND ${VALGRIND_PATH} 
            --tool=memcheck 
            --leak-check=full 
            --show-leak-kinds=all 
            --track-origins=yes 
            --verbose 
            --error-exitcode=1
            $<TARGET_FILE:${TEST_TARGET}>
        DEPENDS ${TEST_TARGET}
        WORKING_DIRECTORY ${CMAKE_BINARY_DIR}
        COMMENT "Running memory check with Valgrind"
    )
endif()

# Print test configuration info
message(STATUS "Test configuration:")
message(STATUS "  Test target: ${TEST_TARGET}")
message(STATUS "  Test sources found: ${TEST_SOURCES}")
message(STATUS "  Coverage enabled: ${ENABLE_COVERAGE}")
message(STATUS "  Valgrind available: ${VALGRIND_PATH}")