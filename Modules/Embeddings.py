from langchain.embeddings.openai import OpenAIEmbeddings

def AzureOpenAIEmbeddings(deployment_name: str):
    return OpenAIEmbeddings(deployment=deployment_name)
    
def EmbeddingRateController(chunkSize: int):
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

    return pause_time

def EmbedData(EmbeddingData):

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

    return texts, metadatas, ids