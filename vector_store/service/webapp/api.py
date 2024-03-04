# -*- coding: utf-8 -*-
"""
Created on February 27, 2024

@author: mansour
"""

from fastapi import FastAPI

from service.webapp.v1.endpoints.add_endpoint import data_router as add_data_router
from service.webapp.v1.endpoints.clean_endpoint import data_router as clean_data_router
from service.webapp.v1.endpoints.retrieve_endpoint import data_router as retrieve_data_router
from service.webapp.v1.endpoints.save_endpoint import data_router as save_data_router

app = FastAPI()

app.include_router(add_data_router, prefix="/faiss", tags=["Faiss add docs."])
app.include_router(retrieve_data_router, prefix="/faiss", tags=["Faiss retrieve docs."])
app.include_router(save_data_router, prefix="/faiss", tags=["Faiss save vector store."])
app.include_router(clean_data_router, prefix="/faiss", tags=["Clean the vector store."])
