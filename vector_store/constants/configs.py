# -*- coding: utf-8 -*-
"""
Created on February 27, 2024

@author: mansour
"""

from os import environ
from logging import getLogger, INFO

log = getLogger(__name__)
log.setLevel(INFO)

# ========== Default values ==========
_DEFAULT_EMBEDDING_MODEL = "text-embedding-ada-002"
_DEFAULT_INDEX_NAME = "autodesk"
_DEFAULT_VECTOR_STORE_K = 10

# ========== Configured values ==========
EMBEDDING_MODEL = environ.get("EMBEDDING_MODEL", _DEFAULT_EMBEDDING_MODEL)
INDEX_NAME = environ.get("INDEX_NAME", _DEFAULT_INDEX_NAME)
VECTOR_STORE_K = environ.get("VECTOR_STORE_K", _DEFAULT_VECTOR_STORE_K)

# ========== Temporary local configs ==========
# This is used for local configs only.
# from constants.local_configs import setup_local_secrets

# setup_local_secrets()
