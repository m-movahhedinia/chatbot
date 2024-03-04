# -*- coding: utf-8 -*-
"""
Created on March 03, 2024

@author: mansour
"""

from uvicorn import run

from service.webapp.v1.api import app


if __name__ == "__main__":
    run(app, host="0.0.0.0", port=2023)
