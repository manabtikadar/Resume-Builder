from langchain_cohere import ChatCohere
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import warnings
import os
load_dotenv()

warnings.filterwarnings('ignore')

COHERE_API_KEY = os.getenv("COHERE_API_KEY")
class web_search(BaseModel):
    """
    The internet. Use web_search for questions that are related to anything else than agents, prompt engineering, and adversarial attacks.
    """

    query: str = Field(description="The query to use when searching the internet.")


class vectorstore(BaseModel):
    """
    A vectorstore containing documents related to agents, prompt engineering, and adversarial attacks. Use the vectorstore for questions on these topics.
    """

    query: str = Field(description="The query to use when searching the vectorstore.")


preamble = """You are an expert at determining whether a user query should be routed to a vectorstore or a web search. The vectorstore contains documents related to different resume templates, including general formats for Engineers, Content Writers, Data Scientists, Marketing Managers, Project Managers, and Software Engineers. Use the vectorstore for queries about these resume templates. For all other topics, use web search."""

llm = ChatCohere(model="command-r", temperature=0,cohere_api_key=COHERE_API_KEY)
structured_llm_router = llm.bind_tools(
    tools=[web_search, vectorstore], preamble=preamble
)

route_prompt = ChatPromptTemplate.from_messages(
    [
        ("human", "{question}"),
    ]
)

question_router = route_prompt|structured_llm_router

# response = question_router.invoke(
#     {"query": "What is a General resume format for Engineers?"}
# )
# print(response.response_metadata["tool_calls"])
# response = question_router.invoke({"query": "what are the key components of a resume?"})
# print(response.response_metadata["tool_calls"])
# response = question_router.invoke({"query": "Hi how are you?"})
# print("tool_calls" in response.response_metadata)