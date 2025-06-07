# benchmarks/CMakeLists.txt

# Find benchmark library (Google Benchmark is most common)
find_package(benchmark REQUIRED CONFIG)

# Alternative: find nanobench (lighter alternative)
# find_package(nanobench QUIET)

# Benchmark executable name
set(BENCHMARK_TARGET ${PROJECT_NAME}_benchmarks)

# Collect benchmark source files
file(GLOB_RECURSE BENCHMARK_SOURCES 
    "${CMAKE_CURRENT_SOURCE_DIR}/*.cpp"
    "${CMAKE_CURRENT_SOURCE_DIR}/*.cxx"
)

# Create benchmark executable
add_executable(${BENCHMARK_TARGET} ${BENCHMARK_SOURCES})

# Link libraries
target_link_libraries(${BENCHMARK_TARGET} 
    PRIVATE 
        ${PROJECT_NAME}           # Main project library
        benchmark::benchmark      # Google Benchmark
        benchmark::benchmark_main # Main function provided by benchmark
        fmt::fmt
        spdlog::spdlog
        # Add threading support (often needed for benchmarks)
        $<$<PLATFORM_ID:Linux>:pthread>
)

# Include directories
target_include_directories(${BENCHMARK_TARGET} 
    PRIVATE 
        ${CMAKE_SOURCE_DIR}/include
        ${CMAKE_SOURCE_DIR}/src      # Access to implementation details if needed
)

# Compiler options optimized for benchmarking
target_compile_options(${BENCHMARK_TARGET} 
    PRIVATE
        # Release-like optimizations even in debug builds
        $<$<CONFIG:Debug>:-O2>
        $<$<CONFIG:Release>:-O3 -DNDEBUG -march=native>
        
        # Compiler-specific options
        $<$<NOT:$<CXX_COMPILER_ID:MSVC>>:-Wall -Wextra>
        
        # Disable some warnings that might be problematic in benchmarks
        $<$<NOT:$<CXX_COMPILER_ID:MSVC>>:-Wno-unused-parameter>
        $<$<NOT:$<CXX_COMPILER_ID:MSVC>>:-Wno-unused-variable>
        
        # Enable fast math for better performance (use with caution)
        # $<$<NOT:$<CXX_COMPILER_ID:MSVC>>:-ffast-math>
)

# Link options for optimization
target_link_options(${BENCHMARK_TARGET}
    PRIVATE
        # Strip debug symbols in release for smaller binaries
        $<$<CONFIG:Release>:-s>
        # Link-time optimization
        $<$<CONFIG:Release>:-flto>
)

# Set C++ standard
target_compile_features(${BENCHMARK_TARGET} PRIVATE cxx_std_${CMAKE_CXX_STANDARD})

# Set output directory
set_target_properties(${BENCHMARK_TARGET} PROPERTIES
    RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/benchmarks
    FOLDER "Benchmarks"
)

# Custom target to run benchmarks
add_custom_target(run_benchmarks
    COMMAND ${BENCHMARK_TARGET} 
        --benchmark_format=console
        --benchmark_out=${CMAKE_BINARY_DIR}/benchmark_results.json
        --benchmark_out_format=json
    DEPENDS ${BENCHMARK_TARGET}
    WORKING_DIRECTORY ${CMAKE_BINARY_DIR}
    COMMENT "Running ${PROJECT_NAME} benchmarks"
)

# Target for running benchmarks with detailed output
add_custom_target(run_benchmarks_verbose
    COMMAND ${BENCHMARK_TARGET}
        --benchmark_format=console
        --benchmark_counters_tabular=true
        --benchmark_repetitions=3
        --benchmark_report_aggregates_only=true
        --benchmark_display_aggregates_only=true
        --benchmark_out=${CMAKE_BINARY_DIR}/benchmark_results_verbose.json
        --benchmark_out_format=json
    DEPENDS ${BENCHMARK_TARGET}
    WORKING_DIRECTORY ${CMAKE_BINARY_DIR}
    COMMENT "Running detailed benchmarks"
)

# Target for performance regression testing
add_custom_target(benchmark_compare
    COMMAND ${CMAKE_COMMAND} -E echo "Running baseline benchmarks..."
    COMMAND ${BENCHMARK_TARGET}
        --benchmark_format=json
        --benchmark_out=${CMAKE_BINARY_DIR}/benchmark_baseline.json
        --benchmark_out_format=json
    COMMAND ${CMAKE_COMMAND} -E echo "Compare with previous results using:"
    COMMAND ${CMAKE_COMMAND} -E echo "  benchmark_compare_py baseline.json current.json"
    DEPENDS ${BENCHMARK_TARGET}
    WORKING_DIRECTORY ${CMAKE_BINARY_DIR}
    COMMENT "Running benchmark comparison"
)

# Optional: CPU frequency scaling warning
if(CMAKE_SYSTEM_NAME STREQUAL "Linux")
    add_custom_target(benchmark_setup_check
        COMMAND ${CMAKE_COMMAND} -E echo "Checking CPU frequency scaling..."
        COMMAND ${CMAKE_COMMAND} -E echo "Current governor:"
        COMMAND cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor || true
        COMMAND ${CMAKE_COMMAND} -E echo "For consistent results, consider:"
        COMMAND ${CMAKE_COMMAND} -E echo "  sudo cpupower frequency-set --governor performance"
        VERBATIM
        COMMENT "Checking benchmark environment"
    )
    add_dependencies(run_benchmarks benchmark_setup_check)
endif()

# Profile-guided optimization setup (advanced)
option(ENABLE_PGO "Enable Profile-Guided Optimization" OFF)
if(ENABLE_PGO AND NOT CMAKE_CXX_COMPILER_ID STREQUAL "MSVC")
    # First pass: generate profile data
    add_custom_target(pgo_generate
        COMMAND ${CMAKE_COMMAND} --build . --target ${BENCHMARK_TARGET}
        COMMAND ${BENCHMARK_TARGET} --benchmark_min_time=0.1
        WORKING_DIRECTORY ${CMAKE_BINARY_DIR}
        COMMENT "Generating PGO profile data"
    )
    
    # Add PGO flags
    target_compile_options(${BENCHMARK_TARGET} PRIVATE
        $<$<CONFIG:Release>:-fprofile-generate>
    )
    target_link_options(${BENCHMARK_TARGET} PRIVATE
        $<$<CONFIG:Release>:-fprofile-generate>
    )
endif()

# Memory usage profiling (with massif)
find_program(VALGRIND_PATH valgrind)
if(VALGRIND_PATH)
    add_custom_target(benchmark_memory
        COMMAND ${VALGRIND_PATH}
            --tool=massif
            --stacks=yes
            --massif-out-file=${CMAKE_BINARY_DIR}/massif.out
            ${BENCHMARK_TARGET}
            --benchmark_min_time=0.1
        DEPENDS ${BENCHMARK_TARGET}
        WORKING_DIRECTORY ${CMAKE_BINARY_DIR}
        COMMENT "Running memory usage benchmarks"
    )
endif()

# Perf integration (Linux only)
find_program(PERF_PATH perf)
if(PERF_PATH AND CMAKE_SYSTEM_NAME STREQUAL "Linux")
    add_custom_target(benchmark_perf
        COMMAND ${PERF_PATH} record -g ${BENCHMARK_TARGET} --benchmark_min_time=1.0
        COMMAND ${PERF_PATH} report
        DEPENDS ${BENCHMARK_TARGET}
        WORKING_DIRECTORY ${CMAKE_BINARY_DIR}
        COMMENT "Running performance analysis with perf"
    )
endif()

# Install benchmarks (optional)
option(INSTALL_BENCHMARKS "Install benchmark executables" OFF)
if(INSTALL_BENCHMARKS)
    install(TARGETS ${BENCHMARK_TARGET}
        RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
    )
endif()

# Print configuration
message(STATUS "Benchmark configuration:")
message(STATUS "  Benchmark target: ${BENCHMARK_TARGET}")
message(STATUS "  Benchmark sources: ${BENCHMARK_SOURCES}")
message(STATUS "  Output directory: ${CMAKE_BINARY_DIR}/benchmarks")
message(STATUS "  PGO enabled: ${ENABLE_PGO}")
message(STATUS "  Valgrind available: ${VALGRIND_PATH}")
message(STATUS "  Perf available: ${PERF_PATH}")