# -*- coding: utf-8 -*-
"""
Created on February 28, 2024

@author: mansour
"""

from os import environ
from logging import getLogger, INFO

log = getLogger(__name__)
log.setLevel(INFO)

# ========== Default values ==========
_DEFAULT_BATCH_SIZE = 5
_DEFAULT_CHUNK_SIZE = 1000
_DEFAULT_OVERLAP = 200
_DEFAULT_VECTOR_STORE = "http://0.0.0.0:2024/faiss/add"
_DEFAULT_VECTOR_STORE_RETRY_ATTEMPTS = 10
_DEFAULT_WAIT_TIME = 3
_DEFAULT_RENDER_HEADLESS = True

# ========== Configured values ==========
BATCH_SIZE = environ.get("BATCH_SIZE", _DEFAULT_BATCH_SIZE)
CHUNK_SIZE = environ.get("CHUNK_SIZE", _DEFAULT_CHUNK_SIZE)
CHUNK_OVERLAP = environ.get("CHUNK_OVERLAP", _DEFAULT_OVERLAP)
VECTOR_STORE = environ.get("VECTOR_STORE", _DEFAULT_VECTOR_STORE)
VECTOR_STORE_RETRY_ATTEMPTS = environ.get("VECTOR_STORE_RETRY_ATTEMPTS", _DEFAULT_VECTOR_STORE_RETRY_ATTEMPTS)
WAIT_TIME = environ.get("WAIT_TIME", _DEFAULT_WAIT_TIME)
RENDER_HEADLESS = environ.get("RENDER_HEADLESS", _DEFAULT_RENDER_HEADLESS)
