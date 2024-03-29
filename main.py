from dotenv import load_dotenv
import os
import time
import logging
import ConsoleInterface

#Import external modules
from Modules.Tools import GetTools
#import DataAnalysis as dA
from Modules.Agents import RunConversationalAgent
from Modules.Chains import run_conversationalretrieval_chain

from Modules.Memory import getConversationBufferMemory
from Modules.Vectorstore import LoadVectorstore

from Modules.LLM import getKUKA_LLM
from Modules.LLM import getMP_LLM
from ScrapeMe import ScrapeMe
from PDF2Chat import PDF2Chat_Run

#Vector Storage
from Modules.Embeddings import AzureOpenAIEmbeddings
from Modules.Vectorstore import CreateVectorstore

#Init Console & Welcome Screen
logger = logging.getLogger('ConsoleInterface')
logger.info("\n\n--- Welcome to SWISSLOG Ai-Empowerment-Suite v1.0.0 ---\n")
logo = r"""

                      ▄
                    ▄▄▄▄▄  
                  ▄▄▄▄▄▄▄▄▄
               ▗  ▄▄▄▄▄▄▄▄▄  ▖
              ▄▄▄   ▄▄▄▄▄   ▄▄▄
            ▄▄▄▄▄▄▄   ▄   ▄▄▄▄▄▄▄
          ▄▄▄▄▄▄▄▄▄▄▄   ▄▄▄▄▄▄▄▄▄▄▄
        ▄▄▄▄▄▄▄▄▄▄▄▄▄   ▄▄▄▄▄▄▄▄▄▄▄▄▄
      ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄   ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄

  NEURAL NET-BASED ARTIFICIAL INTELLIGENCE        
     C Y B E R D Y N E - S Y S T E M S
"""
logger.info(logo)

#Generally required
embeddings = AzureOpenAIEmbeddings(azure_deployment="kuka-text-embedding-ada-002")

def FirstModularTest():
    """
    This function performs the first modular test.

    It initializes the necessary components, such as the KUKA LLM, vectorstore,
    conversation buffer memory, and tools. Then, it runs the conversational agent.

    Parameters:
        None

    Returns:
        None
    """
    llm = getKUKA_LLM()
    vectorstore = LoadVectorstore(embeddings=embeddings)    
    memory = getConversationBufferMemory(memory_key="chat_history")
    Tools = GetTools(selected_tool_names=['Knowledge Base'], llm=llm, vectorstore=vectorstore)
    RunConversationalAgent(llm=llm, Tools=Tools, Memory=memory)


def SecondModularTest():
    llm = getKUKA_LLM()
    vectorstore = LoadVectorstore(embeddings=embeddings)    
    memory = getConversationBufferMemory(memory_key="chat_history")

    run_conversationalretrieval_chain(vectorstore=vectorstore, llm=llm, memory=memory)


if __name__ == "__main__":

    def display_menu():
        print("Menu:")
        print("1. Create Vectorstore from file")
        print("2. Run data analysis against Excel data(PandasAgent)")
        print("3. Load existing Vectorstore to query")
        print("4. ScrapeMe!")
        print("5. PDF2Chat")
        print("6. Search My Vectorstore")
        print("7. Test")
        print("0. Exit")

    # Main Menu
    while True:
        display_menu()
        choice = input("\n"+"Select an option: ")

        if choice == "1":
            #CreateVectorStore()
            CreateVectorstore(embeddings=embeddings)
        elif choice == "2":
            SecondModularTest()
            #dA.RunExcelQuery()
        elif choice == "3":
            FirstModularTest()
            #LoadVectorStore()
        elif choice == "4":
            base_url = input("Provide Base URL to scrape from!: ")
            ScrapeMe(base_url=base_url, url=base_url)
        elif choice == "5":
            PDF2Chat_Run()
        elif choice == "6":    
            None
        elif choice == "7":
            None
        elif choice == "0":
            break
        else:           
            print("Invalid choice. Please try again.")