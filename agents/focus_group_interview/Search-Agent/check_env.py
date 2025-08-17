import sys
import pkg_resources

print("Python version:", sys.version)
print("Python executable:", sys.executable)
print("sys.path:", sys.path)

installed_packages = {pkg.key for pkg in pkg_resources.working_set}
print("youtube-search-python installed:", "youtube-search-python" in installed_packages)
