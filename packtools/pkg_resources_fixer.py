

def get_version(package_name):
    """
    Get the version of a package.

    Args:
        package_name (str): The name of the package.

    Returns:
        str: The version of the package.
        
    # Antes
    from pkg_resources import get_distribution
    version = get_distribution("meu-pacote").version

    # Depois
    from importlib.metadata import version
    version = version("meu-pacote")
    """
    try:
        from importlib.metadata import version
        return version(package_name)
    except ImportError:
        import pkg_resources
        try:
            return pkg_resources.get_distribution(package_name).version
        except pkg_resources.DistributionNotFound:
            return None
    except Exception:
        return None        


def get_iter_entry_points(group, name=None):
    """
    Get the entry points for a given group and name.

    Args:
        group (str): The group of the entry points.
        name (str, optional): The name of the entry points. Defaults to None.

    # Antes
    from pkg_resources import iter_entry_points
    for ep in iter_entry_points("console_scripts"):
        print(ep.name, ep.load())

    # Depois
    from importlib.metadata import entry_points

    # Python 3.10+
    eps = entry_points(group="console_scripts")

    # Python 3.9
    eps = entry_points().get("console_scripts", [])
    """
    try:
        from importlib.metadata import entry_points
        return entry_points(group=group)
    except ImportError:
        from pkg_resources import iter_entry_points
        return iter_entry_points(group=group, name=None)