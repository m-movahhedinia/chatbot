# -*- coding: utf-8 -*-
"""
Created on March 03, 2024

@author: mansour
"""

from operator import itemgetter
from pathlib import Path

from langchain.chat_models.base import BaseChatModel
from langchain.output_parsers.json import SimpleJsonOutputParser
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnableLambda
from requests import post

from chains.commons.exceptions import RetrievalFailedException
from constants.configs import PROMPT_TEMPLATE_DIR, VECTOR_STORE_RETRY_ATTEMPTS, VECTOR_STORE_URL, log


def process_documents(docs: list):
    return "\n".join(doc["page_content"] for doc in docs)


def query_vector_store(data: dict):
    headers = {
        'Content-Type': 'application/json'
    }
    attempt = 0
    while attempt < VECTOR_STORE_RETRY_ATTEMPTS:
        try:
            response = post(VECTOR_STORE_URL, headers=headers, json={"query": data["new_question"]})
            if response.status_code == 200:
                context = process_documents(response.json()["docs"])
                return {"context": context, "question": data["new_question"]}
            else:
                response.raise_for_status()
        except Exception as e:
            log.warning(f"Failed to query vector store. Got: {e}")
            attempt += 1
    else:
        raise RetrievalFailedException(f"Couldn't query the vector store after {VECTOR_STORE_RETRY_ATTEMPTS} attempts.")


def get_responser(model: BaseChatModel):
    prompt_template = Path(PROMPT_TEMPLATE_DIR).joinpath("chat_prompt_template.jinja2").open().read()

    response_prompt = ChatPromptTemplate.from_template(prompt_template, template_format="jinja2",
                                                       validate_template=False)
    return (
            {
                "question": itemgetter("question"),
                "history": itemgetter("history"),
                "new_question": itemgetter("new_question")
            }
            | RunnableLambda(query_vector_store) | response_prompt | model | SimpleJsonOutputParser()
    )
