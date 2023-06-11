import logging
import ConsoleInterface

from langchain.vectorstores.chroma import Chroma
from Custom_Chroma import My_Chroma

logger = logging.getLogger('ConsoleInterface')

def CreateVectorstore():
    logger.info("Select files to create database from system file dialog.\n")


def LoadVectorstore(embeddings):
    persist_directory = "db" #If changed, issues while loading -> stick to default "db"
    
    vectorstore = Chroma(persist_directory=persist_directory, embedding_function=embeddings, collection_name=input("Specify database name to load: "))
    logger.info("Vectorstore loaded successfully!\n")
    return vectorstore

def AddDataToVectorstore():
    None