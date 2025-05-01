import importlib
from strategies.defaut_item_number_strategy import DefaultItemNumberStrategy
from config_reader import ConfigReader

def load_item_number_strategy():
    config = ConfigReader.get_instance().config

    strategy_path = config.get("STRATEGIES", "item_number_strategy", fallback=None)

    if not strategy_path:
        return DefaultItemNumberStrategy()

    try:
        module_path, class_name = strategy_path.rsplit(".", 1)
        module = importlib.import_module(module_path)
        strategy_class = getattr(module, class_name)
        return strategy_class()
    except Exception as e:
        print(f"[WARN] Failed to load item number strategy '{strategy_path}': {e}")
        return DefaultItemNumberStrategy()