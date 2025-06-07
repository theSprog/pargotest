from conan import ConanFile
from conan.tools.cmake import CMake, CMakeToolchain, CMakeDeps
from conan_config.deps import get_all_requires, get_all_options

class twoConan(ConanFile):
    name = "two"
    version = "0.0.1"

    settings = "os", "compiler", "build_type", "arch"

    requires = get_all_requires()
    default_options = get_all_options()

    exports_sources = "src/*", "CMakeLists.txt"

    # conan install . --output-folder=build --build=missing -s build_type={Debug|Release}
    def layout(self):
        self.folders.generators = "conan"  # Conan generator-file are placed in `build/conan`
        self.folders.build = "."             # CMake build are placed in `build/`

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = ["two"]

    def generate(self):
        tc = CMakeToolchain(self)
        tc.generate()

        deps = CMakeDeps(self)
        deps.generate()