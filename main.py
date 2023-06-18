from dotenv import load_dotenv
import os
import time
import logging
import ConsoleInterface


#Import external modules
import Modules.Dataloader as dl
import DataAnalysis as dA



from Modules.LLM import getKUKA_LLM
from Modules.LLM import getMP_LLM
from ScrapeMe import ScrapeMe
from PDF2Chat import PDF2Chat_Run


#Vector Storage
from Modules.Embeddings import AzureOpenAIEmbeddings
from Modules.Vectorstore import CreateVectorstore




#Init Console
logger = logging.getLogger('ConsoleInterface')

#Generally required
llm = getKUKA_LLM()

embeddings = AzureOpenAIEmbeddings(deployment_name="kuka-text-embedding-ada-002")

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
            #CreateVectorStore()
            CreateVectorstore(embeddings=embeddings)
        elif choice == "2":
            dA.RunExcelQuery()
        elif choice == "3":
            None
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