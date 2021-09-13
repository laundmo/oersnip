import importlib

module_names = [
    "environ",
    "clipboard",
    "datetime"
]

envs = {}

for module in module_names:
    try:
        mod = importlib.import_module("." + module, "environments")
    except ImportError as e:
        print(e)
    else:
        envs[module] = mod
