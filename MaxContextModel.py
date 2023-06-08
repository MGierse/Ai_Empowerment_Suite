
"""
This model was specifically designed for experimentation and not intended for operational use.
The aim was to challenge the typical use of chroma in conjunction with the GPT-3.5 Turbo model. Under normal circumstances, chroma doesn't utilize the full context window
of the GPT-3.5 Turbo model, but instead only returns 'k=4' results to respond to a user query. This experimental model, on the other hand, maximizes the use of the context
window by including as much pertinent information as possible in the prompt, alongside the user's question, before forwarding it to the model for response generation.

Current Challenges:

-   A notable issue is that the Conversation Memory, which should ideally store the conversation history, and the extracted facts from documents,
    which should be utilized for context generation, are currently cohabiting the same memory space. This configuration creates a complex problem
    where prior questions are answered repeatedly with each subsequent user query, resulting in a non-linear and confusing conversation flow.

-   The problem seems to stem from the position of the "system-prompt" within the memory. Attempts to rearrange the "system-prompt" position resulted
    in the model being unable to access the information stored prior to the "system-prompt". Although this is still a working hypothesis, it provides
    a starting point for further investigations and debugging.
"""


from dotenv import load_dotenv
import logging
import ConsoleInterface

from main import LoadVectorStore
from LLM_Interface import getMP_LLM
from collections import deque
import tiktoken

load_dotenv()

#Init Console
logger = logging.getLogger('ConsoleInterface')

def retrieveVectorDocuments(vectorstore, QtyDocsToReturn, query):

    content = ""
    
    #vectorstore = LoadVectorStore()
    
    resultsMMR = vectorstore.max_marginal_relevance_search(query=query, k=int(QtyDocsToReturn), fetch_k=int(QtyDocsToReturn)*5)
    resultsSimilarity = vectorstore.similarity_search(query=query, k=int(QtyDocsToReturn))
    
    for text in resultsMMR:
        #print(text)
        content+=text.page_content

    for text in resultsSimilarity:
        #print(text)
        content+=text.page_content

    return content
    
def prepareLLM_Context(query, vectorstore, QtyDocsToReturn, memory, total_tokens):
    
    
    tokenizer = tiktoken.get_encoding("cl100k_base")
    content = retrieveVectorDocuments(vectorstore=vectorstore, QtyDocsToReturn=QtyDocsToReturn, query=query)

    combinedQuery = query + content

    memory.append({"role": "user", "content": combinedQuery})
    history = list(memory)  # Gesamtes Memory als Liste für die Anfrage zusammensetzen

    for word in combinedQuery.split():
        total_tokens += len(tokenizer.encode(word))



    return history, total_tokens


def MaxContextModel():
    vectorstore = LoadVectorStore()
    QtyDocsToReturn = 20

    context_memory = []
    #conversation_memory = deque(maxlen=100)  # Maximale Anzahl von Einträgen im Konversations-Memory festlegen
      
    system_msg = "You are a chatbot having a conversation with a human. Given the following extracted parts of a long document and a question, create a final answer."  # Primer

    max_tokens = 4096
    total_tokens = 0

    foundDocQty = False

    #query = query
    query = input("Enter your query: ")
    context_memory.append({"role": "system", "content": system_msg})

    while True:
    
        if total_tokens <= max_tokens and foundDocQty == False:
            QtyDocsToReturn += 1
            context_memory.clear()
            total_tokens = 0

            context_memory.append({"role": "system", "content": system_msg})
            history, total_tokens = prepareLLM_Context(query, vectorstore, QtyDocsToReturn, context_memory, total_tokens)
            continue
        else:
            if QtyDocsToReturn > 1 and foundDocQty == False:
                del context_memory[-1]
                QtyDocsToReturn -= 1
                total_tokens = 0
                foundDocQty = True
                #context_memory.clear()
                #history.clear()
                #del context_memory[-1]
            
            
        history, total_tokens = prepareLLM_Context(query, vectorstore, QtyDocsToReturn, context_memory, total_tokens)

        

        
        llm = getMP_LLM(history=history)

        reply = llm.choices[0].message.content.strip()
        # Die Antwort des Modells wird auch dem Konversations-Memory hinzugefügt.
        #conversation_memory.append({"role": "user", "content": query})
        context_memory.append({"role": "assistant", "content": reply})
        #conversation_memory.append(history)
        
        logger.info("\n" + "Ai: " + reply + "\n")
        #return conversation_memory    
        #history = list(conversation_memory)

        # to_delete = {"role": "system", "content": system_msg}  # Das Element, das Sie löschen möchten

        # for i, d in enumerate(context_memory):
        #     if d == to_delete:
        #         del context_memory[i]
        #         break  # Beenden Sie die Schleife nach dem Löschen des ersten gefundenen Elements

        for d in reversed(context_memory):
            if d["role"] == "user":
                d["content"] = query
                break  # Beenden Sie die Schleife nach der ersten gefundenen Übereinstimmung


        #context_memory.append({"role": "system", "content": system_msg})        
        query = input("Enter your query: ")

if __name__ == "__main__":
    MaxContextModel()