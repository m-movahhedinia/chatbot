# -*- coding: utf-8 -*-
"""
Created on February 28, 2024

@author: mansour
"""

from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from functools import partial
from pathlib import Path
from re import compile, sub
from time import sleep
from typing import Dict, List

from bs4 import BeautifulSoup
from constants.configs import (BATCH_SIZE, CHUNK_OVERLAP, CHUNK_SIZE, RENDER_HEADLESS, VECTOR_STORE,
                               VECTOR_STORE_RETRY_ATTEMPTS, WAIT_TIME, log)
from ingesters.exceptions import NoBodyException
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders.base import BaseLoader
from requests import put
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from tqdm import tqdm


class HTMLIngester(BaseLoader):
    def __init__(self, files_path: str):
        super().__init__()

        self.files = list(Path(files_path).glob("*.html"))
        self.batches = [self.files[i:i + BATCH_SIZE] for i in range(0, len(self.files), BATCH_SIZE)]
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
        self.docs = []

    def concurrent_load(self) -> "HTMLIngester":
        loader_func = partial(self.load_webpage, splitter=self.text_splitter)
        with ProcessPoolExecutor() as executor:
            self.docs = list(tqdm(executor.map(loader_func, self.batches), total=len(self.batches),
                                  desc="Content loading"))
        return self

    def load(self) -> "HTMLIngester":
        for file in tqdm(self.files):
            data = self.load_webpage([file], splitter=self.text_splitter)
            if data:
                self.docs.append(data[0])
        return self

    @staticmethod
    def load_webpage(files: List[Path], splitter: RecursiveCharacterTextSplitter) -> List[Dict]:
        options = Options()
        if RENDER_HEADLESS:
            options.add_argument('--headless')
        driver = webdriver.Chrome(options=options)
        docs = []
        for file in files:
            try:
                driver.get("file://" + file.as_posix())
                content = driver.find_element(by=By.TAG_NAME, value="body").text
                driver.close()
                if content:
                    doc = Document(page_content=HTMLIngester._normalize_text(content), metadata=file.name)
                else:
                    raise NoBodyException("There were no content in the webpage after rendering it.")
            except Exception as e:
                log.info("Trying BeautifulSoup as Selenium didn't find any content in the webpage.", e)
                soup = BeautifulSoup(file.open(), 'html.parser')
                checks = [
                    soup.find('section', id="cardsContentData"),
                    soup.find('div', class_=compile("cmp-(text|container)")),
                    soup.find('div', class_=compile(r"content(-typography|-area( p-0)? content-typography)?")),
                    soup.find('div', class_="MuiBox-root-80 jss81 jss71 jss75"),
                    soup.find('div', class_=compile(r"MuiTypography-root jss[0-9]{3} MuiTypography-body1")),
                    soup.find('div', class_="uf-tile-title title is-4 is-capitalized"),
                    soup.find('div', class_="field field--name-field-documentation-content field--type-entity-"
                                            "reference-revisions field--label-hidden field__items"),
                    soup.find('div', class_="card-content js-card-content"),
                    soup.find('body', id=compile(r"GUID-(9527C579-9311-4F8C-B87B-D66474C29173|"
                                                 "B405551C-B48A-4EE9-81F4-553886F950D5|"
                                                 "738D6DC2-D971-4AE2-BC13-43609193B8AC|"
                                                 "D7350EC7-5626-4A22-B99F-AA5C1EE4E0C8|"
                                                 "81D983B1-A719-4007-8A22-E26BE5A9C891|"
                                                 "6C873C2B-E65C-4B8F-8ECA-2104825B3694|"
                                                 "B799FADB-CD29-4F2E-899F-F5DEBE5221A6|"
                                                 "EFEC462E-5433-4153-BE59-A304BE962ADD|"
                                                 "DAEB7F61-E9C8-42DB-AB2E-35F137BE501C|"
                                                 "A9B7EC68-7A3C-4CEE-82C3-670D4B0BD09D)")),
                    soup.find('body', xmlns="http://www.w3.org/1999/xhtml"),
                    soup.find('span', class_="yt-core-attributed-string--link-inherit-color"),
                    soup.find('body', class_="body conbody"),
                    soup.find('div', class_="body conbody"),
                    soup.find('div', id="snippet"),
                    soup.find('div', id="bottom-row")
                ]

                if any(checks):
                    doc = Document(page_content=HTMLIngester._normalize_text(max(
                            (content.text for content in checks if content is not None), key=len)),
                            metadata={"file_name": file.name})
                else:
                    doc = None

            if doc:
                docs.append(doc)

        docs = splitter.split_documents(docs)
        return [doc.dict() for doc in docs]

    @staticmethod
    def _normalize_text(text: str) -> str:
        text = sub(r'\n{2,}', '\n', text)
        text = sub(r'\s{2,}', ' ', text)
        return text

    def send_to_vector_store(self, data: List[Dict] = None, url: str = VECTOR_STORE):
        payload = {"docs": data or self.docs}
        headers = {'Content-Type': 'application/json'}
        attempt = 0
        while attempt < VECTOR_STORE_RETRY_ATTEMPTS:
            response = put(url, headers=headers, json=payload)
            if response.status_code == 201:
                return response.json()
            else:
                attempt += 1
                sleep(WAIT_TIME)
                log.warning(f"Writing to vector store failed for {attempt + 1} times. Got: {response.text}")
        else:
            log.error(f"Failed to write to the vector store after {attempt + 1} times.")

    def concurrent_send_to_vector_store(self, data: List[List[Dict]] = None) -> List[Dict]:
        if data is None:
            data = self.docs
        with ThreadPoolExecutor() as executor:
            results = list(executor.map(self.send_to_vector_store, data))
        return results


if __name__ == "__main__":
    html_directory = "/home/mansour/PycharmProjects/autodesk/temp/pages"
    loader = HTMLIngester(html_directory)
    # print(loader.concurrent_load().concurrent_send_to_vector_store())
    print(loader.load().send_to_vector_store())
