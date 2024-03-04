# -*- coding: utf-8 -*-
"""
Created on February 27, 2024

@author: mansour
"""

from typing import Dict, List

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from constants.configs import log
from service.webapp.v1.storage.faiss_vector_store import Faiss

data_router = APIRouter()


class AddVector(BaseModel):
    docs: List[Dict]


@data_router.put("/add")
async def add_vector(payload: AddVector):
    try:
        await Faiss.set_embeddings().add_documents(payload.docs)
        log.info(f"Added {len(payload.docs)} documents to the vector store.")
        result = JSONResponse(content={"status": True}, status_code=201)

    except Exception as e:
        raise e
        # log.error(e)
        # result = JSONResponse(content={"status": False}, status_code=500)

    return result
