# -*- coding: utf-8 -*-
"""
Created on February 27, 2024

@author: mansour
"""

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from constants.configs import log
from service.webapp.v1.storage.faiss_vector_store import Faiss

data_router = APIRouter()


@data_router.get("/save")
async def retrieve_docs():
    try:
        Faiss.save()
        result = JSONResponse(content={"status": True}, status_code=200)
        log.info(f"Saved vector store.")
    except Exception as e:
        log.error(e)
        result = JSONResponse(content={"status": False}, status_code=500)

    return result
