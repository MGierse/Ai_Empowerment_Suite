"""Wrapper around ChromaDB embeddings platform."""
import time
from typing import TYPE_CHECKING, Any, Dict, Iterable, List, Optional, Tuple, Type

from langchain.embeddings.base import Embeddings
from langchain.vectorstores.chroma import Chroma
import logging
import ConsoleInterface

import chromadb
import chromadb.config

_LANGCHAIN_DEFAULT_COLLECTION_NAME = "langchain"

#Init Console
logger = logging.getLogger('ConsoleInterface')

class My_Chroma(Chroma):

    @classmethod
    def from_texts(
        cls: Type[Chroma],
        texts: List[str],
        embedding: Optional[Embeddings] = None,
        metadatas: Optional[List[dict]] = None,
        ids: Optional[List[str]] = None,
        collection_name: str = None,
        persist_directory: Optional[str] = None,
        client_settings: Optional[chromadb.config.Settings] = None,
        client: Optional[chromadb.Client] = None,
        pause_time: float = None,
        **kwargs: Any,

    ) -> Chroma:
        """Create a Chroma vectorstore from a raw documents.

        If a persist_directory is specified, the collection will be persisted there.
        Otherwise, the data will be ephemeral in-memory.

        Args:
            texts (List[str]): List of texts to add to the collection.
            collection_name (str): Name of the collection to create.
            persist_directory (Optional[str]): Directory to persist the collection.
            embedding (Optional[Embeddings]): Embedding function. Defaults to None.
            metadatas (Optional[List[dict]]): List of metadatas. Defaults to None.
            ids (Optional[List[str]]): List of document IDs. Defaults to None.
            client_settings (Optional[chromadb.config.Settings]): Chroma client settings

        Returns:
            Chroma: Chroma vectorstore.
        """
        chroma_collection = cls(
            collection_name=collection_name,
            embedding_function=embedding,
            persist_directory=persist_directory,
            client_settings=client_settings,
            client=client,
        )

        logger.info("Adding files to Vectorstor ...\n")

        for i, text in enumerate(texts):
            chroma_collection.add_texts(texts=[text], metadatas=[metadatas[i]], ids=[ids[i]])

            # Berechnung des Fortschritts
            progress = (i + 1) / len(texts) * 100  # i+1, da die Indexierung bei 0 beginnt
            print(f"Progress: {progress:.2f}% completed", end='\r')

            time.sleep(pause_time)

        return chroma_collection