# Find required tools
find_package(Doxygen REQUIRED dot)
find_program(SPHINX_BUILD sphinx-build REQUIRED)

# Documentation configuration
set(DOCS_SOURCE_DIR ${CMAKE_CURRENT_SOURCE_DIR})
set(DOCS_BUILD_DIR ${CMAKE_CURRENT_BINARY_DIR})
set(DOXYGEN_OUTPUT_DIR ${DOCS_BUILD_DIR}/doxygen)
set(SPHINX_OUTPUT_DIR ${DOCS_BUILD_DIR}/sphinx)

# Doxygen configuration
set(DOXYGEN_INPUT_DIR ${CMAKE_SOURCE_DIR}/include ${CMAKE_SOURCE_DIR}/src)
set(DOXYGEN_CONFIG_FILE ${DOCS_SOURCE_DIR}/Doxyfile.in)
set(DOXYGEN_CONFIG_OUTPUT ${DOCS_BUILD_DIR}/Doxyfile)

# Configure Doxygen
configure_file(${DOXYGEN_CONFIG_FILE} ${DOXYGEN_CONFIG_OUTPUT} @ONLY)

# Doxygen target
add_custom_target(doxygen
    COMMAND ${DOXYGEN_EXECUTABLE} ${DOXYGEN_CONFIG_OUTPUT}
    WORKING_DIRECTORY ${DOCS_BUILD_DIR}
    COMMENT "Generating API documentation with Doxygen"
    VERBATIM
)

# Sphinx target
add_custom_target(sphinx
    COMMAND ${SPHINX_BUILD} -b html 
            -D breathe_projects.${PROJECT_NAME}=${DOXYGEN_OUTPUT_DIR}/xml
            ${DOCS_SOURCE_DIR} ${SPHINX_OUTPUT_DIR}
    WORKING_DIRECTORY ${DOCS_BUILD_DIR}
    DEPENDS doxygen
    COMMENT "Generating documentation with Sphinx"
    VERBATIM
)

# Combined documentation target
add_custom_target(docs
    DEPENDS sphinx
    COMMENT "Building complete documentation"
)

# Clean documentation
add_custom_target(docs_clean
    COMMAND ${CMAKE_COMMAND} -E remove_directory ${DOXYGEN_OUTPUT_DIR}
    COMMAND ${CMAKE_COMMAND} -E remove_directory ${SPHINX_OUTPUT_DIR}
    COMMENT "Cleaning documentation build files"
)

# Open documentation in browser (optional)
if(CMAKE_SYSTEM_NAME STREQUAL "Linux")
    set(BROWSER_COMMAND xdg-open)
elseif(CMAKE_SYSTEM_NAME STREQUAL "Darwin")
    set(BROWSER_COMMAND open)
elseif(CMAKE_SYSTEM_NAME STREQUAL "Windows")
    set(BROWSER_COMMAND cmd /c start)
endif()

if(BROWSER_COMMAND)
    add_custom_target(docs_open
        COMMAND ${BROWSER_COMMAND} ${SPHINX_OUTPUT_DIR}/index.html
        DEPENDS docs
        COMMENT "Opening documentation in browser"
    )
endif()

# Install documentation
option(INSTALL_DOCS "Install documentation" ON)
if(INSTALL_DOCS)
    install(DIRECTORY ${SPHINX_OUTPUT_DIR}/
        DESTINATION ${CMAKE_INSTALL_DOCDIR}
        OPTIONAL
        MESSAGE_NEVER
    )
endif()

# Print configuration
message(STATUS "Documentation configuration:")
message(STATUS "  Doxygen: ${DOXYGEN_EXECUTABLE}")
message(STATUS "  Sphinx: ${SPHINX_BUILD}")
message(STATUS "  Output directory: ${SPHINX_OUTPUT_DIR}")
message(STATUS "  Install docs: ${INSTALL_DOCS}")