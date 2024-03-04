# -*- coding: utf-8 -*-
"""
Created on March 01, 2024

@author: mansour
"""

from operator import itemgetter
from pathlib import Path

from langchain.chat_models.base import BaseChatModel
from langchain.output_parsers.json import SimpleJsonOutputParser
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnablePassthrough

from constants.configs import PROMPT_TEMPLATE_DIR


def get_summarizer(model: BaseChatModel):
    prompt_template = Path(PROMPT_TEMPLATE_DIR).joinpath("summarization_prompt_template.jinja2").open().read()

    summarization_prompt = ChatPromptTemplate.from_template(prompt_template, template_format="jinja2",
                                                            validate_template=False)
    return (
            {
                "question": itemgetter("question"),
                "history": itemgetter("history"),
                "new_question": summarization_prompt | model | SimpleJsonOutputParser(),
            }
            | RunnablePassthrough()
    )
