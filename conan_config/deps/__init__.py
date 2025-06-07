import os
import pkgutil
import importlib

def _load_dependency_modules():
    package_path = os.path.dirname(__file__)
    module_names = [
        name for _, name, ispkg in pkgutil.iter_modules([package_path])
        if not name.startswith("_") and not ispkg
    ]

    modules = []
    for name in module_names:
        full_name = f"{__package__}.{name}"  # e.g. "conan.dependencies.boost"
        modules.append(importlib.import_module(full_name))
    return modules

def get_all_requires():
    return sum((m.requires() for m in _load_dependency_modules() if hasattr(m, "requires")), [])

def get_all_options():
    options = {}
    for m in _load_dependency_modules():
        if hasattr(m, "options"):
            options.update(m.options())
    return options