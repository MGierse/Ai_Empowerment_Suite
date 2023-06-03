from dotenv import load_dotenv
import pandas as pd
import tkinter as tk
from tkinter import filedialog
from LLM_Interface import getKUKA_LLM

#Import API Keys
load_dotenv()

import langchain.schema
from langchain.agents import create_pandas_dataframe_agent

# chat completion llm
llm = getKUKA_LLM()

#LoadXLSX() Data in Pandas Dataframe
def LoadExcel():
    # Open file dialog to select a xlsx file
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(filetypes=[("Excel", "*.xlsx")])

    # Read the xlsx file into a pandas DataFrame
    df = pd.read_excel(file_path)

    chat = llm
    agent = create_pandas_dataframe_agent(chat, df, verbose=True)

    return agent

def RunExcelQuery():
    agent = LoadExcel()
    while True:
        query = input("Enter your query: ")
        if query.lower() == "exit" or query.lower() == "quit":
            break
        try:
            agent.run(str(query))
        except langchain.schema.OutputParserException as e:
            # Extract the message from the exception
            message = str(e)
            # The message is in the form "Could not parse LLM output: `...`"
            # So, we can split it by the backticks and take the second element
            answer = message.split('`')[1]
            print("\n\nAnswer: ", answer)

if __name__ == "__main__":

    RunExcelQuery()