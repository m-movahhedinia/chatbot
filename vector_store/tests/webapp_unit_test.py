# -*- coding: utf-8 -*-
"""
Created on February 27, 2024

@author: mansour
"""

from service.webapp.api import app
from pytest import fixture, mark
from fastapi.testclient import TestClient


@fixture
def client():
    return TestClient(app)


@mark.order(200)
def test_add_endpoint(client):
    docs = {"docs": [{"page_content": x, "metadata": {y: y}} for y, x in
                     enumerate(["this is a test", "this is also a test", "even this", "mind blowing! This as well!"])]}
    response = client.put("/faiss/add", json=docs)
    assert response.status_code == 201
    assert response.json() == {'requested_docs': 4, 'status': True}


@mark.order(201)
def test_retrieve_endpoint(client):
    response = client.post("/faiss/retrieve", json={"query": "Which is the test?"})
    assert response.status_code == 200
    assert response.json() == {'status': True, 'query': 'Which is the test?',
                               'docs': [{'page_content': 'this is a test', 'metadata': {}, 'type': 'Document'},
                                        {'page_content': 'this is also a test', 'metadata': {}, 'type': 'Document'},
                                        {'page_content': 'even this', 'metadata': {}, 'type': 'Document'},
                                        {'page_content': 'mind blowing! This as well!', 'metadata': {},
                                         'type': 'Document'}]}


@mark.order(202)
def test_save_endpoint(client):
    response = client.get("/faiss/save")
    assert response.status_code == 200
    assert response.json() == {"status": True}


@mark.order(203)
def test_clean_endpoint(client):
    response = client.post("/faiss/clean", json={"everything": True})
    assert response.status_code == 200
    assert response.json() == {"status": True}
