# -*- coding: utf-8 -*-
"""
Created on February 27, 2024

@author: mansour
"""

from constants.configs import log

try:
    from langchain_openai import OpenAIEmbeddings

    models_embeddings = {"text-embedding-ada-002": OpenAIEmbeddings,
                         "text-embedding-3-small": OpenAIEmbeddings,
                         "text-embedding-3-large": OpenAIEmbeddings}
except Exception as e:
    log.error(f"Failed at loading OpenAI embeddings. Got:\n {e}")
