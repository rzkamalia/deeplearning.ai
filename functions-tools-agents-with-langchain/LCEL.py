import openai
import os

from dotenv import load_dotenv, find_dotenv
from typing import List

from langchain.prompts import ChatPromptTemplate

from langchain.schema.runnable import RunnableMap
from langchain.schema.output_parser import StrOutputParser

from langchain_community.chat_models import ChatOpenAI
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import DocArrayInMemorySearch


_ = load_dotenv(find_dotenv())
openai.api_key = os.environ['OPENAI_API_KEY']

def simple_chain(input: str) -> str:
    """Main of simple chain.

    Args:
        input: string
    Returns: string
    """
    prompt = ChatPromptTemplate.from_template(
        "tell me a short joke about {topic}"
    )
    model = ChatOpenAI()
    output_parser = StrOutputParser()

    chain = prompt | model | output_parser

    result = chain.invoke(
        {
            "topic": input
        }
    )
    return result

result = simple_chain(input="super junior")
print(result)

def retrieve_doc(input: str) -> List:
    """Retrieve documment.

    Args:
        input: string
    Returns: string
    """
    vectorstore = DocArrayInMemorySearch.from_texts(
        [
            "harrison worked at kensho", 
            "bears like to eat honey"
        ],
        embedding=OpenAIEmbeddings()
    )
    retriever = vectorstore.as_retriever()

    return retriever.get_relevant_documents(input)

def complex_chain(input: str) -> str:
    """Main of complex chain.

    Args:
        input: string
    Returns: string
    """
    template = """
        Answer the question based only on the following context:
        {context}

        Question: {question}
    """
    prompt = ChatPromptTemplate.from_template(template)
    model = ChatOpenAI()
    output_parser = StrOutputParser()

    chain = RunnableMap(
        {
            "context": lambda x: retrieve_doc(x["question"]),
            "question": lambda x: x["question"],
        }
    ) | prompt | model | output_parser

    result = chain.invoke(
        {
            "question": input
        }
    )
    return result

# result = complex_chain(input="where did harrison work")
# print(result)

def run_in_batch(inputs: List) -> List:
    """Running in batch.

    Args: 
        inputs: List
    Returns: List
    """
    prompt = ChatPromptTemplate.from_template(
        "Tell me a short joke about {topic}"
    )
    model = ChatOpenAI()
    output_parser = StrOutputParser()

    chain = prompt | model | output_parser

    results = chain.batch(inputs)
    return results

inputs = [
    {"topic": "super junior"}, 
    {"topic": "shinee"},
]
# results = run_in_batch(inputs)
# print(results)