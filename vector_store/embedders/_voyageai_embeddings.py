# -*- coding: utf-8 -*-
"""
Created on February 27, 2024

@author: mansour
"""

from constants.configs import log

try:
    from langchain_community.embeddings import VoyageEmbeddings

    models_embeddings = {"voyage-lite-02-instruct": VoyageEmbeddings}
except Exception as e:
    log.error(f"Failed at loading VoyageAI embeddings. Got:\n {e}")
