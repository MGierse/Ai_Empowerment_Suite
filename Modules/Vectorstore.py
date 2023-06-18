import logging
import ConsoleInterface
from dotenv import load_dotenv

from langchain.vectorstores.chroma import Chroma
from Custom_Chroma import My_Chroma
from Modules.Dataloader import GetEmbeddingData
from Modules.Embeddings import EmbeddingRateController
from Modules.Embeddings import EmbedData

logger = logging.getLogger('ConsoleInterface')
#Load Environment Variables


def CreateVectorstore(embeddings):
    load_dotenv()

    persist_directory = "db" #If changed, issues while loading -> stick to default "db"

    collection_name = input("Specify database name to create: ")

    chunkSize = input("How many tokens per chunk?: ")
    logger.info("Chunksize set to "  + chunkSize + "\n")

    logger.info("Select files to create database from system file dialog.\n")
    EmbeddingData = GetEmbeddingData(int(chunkSize))

    pause_time = EmbeddingRateController(int(chunkSize))
    texts, metadatas, ids = EmbedData(EmbeddingData)
    logger.info("Data embedded successfully!\n")

    vectorstore = My_Chroma.from_texts(texts=texts, metadatas=metadatas, ids=ids, embedding=embeddings, persist_directory=persist_directory, collection_name=collection_name, pause_time=pause_time)
    logger.info("Vectorstore created successfully!\n")

    def store_DataBaseName_ToFile(collection_name):
        with open('DataBaseIDs.txt', 'r') as f:
            current_lines = f.readlines()

        with open('DataBaseIDs.txt', 'a') as f:
            line_number = len(current_lines) + 1
            f.write(f"{line_number}. {collection_name}\n")

        logger.info("Filename written to root\DataBaseIDs.txt successfully!\n")

    store_DataBaseName_ToFile(collection_name)

    vectorstore.persist()
    vectorstore=None

    logger.info("Vectorstore saved to \\root\\" + persist_directory + "\n")

    return vectorstore

def LoadVectorstore(embeddings):
    persist_directory = "db" #If changed, issues while loading -> stick to default "db"
    
    vectorstore = Chroma(persist_directory=persist_directory, embedding_function=embeddings, collection_name=input("Specify database name to load: "))
    logger.info("Vectorstore loaded successfully!\n")
    return vectorstore

def AddDataToVectorstore():
    None