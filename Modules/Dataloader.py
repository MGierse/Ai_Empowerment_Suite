import tkinter as tk
from tkinter import filedialog
import PyPDF2
import docx2txt
import tiktoken
import os


def LoadFiles():
    # Open file dialog to select multiple files
    root = tk.Tk()
    root.withdraw()

    filetypes = [("Text files", "*.txt;*.pdf;*.docx"), ("PDF files", "*.pdf"), ("Excel files", "*.xlsx"), ("Word files", "*.docx"), ("Text files", "*.txt")]

    file_paths = filedialog.askopenfilenames(filetypes=filetypes)

    words_all = []

    # Process each file based on its extension
    for file_path in file_paths:
        _, ext = os.path.splitext(file_path)

        if ext == '.txt':
            words = LoadTXT(file_path)
        elif ext == '.docx':
            text = docx2txt.process(file_path)
            words = text.split()
        elif ext == '.pdf':
            words = LoadPDF(file_path)
        elif ext == '.xlsx':
            return file_path #For Excel based data only the respective file path is being returned to be processed in datafram or similar afterwards
        else:
            print(f'Unsupported file type: {ext}')
            continue

        words_all.extend(words)

    return words_all

def LoadTXT(file_path):
    txtFileObject = open(file_path, "r")
    text = txtFileObject.read()
    words = text.split()
    txtFileObject.close()
    return words

def LoadPDF(file_path):
    pdfFileObject = open(file_path, "rb")
    pdfReader = PyPDF2.PdfReader(pdfFileObject)
    count = len(pdfReader.pages)
    text = ""
    for i in range(count):
        page = pdfReader.pages[i]
        text += page.extract_text() + "\n"
    words = text.split()
    pdfFileObject.close()
    return words

#Create Embeddings according to the chunk size specified for selected filetype
def GetEmbeddingData(chunkSize: int):

    words_all = LoadFiles()

    chunks = []
    chunk = []
    chunk_token_count = 0

    # Import the tiktoken package and create a length function
    tokenizer = tiktoken.get_encoding("cl100k_base")

    for word in words_all:
        word_token_count = len(tokenizer.encode(word))
        if chunk_token_count + word_token_count > chunkSize:
            # Join the current chunk into a string and add it to the chunks list
            chunks.append(' '.join(chunk))
            # Start a new chunk with the current word
            chunk = [word]
            chunk_token_count = word_token_count
        else:
            # Add the current word to the current chunk
            chunk.append(word)
            chunk_token_count += word_token_count

    # Don't forget to add the last chunk if it's not empty
    if chunk:
        chunks.append(' '.join(chunk))

    EmbeddingData = [' '.join(words_all[i:i+chunkSize]) for i in range(0, len(words_all), chunkSize)]

    # while len(batches) < 4: #equals k parameter in query of openAI api
    #     batches.append("")

    return EmbeddingData