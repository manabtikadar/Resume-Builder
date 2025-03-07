from langchain_core.output_parsers import StrOutputParser
from langchain_cohere import ChatCohere
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage

preamble = """You are an expert assistant for resume building. When relevant documents are unavailable, generate a concise and professional response based on general knowledge of resumes, job applications, and career development. Keep your answers precise, clear, and limited to three sentences."""

llm = ChatCohere(model_name="command-r", temperature=0).bind(preamble=preamble)

def prompt(x):
    return ChatPromptTemplate.from_messages(
        [HumanMessage(f"Question: {x['question']} \nAnswer: ")]
    )


llm_chain = prompt | llm | StrOutputParser()


