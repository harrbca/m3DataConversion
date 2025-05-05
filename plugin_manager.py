import importlib
from transformers.mms200_transformer import MMS200Transformer
from transformers.mms200_addItmViaItmTyp_transformer import MMS200AddItmViaItmTypTransformer
from transformers.mms200_updItmBasic_transformer import MMS200UpdItmBasicTransformer
from transformers.mms015_transformer import MMS015Transformer
from transformers.crs025_transformer import CRS025Transformer
from transformers.crs035_transformer import CRS035Transformer
from transformers.crs099_transformer import CRS099Transformer
from transformers.crs610_add_transformer import CRS610AddTransformer
from transformers.mms200_updItmWhs_transformer import MMS200UpdItmWhsTransformer
from transformers.mms010_addLocation_transformer import MMS010AddLocationTransformer

DEFAULT_TRANSFORMERS = {
    "crs025": CRS025Transformer,
    "crs035": CRS035Transformer,
    "crs099": CRS099Transformer,
    "mms010_addLocation": MMS010AddLocationTransformer,
    "mms015": MMS015Transformer,
    "mms200": MMS200Transformer,
    "mms200_addItmViaItmTyp": MMS200AddItmViaItmTypTransformer,
    "mms200_updItmBasic": MMS200UpdItmBasicTransformer,
    "mms200_updItmWhs": MMS200UpdItmWhsTransformer,
    "crs610_add": CRS610AddTransformer
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
    default_class = DEFAULT_TRANSFORMERS.get(transformer_key)
    if default_class is None:
        raise ValueError(f"No default transformer found for key '{transformer_key}'")
    return default_class()