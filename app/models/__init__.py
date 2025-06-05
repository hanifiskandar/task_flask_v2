import os
import importlib

# Get current directory
models_dir = os.path.dirname(__file__)

# Loop through each .py file that isn't __init__.py
for filename in os.listdir(models_dir):
    if filename.endswith(".py") and filename != "__init__.py":
        module_name = f"{__name__}.{filename[:-3]}"
        importlib.import_module(module_name)

# Explicitly expose classes you want to import directly
from .task import Task
from .user import User