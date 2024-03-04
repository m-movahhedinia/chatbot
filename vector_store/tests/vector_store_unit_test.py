# -*- coding: utf-8 -*-
"""
Created on February 27, 2024

@author: mansour
"""

from hashlib import sha256
from unittest.mock import Mock

from pytest import mark

from service.webapp.v1.storage.faiss_vector_store import Faiss


@mark.order(100)
def test_faiss_unset():
    assert Faiss.storage == Faiss.retriever == Faiss.embeddings is None
    # assert Faiss.local_file.as_posix() == ""


@mark.order(101)
def test_faiss_set_embeddings():
    Faiss.set_embeddings()
    assert Faiss.embeddings is not None


@mark.order(102)
def test_faiss_get_ids():
    texts = ["this is a test", "this is also a test", "even this", "mind blowing! This as well!"]
    expected = [sha256(text.encode("utf-8")).hexdigest() for text in texts]
    mocked_docs = [Mock(spec=[], page_content=text) for text in texts]

    actual = Faiss._get_ids(mocked_docs)
    assert actual == expected


@mark.order(103)
@mark.asyncio
async def test_faiss_upsert_documents():
    assert Faiss.storage is None
    texts = ["this is a test", "this is also a test", "even this", "mind blowing! This as well!"]
    mocked_docs = [Mock(spec=[], page_content=text, metadata={}) for text in texts]
    await Faiss.set_embeddings().add_documents(mocked_docs)
    assert Faiss.storage is not None
    doc = await Faiss.storage.asimilarity_search("Which is the test?")
    assert doc[0].page_content == "this is a test"


@mark.order(104)
def test_faiss_set_retriever():
    assert Faiss.retriever is None
    Faiss.set_retriever()
    assert Faiss.retriever is not None


@mark.order(105)
def test_faiss_retrieve_documents():
    doc = Faiss.retrieve_documents("Which is the test?")
    assert doc == [{'metadata': {}, 'page_content': 'this is a test', 'type': 'Document'},
                   {'metadata': {}, 'page_content': 'this is also a test', 'type': 'Document'},
                   {'metadata': {}, 'page_content': 'even this', 'type': 'Document'},
                   {'metadata': {}, 'page_content': 'mind blowing! This as well!', 'type': 'Document'}]


@mark.order(106)
def test_faiss_save():
    assert not Faiss.local_file.joinpath("index.faiss").is_file()
    Faiss.save()
    assert Faiss.local_file.joinpath("index.faiss").is_file()
    assert Faiss.local_file.joinpath("index.pkl").is_file()


@mark.order(107)
def test_faiss_load():
    Faiss.storage = None
    assert Faiss.storage is None
    Faiss.load()
    assert Faiss.storage is not None
    doc = Faiss.retrieve_documents("Which is the test?")
    assert doc == [{'metadata': {}, 'page_content': 'this is a test', 'type': 'Document'},
                   {'metadata': {}, 'page_content': 'this is also a test', 'type': 'Document'},
                   {'metadata': {}, 'page_content': 'even this', 'type': 'Document'},
                   {'metadata': {}, 'page_content': 'mind blowing! This as well!', 'type': 'Document'}]


@mark.order(108)
def test_faiss_clean():
    assert Faiss.local_file.joinpath("index.faiss").is_file()
    assert Faiss.local_file.joinpath("index.pkl").is_file()
    doc = Faiss.retrieve_documents("Which is the test?")
    assert doc == [{'metadata': {}, 'page_content': 'this is a test', 'type': 'Document'},
                   {'metadata': {}, 'page_content': 'this is also a test', 'type': 'Document'},
                   {'metadata': {}, 'page_content': 'even this', 'type': 'Document'},
                   {'metadata': {}, 'page_content': 'mind blowing! This as well!', 'type': 'Document'}]
    Faiss.clean(False)
    assert Faiss.local_file.joinpath("index.faiss").is_file()
    assert Faiss.local_file.joinpath("index.pkl").is_file()


@mark.order(109)
def test_faiss_clean_everything():
    assert Faiss.local_file.joinpath("index.faiss").is_file()
    assert Faiss.local_file.joinpath("index.pkl").is_file()
    Faiss.clean()
    assert not Faiss.local_file.joinpath("index.faiss").is_file()
    assert not Faiss.local_file.joinpath("index.pkl").is_file()
