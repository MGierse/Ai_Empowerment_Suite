from langchain.tools import Tool
from langchain.utilities import GoogleSearchAPIWrapper
from langchain.utilities import ArxivAPIWrapper
from langchain.utilities import PythonREPL
from langchain.chains import LLMMathChain, RetrievalQA

from Modules.Vectorstore import LoadVectorstore

from QuickMove import parsing_calcConveyor

def create_knowledge_base_tool(llm, **kwargs):
    vectorstore = kwargs.get('vectorstore')
    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectorstore.as_retriever()
    )

    return Tool(
        name='Knowledge Base',
        func=qa.run,
        description="Before attempting to answer any queries related to logistics or the knowledge base, it is mandatory that you utilize this 'Knowledge Base' tool. This is the first and foremost source of information and all efforts should be made to extract relevant information from it. All answers should be directly derived from the information contained within this tool only, without any supplementation or conjecture from your existing general knowledge or other sources. Only when you are 100 percent sure that the required information cannot be found within the 'Knowledge Base' should you consider any alternative actions. If such a situation arises, you must clearly express this limitation to the user and do not attempt to fabricate a response. Instead, request permission from the user to consider using other tools or your general knowledge. Wait for explicit user approval before proceeding to use these alternative information sources."
    )

def create_google_search_tool(**kwargs):
    search = GoogleSearchAPIWrapper()
    return Tool(
        name="Google Search",
        func=search.run,
        description="Useful for all question which require general knowledge and up to date information"
    )

def create_arxiv_paper_search_tool(**kwargs):
    arXiv = ArxivAPIWrapper()
    return Tool(
        name="arXiv Paper Search",
        func=arXiv.run,
        description="useful for all question that asks about scientific papers"
    )

def create_python_repl_tool(**kwargs):
    python_repl = PythonREPL()
    return Tool(
        name="Python REPL",
        func=python_repl.run,
        description="useful for all question that asks about Python codes"
    )

def create_calculator_tool(llm, **kwargs):
    math = LLMMathChain.from_llm(llm=llm)
    return Tool(
        name="Calculator",
        description="Useful for when you need to perform calculations.",
        func=math.run
    )

def create_quickmove_conveyor_calculator_tool(**kwargs):
    return Tool(
        name="QuickMove Conveyor Calculator",
        description="""Use this tool when you need to calculate the parameters of a QuickMove conveyor.
            The input to this tool should be a comma separated list of the two integers length and width and as well a string orientation, representing the inputs to be passed in the underlying function. 
            For example, `600, 350, "short side leading"` would be the input if a TU has been specified with length=600, width=350 and orientation="short side leading".
            The output of this tool would be a string with the parameters of the conveyor.""",
        func=parsing_calcConveyor
    )


def GetTools(selected_tool_names, **kwargs):
     # Store the functions to create the tools in a dictionary.
    tool_creators = {
        'Knowledge Base': create_knowledge_base_tool,
        'Google Search': create_google_search_tool,
        'arXiv Paper Search': create_arxiv_paper_search_tool,
        'Python REPL': create_python_repl_tool,
        'Calculator': create_calculator_tool
    }

    # Create and return the selected tools.
    return [tool_creators[name](**kwargs) for name in selected_tool_names if name in tool_creators]