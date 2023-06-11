from langchain.embeddings.openai import OpenAIEmbeddings

def AzureOpenAIEmbeddings(deployment_name: str):
    return OpenAIEmbeddings(deployment=deployment_name)
    