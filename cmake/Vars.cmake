if(NOT DEFINED LOG_LEVEL)
    # 确保 build type 有值
    if(NOT CMAKE_BUILD_TYPE)
        set(CMAKE_BUILD_TYPE "Release")  # 默认构建类型
    endif()

    string(TOUPPER "${CMAKE_BUILD_TYPE}" _bt)

    if(_bt STREQUAL "DEBUG" OR _bt STREQUAL "RELWITHDEBINFO")
        set(LOG_LEVEL "DEBUG")
    else()
        set(LOG_LEVEL "INFO")
    endif()
endif()