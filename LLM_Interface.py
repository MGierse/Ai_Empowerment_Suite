from dotenv import load_dotenv
import os
from langchain.chat_models import AzureChatOpenAI #(Private Azure Acces)

load_dotenv()

def getKUKA_LLM():
    
    llm = AzureChatOpenAI (
        openai_api_base=os.getenv("OPENAI_API_BASE_AZURE"),
        openai_api_version="2023-03-15-preview",
        deployment_name=os.getenv("DEPLOYMENT_NAME_AZURE"), 
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        openai_api_type = "azure",
        temperature=0
    )
    return llm