import importlib.metadata

def is_package_installed(package_name):
    """ Check for the distribution package. """

    try:
        importlib.metadata.version(package_name)
        return True
    except importlib.metadata.PackageNotFoundError:
        return False