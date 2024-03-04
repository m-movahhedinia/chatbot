# -*- coding: utf-8 -*-
"""
Created on February 27, 2024

@author: mansour
"""

from constants.configs import log

try:
    from langchain_together import TogetherEmbeddings

    models_embeddings = {"UAE-Large-v1": TogetherEmbeddings,
                         "BGE-Large-EN-v1.5": TogetherEmbeddings}
except Exception as e:
    log.error(f"Failed at loading TogetherAI embeddings. Got:\n {e}")
