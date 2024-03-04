# -*- coding: utf-8 -*-
"""
Created on March 01, 2024

@author: mansour
"""
from operator import itemgetter
from re import fullmatch

from langchain.chat_models.base import BaseChatModel
from langchain.schema.runnable import Runnable, RunnableLambda

from chains.response.question_responser import get_responser
from chains.summarization.chat_summarizer import get_summarizer


def validate_history(history: str) -> str | None:
    if history:
        match = fullmatch(r"^(USER:\s+(.|\n)+)(\nBOT:\s+(.|\n)+\nUSER:\s+.+)?$", history)
        if not bool(match):
            raise ValueError(f"A malformed history was given. Got: {history}")
    return history


def build_discourse_chain(model: BaseChatModel) -> Runnable:
    return (
            {
                "question": itemgetter("question"),
                "history": itemgetter("history") | RunnableLambda(validate_history)
            }
            | get_summarizer(model)
            | get_responser(model)
    )
