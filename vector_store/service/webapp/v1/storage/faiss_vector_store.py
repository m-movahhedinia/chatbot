# -*- coding: utf-8 -*-
"""
Created on February 27, 2024

@author: mansour
"""

from hashlib import sha256
from pathlib import Path
from typing import Dict, List, Type

from langchain.schema import Document
from langchain_community.vectorstores.faiss import FAISS as _FAISS
from langchain_community.vectorstores.utils import DistanceStrategy
from langchain_core.embeddings import Embeddings

from constants.configs import EMBEDDING_MODEL, VECTOR_STORE_K, log
from embedders import embedding_models


class Faiss:
    storage: _FAISS = None
    retriever = None
    embeddings: Embeddings = None
    local_file: Path = Path(__file__).parent.joinpath("local", "faiss_vectors")

    @staticmethod
    def set_embeddings(model: str = None) -> Type["Faiss"]:
        if Faiss.embeddings is None:
            Faiss.embeddings = embedding_models[model or EMBEDDING_MODEL]()
        return Faiss

    @staticmethod
    def set_retriever() -> Type["Faiss"]:
        if Faiss.storage is None:
            Faiss.load()

        if Faiss.retriever is None:
            Faiss.retriever = Faiss.storage.as_retriever(search_kwargs={"k": VECTOR_STORE_K},
                                                         return_source_documents=True)

        return Faiss

    @staticmethod
    async def add_documents(documents: List[Document | Dict]):
        if isinstance(documents[0], dict):
            documents = [Document(page_content=document["page_content"],
                                  metadata=document.get("metadata", {})) for document in documents]
        ids = Faiss._get_ids(documents)
        documents, ids = Faiss._dedupe_documents(documents, ids)
        if Faiss.storage is None:
            Faiss.storage = await _FAISS.afrom_documents(documents=documents, ids=ids, embedding=Faiss.embeddings,
                                                         distance_strategy=DistanceStrategy.EUCLIDEAN_DISTANCE)
        else:
            uniques_ids = [idx for idx, id_ in enumerate(ids) if id_ not in Faiss.storage.index_to_docstore_id.values()]
            ids = [ids[idx] for idx in uniques_ids]
            documents = [documents[idx] for idx in uniques_ids]
            if ids:
                await Faiss.storage.aadd_documents(documents=documents, ids=ids, embedding=Faiss.embeddings)

    @staticmethod
    def _get_ids(documents: List[Document]) -> List[str]:
        return [sha256(document.page_content.encode("utf-8")).hexdigest() for document in documents]

    @staticmethod
    def retrieve_documents(query):
        result = [document.dict() for document in Faiss.set_retriever().retriever.invoke(query)]
        return result

    @staticmethod
    def load():
        if Faiss.local_file.joinpath("index.faiss").is_file() and Faiss.local_file.joinpath("index.pkl").is_file():
            Faiss.set_embeddings()
            Faiss.storage = _FAISS.load_local(Faiss.local_file.as_posix(), Faiss.embeddings)
        else:
            raise FileNotFoundError(f"Could not load the vector store from {Faiss.local_file.as_posix()}")

    @staticmethod
    def save():
        Faiss.local_file.parent.mkdir(parents=True, exist_ok=True)
        if Faiss.storage is not None:
            Faiss.storage.save_local(Faiss.local_file.as_posix())

    @staticmethod
    def clean(everything: bool = True):

        if everything:
            Faiss.local_file.joinpath("index.faiss").unlink(missing_ok=True)
            Faiss.local_file.joinpath("index.pkl").unlink(missing_ok=True)

        try:
            Faiss.storage.delete(list(Faiss.storage.index_to_docstore_id.values()))
        except ValueError as e:
            log.info(f"The vector store is empty. Nothing to delete. Got: {e}")

    @staticmethod
    def _dedupe_documents(documents: List[Document], ids: List[str]):
        unique_indices = sorted({s: i for i, s in enumerate(ids)}.values())
        return zip(*[(documents[i], ids[i]) for i in unique_indices])

