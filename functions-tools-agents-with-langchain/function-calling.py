import openai
import os

from dotenv import load_dotenv, find_dotenv
from pydantic import BaseModel, Field

from langchain_community.chat_models import ChatOpenAI
from langchain_core.utils.function_calling import convert_to_openai_function


_ = load_dotenv(find_dotenv())
openai.api_key = os.environ['OPENAI_API_KEY']

class pUser(BaseModel):
    name: str
    age: int
    email: str

foo_p = pUser(
    name="Yoona", 
    age=34, 
    email="yoona@gmail.com"
)

class WeatherSearch(BaseModel):
    """Call this with an airport code to get the weather at that airport.
    """
    airport_code: str = Field(description="airport code to get weather for")

def main(input: str):
    """Main for pydantic to OpenAI function.

    Args: 
        input: string
    """
    model = ChatOpenAI()

    functions = [
        convert_to_openai_function(WeatherSearch),
    ]

    model_with_functions = model.bind(functions=functions)

    result = model_with_functions.invoke(input)

    return result
    
result = main("what is the weather in sf?")
print(result)