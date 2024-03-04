# Overview

This project is designed with a microservice architecture in mind and consists of four main components: 
`discourse_manager`, `document_ingestion`, `vector_store`, and `UI`. To run the project, the services need to be 
launched in this order.
1- vector_store
2- document_ingestion
3- discourse_manager
4- user_interface

## Components

### Discourse Manager

The `discourse_manager` handles conversations. 

#### Requirements

Install the requirements using the following command:

```bash
pip install -r discourse_manager/requirements.txt
```

#### Running the Service
You can run the discourse_manager using the command bellow from the said microservice's root.
```bash
python serve.py
```
When the server is up, you can start chatting with the bot. A sample curl is provided below.
```bash
curl --location 'http://0.0.0.0:2023/converse/ask' --header 'Content-Type: application/json' --data '{"question": "What is Autodesk Fusion 360 with PowerInspect?", "history": null}'
```

### Document Ingestion
The document_ingestion ingests the documents into the vector store.

#### Requirements
Install the requirements using the following command:
```bash
pip install -r document_ingestion/requirements.txt
```

#### Running Document Ingestion
You need the vector store to be running to be able to run the document ingestion.
To run the document ingestion use the command bellow from the document_ingestion root directory.
```bash
python ingest.py --data_directory <path to the directory with teh html files>
```

### UI
The UI provides a simplistic user interface for the chatbot.

#### Requirements
Install the requirements using the following command:

```bash
pip install -r user_interface/requirements.txt
```

#### Running the UI
To run the UI run the command bellow from the user_interface root.
```bash
python ui.py
```

### Vector Store
The vector_store implements a very rudimentary faiss vector store.

#### Requirements
Install the requirements using the following command:

```bash
pip install -r vector_store/requirements.txt
```

#### Running the Service
You can run the vector_store using the command bellow from the said microservice's root.
```bash
python serve.py
```

#### Docker
The vector_store also includes a Dockerfile. To build and run the Docker container, use the following commands from the root of the microservice.

```bash
docker build -t faiss .
docker run -p 2024:2024 faiss
```
