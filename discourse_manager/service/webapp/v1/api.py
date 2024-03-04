# -*- coding: utf-8 -*-
"""
Created on March 03, 2024

@author: mansour
"""

from fastapi import FastAPI
from constants.configs import WEBAPP_VERSION

from service.webapp.v1.conversation_endpoint import conversation_router

app = FastAPI(
        title="Chatter desk",
        version=WEBAPP_VERSION,
        description="A fun chatbot!"
)


app.include_router(conversation_router, prefix="/converse", tags=["Conversation endpoint"])
