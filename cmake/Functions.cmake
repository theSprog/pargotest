# ---------------------------------------------------------
# log 相关函数

# 支持的日志等级: ERROR > WARN > INFO > DEBUG
set_property(GLOBAL PROPERTY LOG_LEVEL ${LOG_LEVEL})

# 定义 ANSI 颜色码变量
string(ASCII 27 ESC)
set(COLOR_RED "${ESC}[1;31m")
set(COLOR_YELLOW "${ESC}[1;33m") 
set(COLOR_CYAN "${ESC}[1;36m")
set(COLOR_MAGENTA "${ESC}[1;35m")
set(COLOR_GRAY "${ESC}[1;90m")
set(COLOR_RESET "${ESC}[0m")

function(set_log_level level)
    string(TOUPPER "${level}" level)
    set_property(GLOBAL PROPERTY LOG_LEVEL "${level}")
endfunction()

function(log level msg)
    string(TOUPPER "${level}" level)
    get_property(current_level GLOBAL PROPERTY LOG_LEVEL)

    # 日志等级优先级(数字越大,权限越大)
    set(LOG_LEVELS DEBUG INFO WARN ERROR)
    list(FIND LOG_LEVELS "${level}" level_priority)
    list(FIND LOG_LEVELS "${current_level}" current_priority)

    # 若当前等级允许输出
    if(level_priority GREATER_EQUAL current_priority)
        # ANSI 颜色
        if(level STREQUAL "ERROR")
            set(color "${COLOR_RED}")
        elseif(level STREQUAL "WARN")
            set(color "${COLOR_YELLOW}")
        elseif(level STREQUAL "INFO")
            set(color "${COLOR_CYAN}")
        elseif(level STREQUAL "DEBUG")
            set(color "${COLOR_GRAY}")
        else()
            set(color "${COLOR_RESET}")
        endif()

        # 输出
        message(STATUS "${color}[${level}] ${msg}${COLOR_RESET}")
    endif()
endfunction()

# ---------------------------------------------------------