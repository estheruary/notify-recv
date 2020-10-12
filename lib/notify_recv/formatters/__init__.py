import pkgutil
import inspect
import os
from functools import reduce
from collections import defaultdict

from notify_recv.formatters.base import Formatter

class FormatPlugins(object):
    def __init__(self, search_package=__name__):
        self.search_package = search_package
        self.reload_plugins()
        self.formatters = map(lambda x: x(), self.plugins)
        self.formatters_lookup = reduce(lambda a, x: {**a, **{x.format_str: x}}, self.formatters, {})

    def reload_plugins(self):
        self.plugins = set()
        self.seen_paths = []
        self._walk_package(self.search_package)

    def get_plugins(self):
        return [*self.formatters_lookup]

    def get_plugin(self, formatter):
        return self.formatters_lookup[formatter]

    def _walk_package(self, package):
        imported_package = __import__(package, fromlist=['blah'])

        for _, pluginname, ispkg in pkgutil.iter_modules(imported_package.__path__, imported_package.__name__ + '.'):
            if not ispkg:
                plugin_module = __import__(pluginname, fromlist=['blah'])
                clsmembers = inspect.getmembers(plugin_module, inspect.isclass)
                for (_, c) in clsmembers:
                    if issubclass(c, Formatter) & (c is not Formatter):
                        self.plugins.add(c)

        all_current_paths = []
        if isinstance(imported_package.__path__, str):
            all_current_paths.append(imported_package.__path__)
        else:
            all_current_paths.extend([x for x in imported_package.__path__])

        for pkg_path in all_current_paths:
            if pkg_path not in self.seen_paths:
                self.seen_paths.append(pkg_path)

                # Get all subdirectory of the current package path directory
                child_pkgs = [p for p in os.listdir(pkg_path) if os.path.isdir(os.path.join(pkg_path, p))]

                # For each subdirectory, apply the walk_package method recursively
                for child_pkg in child_pkgs:
                    self._walk_package(package + '.' + child_pkg)
