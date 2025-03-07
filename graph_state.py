from typing import List
from typing_extensions import TypedDict
from langchain.schema import Document

from Retriever import retriever
from generate_answer import rag_chain
from Grader import retrieval_grader
from question_rewrite import q_rewriter
from doc_chain import doc_chain
from final_generate import addn_final_rag_chain
from LLM_fallback import llm_chain
from question_answer import information_chain
from router import question_router
from Web_Search import web_search_chain
import warnings

warnings.filterwarnings('ignore')


class GraphState(TypedDict):
    query: str
    question: str
    generation: str
    json_output: dict
    latex_output:str
    linkedin_link: str
    documents: List[Document]

def retrieve(state: GraphState) -> GraphState:
    print("---RETRIEVE---")
    question = state["question"]

    documents = retriever.get_relevant_documents(question)
    return {
        **state,
        "documents": documents
        }

def generate(state: GraphState) -> GraphState:
    print("---GENERATE---")
    question = state["question"]
    documents = state["documents"]
    generation = rag_chain.invoke(
        {
           "docs":documents, 
           "question": question
        }
    )
    return{
        **state,
        "generation":generation
    }

def grade_documents(state: GraphState) -> GraphState:
    print("---CHECK DOCUMENT RELEVANCE TO QUESTION---")
    question = state["question"]
    documents = state["documents"]
    filtered_docs = []

    for d in documents:
        score = retrieval_grader.invoke({
            "doc": d.page_content,
            "question": question
        })
        if score.get("score") == "yes":
            print("---GRADE: DOCUMENT RELEVANT---")
            filtered_docs.append(d)
        else:
            print("---GRADE: DOCUMENT NOT RELEVANT---")
    
    return {
        **state, 
        "documents": filtered_docs
        }

def generate_resume_json(state: GraphState) -> GraphState:
    print("---CREATE JSON FILE AND ADD WITH DOCS FOR RESUME GENERATION---")

    query = state["query"]
    filtered_documents = state["documents"]

    json_docs = information_chain.invoke(
        {
            "query":query
        }
    )
    new_docs = []
    for d in filtered_documents:
        new_doc = doc_chain.invoke(
            {
              "input_json": json_docs, 
              "docs": d.page_content
            }
        )
        new_docs.append(Document(page_content=new_doc))
    return {
        **state,
        "documents":new_docs
    }

def Rewrite_Question(state: GraphState) -> GraphState:
    print("---REWRITE THE QUESTION---")
    question = state["question"]
    better_question = q_rewriter.invoke({"question": question})
    return {
        **state, 
        "question": better_question
        }

def route_question(state:GraphState) -> GraphState:
    print("---ROUTE QUESTION---")
    question = state["question"]
    source = question_router.invoke({"question": question})


    if "tool_calls" not in source.additional_kwargs:
        print("---ROUTE QUESTION TO LLM---")
        return "llm_fallback"
    if len(source.additional_kwargs["tool_calls"]) == 0:
        raise "Router could not decide source"

    datasource = source.additional_kwargs["tool_calls"][0]["function"]["name"]
    if datasource == "web_search":
        print("---ROUTE QUESTION TO WEB SEARCH---")
        return "web_search"
    elif datasource == "vectorstore":
        print("---ROUTE QUESTION TO RAG---")
        return "vectorstore"
    else:
        print("---ROUTE QUESTION TO LLM---")
        return "vectorstore"

def decide_to_generate(state:GraphState) -> GraphState:
    print("---ASSESS GRADED DOCUMENTS---")
    filtered_documents = state["documents"]

    if not filtered_documents:
        print("---DECISION: ALL DOCUMENTS ARE NOT RELEVANT TO QUESTION, WEB SEARCH---")
        return "Rewrite_Question"
    else:
        print("---DECISION: GENERATE---")
        return "generate"
    
def web_search_generation(state: GraphState) -> GraphState:
    print("---START WEB SEARCHING---")
    linkedin_link = state["linkedin_link"]
    question = state["question"]
    result = web_search_chain(
        linkedin_url=linkedin_link,
        question=question
    )
    return {
        **state, 
        "generation": result
        }

def addition_generation_node(state: GraphState) -> GraphState:
    print("---ADDITION GENERATION NODE---")
    generation = state["generation"] + state["query"]
    final_generation = addn_final_rag_chain.invoke({"query": generation})
    return {
        **state, 
        "generation": final_generation
        }

def create_json(state):
    print(" --- CREATING FINAL JSON FILE FROM GENERATED OUTPUT FROM LLM --- ")
    generate = state["generation"]

    json_result = information_chain.invoke({
        "query":generate
    })

    return {
        **state,
        "json_output":json_result
    }


def llm_fallback(state:GraphState) -> GraphState:
    """
    Generate answer using the LLM w/o vectorstore

    Args:
        state (dict): The current graph state

    Returns:
        state (dict): New key added to state, generation, that contains LLM generation
    """
    print("---LLM Fallback---")
    question = state["question"]
    generation = llm_chain.invoke({"question": question})
    return {
        **state,
        "generation": generation}

print("all nodes are created successfully")