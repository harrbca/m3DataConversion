import importlib
from transformers.mms200_transformer import MMS200Transformer
from transformers.crs025_transformer import CRS025Transformer
from transformers.crs035_transformer import CRS035Transformer
from transformers.crs099_transformer import CRS099Transformer

DEFAULT_TRANSFORMERS = {
    "crs025": CRS025Transformer,
    "crs035": CRS035Transformer,
    "crs099": CRS099Transformer,
    "mms200": MMS200Transformer
}

def load_transformer(transformer_key, plugin_path=None):
    """
    Load a transformer class from a plugin path.
    """
    if plugin_path:
        module_name, class_name = plugin_path.rsplit('.', 1)
        plugin_module = importlib.import_module(module_name)
        plugin_class = getattr(plugin_module, class_name)
        return plugin_class()  # instantiate the custom

    # Otherwise, return the default from our dictionary
    default_class = DEFAULT_TRANSFORMERS.get(transformer_key.lower())
    if default_class is None:
        raise ValueError(f"No default transformer found for key '{transformer_key}'")
    return default_class()