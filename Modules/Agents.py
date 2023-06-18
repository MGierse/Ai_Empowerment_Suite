import logging
import ConsoleInterface

import langchain.schema
from langchain.agents import initialize_agent, create_pandas_dataframe_agent, AgentType

logger = logging.getLogger('ConsoleInterface')

def PandasDataframeAgent(llm, Dataframe):
    PandasDataframeAgent = create_pandas_dataframe_agent(llm, df=Dataframe, verbose=True)

    return PandasDataframeAgent
    
def RunConversationalAgent(llm, Tools, Memory):

    initialize_agent
    Agent = initialize_agent(agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION, llm=llm, tools=Tools, memory=Memory, verbose=True)
    logger.info("Agent initialized successfully!\n")

    while True:
        query = input("Enter your query: ")
        if query.lower() == "exit" or query.lower() == "quit":
            break
        try:
            Agent.run(str(query))
        except langchain.schema.OutputParserException as e:
                # Extract the message from the exception
                message = str(e)
                # The message is in the form "Could not parse LLM output: `...`"
                # So, we can split it by the backticks and take the second element
                answer = message.split('`')[1]

                logger.warning("\nError occured in retrieving answer from language model. Please check your query and try again. Answer stored in error message will be printed:\n")
                logger.warning("\nAnswer: ", answer)