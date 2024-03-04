# -*- coding: utf-8 -*-
"""
Created on March 03, 2024

@author: mansour
"""

from typing import Optional

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from langchain_openai import ChatOpenAI
from pydantic import BaseModel

from chains.discussant import build_discourse_chain
from constants.configs import GENERATIVE_MODEL, MODEL_TEMPERATURE, log

conversation_function = build_discourse_chain(ChatOpenAI(model=GENERATIVE_MODEL, temperature=MODEL_TEMPERATURE))

conversation_router = APIRouter()


class ConversationPayload(BaseModel):
    question: str
    history: Optional[str] = None


@conversation_router.post("/ask")
async def converse(payload: ConversationPayload):
    try:
        log.info("Generating response.")
        response = conversation_function.invoke({"question": payload.question, "history": payload.history})
        result = JSONResponse(content=response, status_code=200)
    except Exception as e:
        raise e
        # log.error(e)
        # result = JSONResponse(content={"status": False}, status_code=500)

    return result
