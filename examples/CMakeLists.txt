# Find all example subdirectories
file(GLOB EXAMPLE_SUBDIRS LIST_DIRECTORIES true "${CMAKE_CURRENT_SOURCE_DIR}/*")
list(FILTER EXAMPLE_SUBDIRS INCLUDE REGEX ".*[^/\\]$")  # Filter out files

# Function to create example targets
function(add_example EXAMPLE_NAME)
    set(EXAMPLE_TARGET "example_${EXAMPLE_NAME}")
    
    # Find source files for this example
    file(GLOB_RECURSE EXAMPLE_SOURCES 
        "${CMAKE_CURRENT_SOURCE_DIR}/${EXAMPLE_NAME}/*.cpp"
        "${CMAKE_CURRENT_SOURCE_DIR}/${EXAMPLE_NAME}/*.cxx"
    )
    
    if(NOT EXAMPLE_SOURCES)
        message(WARNING "No source files found for example: ${EXAMPLE_NAME}")
        return()
    endif()
    
    # Create executable
    add_executable(${EXAMPLE_TARGET} ${EXAMPLE_SOURCES})
    
    # Link libraries
    target_link_libraries(${EXAMPLE_TARGET} 
        PRIVATE 
            ${PROJECT_NAME}      # Main project library
            fmt::fmt
            spdlog::spdlog
    )
    
    # Include directories
    target_include_directories(${EXAMPLE_TARGET} 
        PRIVATE 
            ${CMAKE_SOURCE_DIR}/include
            ${CMAKE_CURRENT_SOURCE_DIR}/${EXAMPLE_NAME}  # Example-specific headers
    )
    
    # Compiler options (more relaxed than main project)
    target_compile_options(${EXAMPLE_TARGET} 
        PRIVATE
            $<$<NOT:$<CXX_COMPILER_ID:MSVC>>:-Wall -Wextra>
            $<$<NOT:$<CXX_COMPILER_ID:MSVC>>:-Wno-unused-parameter>
            $<$<NOT:$<CXX_COMPILER_ID:MSVC>>:-Wno-unused-variable>
    )
    
    # Set C++ standard
    target_compile_features(${EXAMPLE_TARGET} PRIVATE cxx_std_${CMAKE_CXX_STANDARD})
    
    # Set output directory
    set_target_properties(${EXAMPLE_TARGET} PROPERTIES
        RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/examples
    )
    
    # Add to examples group
    set_target_properties(${EXAMPLE_TARGET} PROPERTIES FOLDER "Examples")
    
    message(STATUS "Added example: ${EXAMPLE_TARGET}")
endfunction()

# Auto-discover examples from subdirectories
foreach(EXAMPLE_DIR ${EXAMPLE_SUBDIRS})
    if(IS_DIRECTORY ${EXAMPLE_DIR})
        get_filename_component(EXAMPLE_NAME ${EXAMPLE_DIR} NAME)
        add_example(${EXAMPLE_NAME})
    endif()
endforeach()

# Also check for single-file examples in the current directory
file(GLOB SINGLE_FILE_EXAMPLES "${CMAKE_CURRENT_SOURCE_DIR}/*.cpp")
foreach(EXAMPLE_FILE ${SINGLE_FILE_EXAMPLES})
    get_filename_component(EXAMPLE_NAME ${EXAMPLE_FILE} NAME_WE)
    
    set(EXAMPLE_TARGET "example_${EXAMPLE_NAME}")
    
    add_executable(${EXAMPLE_TARGET} ${EXAMPLE_FILE})
    
    target_link_libraries(${EXAMPLE_TARGET} 
        PRIVATE 
            ${PROJECT_NAME}
            fmt::fmt
            spdlog::spdlog
    )
    
    target_include_directories(${EXAMPLE_TARGET} 
        PRIVATE 
            ${CMAKE_SOURCE_DIR}/include
    )
    
    target_compile_options(${EXAMPLE_TARGET} 
        PRIVATE
            $<$<NOT:$<CXX_COMPILER_ID:MSVC>>:-Wall -Wextra>
            $<$<NOT:$<CXX_COMPILER_ID:MSVC>>:-Wno-unused-parameter>
    )
    
    target_compile_features(${EXAMPLE_TARGET} PRIVATE cxx_std_${CMAKE_CXX_STANDARD})
    
    set_target_properties(${EXAMPLE_TARGET} PROPERTIES
        RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/examples
        FOLDER "Examples"
    )
    
    message(STATUS "Added single-file example: ${EXAMPLE_TARGET}")
endforeach()

# Custom target to build all examples
add_custom_target(examples 
    COMMENT "Building all examples"
)

# Get all example targets and add them as dependencies
get_property(ALL_TARGETS DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR} PROPERTY BUILDSYSTEM_TARGETS)
foreach(TARGET ${ALL_TARGETS})
    if(TARGET MATCHES "^example_")
        add_dependencies(examples ${TARGET})
    endif()
endforeach()

# Custom target to run all examples
add_custom_target(run_examples
    COMMENT "Running all examples"
    DEPENDS examples
)

# Add run commands for each example
foreach(TARGET ${ALL_TARGETS})
    if(TARGET MATCHES "^example_")
        add_custom_command(TARGET run_examples POST_BUILD
            COMMAND ${CMAKE_COMMAND} -E echo "Running ${TARGET}:"
            COMMAND $<TARGET_FILE:${TARGET}> || true
            COMMAND ${CMAKE_COMMAND} -E echo "---"
            WORKING_DIRECTORY ${CMAKE_BINARY_DIR}/examples
        )
    endif()
endforeach()

# Install examples (optional)
option(INSTALL_EXAMPLES "Install example executables" OFF)
if(INSTALL_EXAMPLES)
    foreach(TARGET ${ALL_TARGETS})
        if(TARGET MATCHES "^example_")
            install(TARGETS ${TARGET}
                RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}/examples
            )
        endif()
    endforeach()
endif()

# Print configuration
get_property(EXAMPLE_TARGETS DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR} PROPERTY BUILDSYSTEM_TARGETS)
list(FILTER EXAMPLE_TARGETS INCLUDE REGEX "^example_")
list(LENGTH EXAMPLE_TARGETS EXAMPLE_COUNT)

message(STATUS "Examples configuration:")
message(STATUS "  Found ${EXAMPLE_COUNT} examples")
message(STATUS "  Output directory: ${CMAKE_BINARY_DIR}/examples")
message(STATUS "  Install examples: ${INSTALL_EXAMPLES}")