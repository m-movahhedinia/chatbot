# -*- coding: utf-8 -*-
"""
Created on February 27, 2024

@author: mansour
"""

from importlib.util import spec_from_file_location, module_from_spec
from pathlib import Path

_local_space = Path(__file__).parent.resolve()

embedding_models = {}

for file in _local_space.glob("*.py"):
    if file.stem.endswith("_embeddings") and not file.name.startswith("__"):
        spec = spec_from_file_location(file.with_suffix("").as_posix(), file)
        module = module_from_spec(spec)
        spec.loader.exec_module(module)
        embedding_models.update(module.models_embeddings)
