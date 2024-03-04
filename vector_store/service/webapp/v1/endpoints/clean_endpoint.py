# -*- coding: utf-8 -*-
"""
Created on February 27, 2024

@author: mansour
"""

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from constants.configs import log
from service.webapp.v1.storage.faiss_vector_store import Faiss

data_router = APIRouter()


class CleanVectorStore(BaseModel):
    everything: bool


@data_router.post("/clean")
async def clean_docs(payload: CleanVectorStore):
    try:
        Faiss.clean(payload.everything)
        result = JSONResponse(content={"status": True}, status_code=200)
        log.info(f"Vector store cleaned, {'' if payload.everything else 'not'} including local files.")
    except Exception as e:
        log.error(e)
        result = JSONResponse(content={"status": False}, status_code=500)

    return result
