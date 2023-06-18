from dotenv import load_dotenv
import os
from langchain.chat_models import AzureChatOpenAI #(Private Azure Acces)
import openai



def getKUKA_LLM():

    load_dotenv()

    llm = AzureChatOpenAI (
        openai_api_base=os.getenv("OPENAI_API_BASE_AZURE"),
        openai_api_version="2023-03-15-preview",
        deployment_name=os.getenv("DEPLOYMENT_NAME_AZURE"), 
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        openai_api_type = "azure",
        temperature=0
    )
    return llm

def getMP_LLM(message): #Multi Purpose LLM on Azure (CHATGPT)

    load_dotenv()

    openai.api_type = "azure"
    openai.api_base = "https://kuka-openai-playground.openai.azure.com/"
    openai.api_version = "2023-03-15-preview"
    openai.api_key = os.getenv("OPENAI_API_KEY")

    llm = openai.ChatCompletion.create(
        engine="kuka-gpt-35-turbo-v0301",
        messages = message,
        temperature=0.7,
        max_tokens=800,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None,
        n=1
        )
    
    return llm