def requires():
    return ["fmt/10.2.1"]

def options():
    return {
        "fmt/*:shared": True,
    }