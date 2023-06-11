from dotenv import load_dotenv
import os
import time
import logging
import ConsoleInterface

#Import external modules
import Modules.Dataloader as dl
import DataAnalysis as dA
from QuickMove import parsing_calcConveyor
from Modules.LLM import getKUKA_LLM
from Modules.LLM import getMP_LLM
from ScrapeMe import ScrapeMe
from PDF2Chat import PDF2Chat_Run


#Vector Storage
from Modules.Embeddings import AzureOpenAIEmbeddings
from langchain.vectorstores.chroma import Chroma
from Custom_Chroma import My_Chroma

from Modules.Memory import ConversationBufferMemory
from langchain.chains import RetrievalQA
from langchain.chains import qa_with_sources
import langchain.schema

#Tool Interface
from langchain.tools import Tool
from langchain.utilities import GoogleSearchAPIWrapper
from langchain.utilities import ArxivAPIWrapper
from langchain.utilities import PythonREPL
from langchain.chains import LLMMathChain

#Agent Interface
from langchain.agents import initialize_agent, AgentType
import tiktoken

#Load Environment Variables
load_dotenv()

#Init Console
logger = logging.getLogger('ConsoleInterface')

#Generally required
#llm = getKUKA_LLM()
llm = getKUKA_LLM()

embeddings = AzureOpenAIEmbeddings(deployment_name="kuka-text-embedding-ada-002")

persist_directory = "db"
vectorstore = None
collection_name = ""

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
print.test
logger.info(logo)

def LoadVectorStore():
    vectorstore = Chroma(persist_directory=persist_directory, embedding_function=embeddings, collection_name=input("Specify database name to load: "))

    logger.info("Vectorstore loaded successfully!\n")

    proceedWithAgent = input("Would you like to use the agent? (y/n): ")

    if proceedWithAgent == "y":
        GetAgent(vectorstore)
    
    return vectorstore

def CreateVectorStore():
    logger.info("Select files to create database from system file dialog.\n")
    LoadedData = dl.LoadFiles()

    collection_name = input("Specify database name to create: ")

    chunkSize = input("How many tokens per chunk?: ")
    logger.info("Chunksize set to "  + chunkSize + "\n")

    EmbeddingData = dl.GetEmbeddingData(LoadedData, chunk_size=int(chunkSize))
        
    # Die Anzahl der Tokens, die pro Anfrage verbraucht werden
    n = int(chunkSize)  # Beispielwert, sollte so angepasst werden, dass n*q <= 120000
    
    # Die Anzahl der Anfragen, die Sie pro Minute machen möchten
    q = 230 #<= 300 according to API specification Embeddings with Azure OpenAi

    # Sicherstellen, dass Sie das Token-Limit nicht überschreiten
    #assert n*q <= 120000, "Die Anzahl der Anfragen pro Minute überschreitet das Token-Limit."
    if n*q > 115000:
        q = 115000 / n

    # Die Zeit zwischen den Anfragen in Sekunden
    pause_time = 60.0 / q

    texts = []
    metadatas = []
    ids = []

    for i, chunks in enumerate(EmbeddingData):
        # Hier führen Sie den Code aus, der die Anfragen macht und die Tokens verbraucht
        texts.append(chunks)
        metadatas.append({"source": f"doc{i}"})
        ids.append(f"doc{i}")

        # Berechnung des Fortschritts
        progress = (i + 1) / len(EmbeddingData) * 100  # i+1, da die Indexierung bei 0 beginnt
        print(f"Progress: {progress:.2f}% completed", end='\r')
        
        # Pause einlegen, nachdem jede Anfrage ausgeführt wurde
        #time.sleep(pause_time)

    logger.info("Data embedded successfully!\n")

    vectorstore = My_Chroma.from_texts(texts=texts, metadatas=metadatas, ids=ids, embedding=embeddings, persist_directory=persist_directory, collection_name=collection_name, pause_time=pause_time)
    
    logger.info("Vectorstore created successfully!\n")
    
    store_DataBaseName_ToFile(collection_name)
    # # Add documents to the index
    # documents = []

    # for i, chunks in enumerate(EmbeddingData):
    #     document = {"metadata": {"doc_id": f"doc{i}"}, "page_content": chunks}
    #     documents.append(document)
    #     vectorstore.add_documents(documents)
    #     documents.clear()

    vectorstore.persist()
    #vectorstore=None

    logger.info("Vectorstore saved to \\root\\" + vectorstore._persist_directory + "\n")

    GetAgent(vectorstore)
    return vectorstore

def GetAgent(vectorstore):

    # retrieval qa chain
    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectorstore.as_retriever()
    )

    search = GoogleSearchAPIWrapper()
    arXiv = ArxivAPIWrapper()
    python_repl = PythonREPL()
    math = LLMMathChain.from_llm(llm=llm)

    tools = [
        Tool(
            name='Knowledge Base',
            func=qa.run,
            description="Before attempting to answer any queries related to logistics or the knowledge base, it is mandatory that you utilize this 'Knowledge Base' tool. This is the first and foremost source of information and all efforts should be made to extract relevant information from it. All answers should be directly derived from the information contained within this tool only, without any supplementation or conjecture from your existing general knowledge or other sources. Only when you are 100 percent sure that the required information cannot be found within the 'Knowledge Base' should you consider any alternative actions. If such a situation arises, you must clearly express this limitation to the user and do not attempt to fabricate a response. Instead, request permission from the user to consider using other tools or your general knowledge. Wait for explicit user approval before proceeding to use these alternative information sources."
            ),

        Tool(
            name="Google Search",
            func=search.run,
            description="Useful for all question which require general knowledge and up to date information"
            ),

        Tool(
            name="arXiv Paper Search",
            func=arXiv.run,
            description="useful for all question that asks about scientific papers"
            ), 

        Tool(
            name="Python REPL",
            func=python_repl.run,
            description="useful for all question that asks about Python codes"
            ),

        Tool(
            name="Calculator",
            description="Useful for when you need to perform calculations.",
            func=math.run
            ),


        Tool(
            name="QuickMove Conveyor Calculator",
            description="""Use this tool when you need to calculate the parameters of a QuickMove conveyor.
            The input to this tool should be a comma separated list of the two integers length and width and as well a string orientation, representing the inputs to be passed in the underlying function. 
            For example, `600, 350, "short side leading"` would be the input if a TU has been specified with length=600, width=350 and orientation="short side leading".
            The output of this tool would be a string with the parameters of the conveyor.""",
            func=parsing_calcConveyor
            )
    ]

    memory = ConversationBufferMemory("chat_history")
    agent = initialize_agent(tools, llm,verbose=True, agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION, memory=memory)

    logger.info("Agent initialized successfully!\n")
    
    RunQuery(agent)

    return agent

def store_DataBaseName_ToFile(collection_name):
    with open('DataBaseIDs.txt', 'r') as f:
        current_lines = f.readlines()

    with open('DataBaseIDs.txt', 'a') as f:
        line_number = len(current_lines) + 1
        f.write(f"{line_number}. {collection_name}\n")

    logger.info("Filename written to root\DataBaseIDs.txt successfully!\n")

def RunQuery(agent):
    logger.info("Ready to query data!\n")
    while True:
            query = input("Enter your query: ")
            if query.lower() == "exit" or query.lower() == "quit":
                break
            try:
                #agent(query)
                agent.run(query)
            except langchain.schema.OutputParserException as e:
                # Extract the message from the exception
                message = str(e)
                # The message is in the form "Could not parse LLM output: `...`"
                # So, we can split it by the backticks and take the second element
                answer = message.split('`')[1]

                logger.warning("\nError occured in retrieving answer from language model. Please check your query and try again. Answer stored in error message will be printed:\n")
                logger.warning("\nAnswer: ", answer)



        

if __name__ == "__main__":
    def display_menu():
        print("Menu:")
        print("1. Create Vectorstore and run agent (optional)")
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
            CreateVectorStore()
        elif choice == "2":
            dA.RunExcelQuery()
        elif choice == "3":
            LoadVectorStore()
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