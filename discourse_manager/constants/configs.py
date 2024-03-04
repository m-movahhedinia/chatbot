# -*- coding: utf-8 -*-
"""
Created on March 03, 2024

@author: mansour
"""

from logging import INFO, getLogger
from os import environ
from pathlib import Path

log = getLogger(__name__)
log.setLevel(INFO)

# ========== Default values ==========
_DEFAULT_VECTOR_STORE_URL = "http://0.0.0.0:2024/faiss/retrieve"
_DEFAULT_VECTOR_STORE_RETRY_ATTEMPTS = 3
_DEFAULT_PROMPT_TEMPLATE_DIR = Path().cwd().joinpath("chains", "commons", "prompt_templates").as_posix()
_DEFAULT_GENERATIVE_MODEL = "gpt-4-1106-preview"
_DEFAULT_MODEL_TEMPERATURE = 0
_DEFAULT_WEBAPP_VERSION = "0.0.1r"

# ========== Configured values ==========
VECTOR_STORE_URL = environ.get("VECTOR_STORE_URL", _DEFAULT_VECTOR_STORE_URL)
VECTOR_STORE_RETRY_ATTEMPTS = environ.get("VECTOR_STORE_RETRY_ATTEMPTS", _DEFAULT_VECTOR_STORE_RETRY_ATTEMPTS)
PROMPT_TEMPLATE_DIR = environ.get("PROMPT_TEMPLATE_DIR", _DEFAULT_PROMPT_TEMPLATE_DIR)
GENERATIVE_MODEL = environ.get("GENERATIVE_MODEL", _DEFAULT_GENERATIVE_MODEL)
MODEL_TEMPERATURE = environ.get("MODEL_TEMPERATURE", _DEFAULT_MODEL_TEMPERATURE)
WEBAPP_VERSION = environ.get("WEBAPP_VERSION", _DEFAULT_WEBAPP_VERSION)

# ========== Temporary local configs ==========
from constants.local_configs import setup_local_secrets

setup_local_secrets()
