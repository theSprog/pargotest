def requires():
    return ["spdlog/1.12.0"]

def options():
    return {
        "spdlog/*:shared": True,
    }