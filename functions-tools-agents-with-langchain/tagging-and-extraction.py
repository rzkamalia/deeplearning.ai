import openai
import os

from dotenv import load_dotenv, find_dotenv
from pydantic import BaseModel, Field
from typing import List, Optional

from langchain.output_parsers.openai_functions import JsonOutputFunctionsParser
from langchain.prompts import ChatPromptTemplate

from langchain_community.chat_models import ChatOpenAI
from langchain_core.utils.function_calling import convert_to_openai_function


_ = load_dotenv(find_dotenv())
openai.api_key = os.environ['OPENAI_API_KEY']

class Tagging(BaseModel):
    """Tag the piece of text with particular info."""
    sentiment: str = Field(description="sentiment of text, should be `pos`, `neg`, or `neutral`")
    language: str = Field(description="language of text (should be ISO 639-1 code)")

def main_tagging(input: str):
    """Main tagging.
    
    Args:
        input: string
    """
    model = ChatOpenAI(temperature=0)

    tagging_functions = [convert_to_openai_function(Tagging)]
    
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "Think carefully, and then tag the text as instructed"),
            ("user", "{input}")
        ]
    )

    model_with_functions = model.bind(
        functions=tagging_functions,
        function_call={"name": "Tagging"}
    )

    tagging_chain = prompt | model_with_functions | JsonOutputFunctionsParser()
    
    result = tagging_chain.invoke(
        {
            "input": input
        }
    )

    return result

# result = main_tagging(input="I love super junior")
# print(result)

class Person(BaseModel):
    """Information about a person.
    """
    name: str = Field(description="person's name")
    age: Optional[int] = Field(description="person's age")

class Information(BaseModel):
    """Information to extract.
    """
    people: List[Person] = Field(description="List of info about people")

def main_extraction(input: str):
    """Main extraction.
    
    Args:
        input: string
    """
    model = ChatOpenAI(temperature=0)

    extraction_functions = [convert_to_openai_function(Information)]
    extraction_model = model.bind(
        functions=extraction_functions, 
        function_call={"name": "Information"}
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "Extract the relevant information, if not explicitly provided do not guess. Extract partial info"),
            ("user", "{input}")
        ]
    )

    extraction_chain = prompt | extraction_model | JsonOutputFunctionsParser()
    
    result = extraction_chain.invoke(
        {
            "input": input
        }
    )

    return result

result = main_extraction(input="My name is Yoona. I am 30 years old.")
print(result)