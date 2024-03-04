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


class RetrieveDocs(BaseModel):
    query: str


@data_router.post("/retrieve")
async def retrieve_docs(payload: RetrieveDocs):
    try:
        docs = Faiss.retrieve_documents(payload.query)
        result = JSONResponse(content={"status": True, "query": payload.query, "docs": docs}, status_code=200)
        log.info(f"Retrieved {docs} for {payload.query}")
    except Exception as e:
        raise e
        log.error(e)
        result = JSONResponse(content={"status": False, "query": payload.query, "docs": None}, status_code=500)

    return result
