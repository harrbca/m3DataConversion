import importlib
import os
import inspect

# Dictionary to store registered views
registered_views = {}

def register_view(section, title, section_order=100, title_order=100):
    """
    Decorator to register a view dynamically with a specific menu structure.

    :param section: Name of the section (menu category)
    :param title: Name of the menu item
    :param section_order: Order of the section in the sidebar (lower = higher priority)
    :param title_order: Order of the title within the section (lower = higher priority)
    """
    def wrapper(cls):
        key = f"{section}::{title}" if title else section
        registered_views[key] = {
            "class" : cls,
            "section": section,
            "title": title,
            "section_order": section_order,
            "title_order": title_order
        }
        return cls
    return wrapper

def discover_views(directory="views"):
    """Scans a directory for Python files and imports them to register annotated views."""
    for filename in os.listdir(directory):
        if filename.endswith(".py") and filename != "__init__.py":
            module_name = f"{directory}.{filename[:-3]}"  # Convert to module format

            try:
                module = importlib.import_module(module_name)  # Import the module
                # Ensure the module's classes are actually registered
                for _, obj in inspect.getmembers(module):
                    if inspect.isclass(obj) and obj.__module__ == module.__name__:
                        pass  # Just forcing execution to load decorators
            except Exception as e:
                print(f"❌ Error loading {module_name}: {e}")
