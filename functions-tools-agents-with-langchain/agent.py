import datetime
import openai
import os
import requests
import wikipedia

from dotenv import load_dotenv, find_dotenv
from pydantic import BaseModel, Field
from typing import Dict

from langchain.agents import AgentExecutor
from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser
from langchain.agents.format_scratchpad import format_to_openai_functions
from langchain.memory import ConversationBufferMemory
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema.agent import AgentFinish
from langchain.schema.runnable import RunnablePassthrough
from langchain.tools import render, tool

from langchain_community.chat_models import ChatOpenAI


_ = load_dotenv(find_dotenv())
openai.api_key = os.environ['OPENAI_API_KEY']

class OpenMeteoInput(BaseModel):
    latitude: float = Field(..., description="Latitude of the location to fetch weather data for")
    longitude: float = Field(..., description="Longitude of the location to fetch weather data for")

@tool(args_schema=OpenMeteoInput)
def get_current_temperature(latitude: float, longitude: float) -> Dict:
    """Fetch current temperature for given coordinates.

    Args: 
        latitude: float
        longtitude: float
    Returns: Dict
    """
    
    BASE_URL = "https://api.open-meteo.com/v1/forecast"
    
    params = {
        'latitude': latitude,
        'longitude': longitude,
        'hourly': 'temperature_2m',
        'forecast_days': 1,
    }

    response = requests.get(BASE_URL, params=params)
    
    if response.status_code == 200:
        results = response.json()
    else:
        raise Exception(f"API Request failed with status code: {response.status_code}")

    current_utc_time = datetime.datetime.utcnow()
    time_list = [datetime.datetime.fromisoformat(time_str.replace('Z', '+00:00')) for time_str in results['hourly']['time']]
    temperature_list = results['hourly']['temperature_2m']
    
    closest_time_index = min(range(len(time_list)), key=lambda i: abs(time_list[i] - current_utc_time))
    current_temperature = temperature_list[closest_time_index]
    
    return f'The current temperature is {current_temperature}°C'

@tool
def search_wikipedia(query: str) -> str:
    """Run Wikipedia search and get page summaries.

    Args: 
        query: string
    Returns: string
    """
    page_titles = wikipedia.search(query)
    summaries = []
    for page_title in page_titles[:3]:
        try:
            wiki_page =  wikipedia.page(title=page_title, auto_suggest=False)
            summaries.append(f"Page: {page_title}\nSummary: {wiki_page.summary}")
        except: 
            pass
    if not summaries:
        return "No good Wikipedia Search Result was found"
    return "\n\n".join(summaries)

def main(input: str):
    """Main function without agent.
    
    Args:
        input: string
    """
    tools = [get_current_temperature, search_wikipedia]
    functions = [render.format_tool_to_openai_function(f) for f in tools]

    model = ChatOpenAI().bind(functions=functions)

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "You are helpful but sassy assistant"),
            ("user", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad")
        ]
    )

    chain = prompt | model | OpenAIFunctionsAgentOutputParser()

    return chain.invoke(
        {
            "input": input,
            "agent_scratchpad": []
        }
    )

# result = main(input="what is the weather is sf?")
# print(result)

def run_agent(input: str):
    """Main function for running agent.
    
    Args:
        input: string
    """
    intermediate_steps = []
    while True:
        tools = [get_current_temperature, search_wikipedia]
        functions = [render.format_tool_to_openai_function(f) for f in tools]

        model = ChatOpenAI().bind(functions=functions)

        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", "You are helpful but sassy assistant"),
                ("user", "{input}"),
                MessagesPlaceholder(variable_name="agent_scratchpad")
            ]
        )

        chain = prompt | model | OpenAIFunctionsAgentOutputParser()

        agent_chain = RunnablePassthrough.assign(
            agent_scratchpad= lambda x: format_to_openai_functions(x["intermediate_steps"])
        ) | chain
        
        result = agent_chain.invoke(
            {
                "input": input, 
                "intermediate_steps": intermediate_steps
            }
        )
        if isinstance(result, AgentFinish):
            return result
        tool = {
            "search_wikipedia": search_wikipedia, 
            "get_current_temperature": get_current_temperature,
        }[result.tool]
        observation = tool.run(result.tool_input)
        intermediate_steps.append((result, observation))

# print(run_agent("what is the weather is sf?"))
# print(run_agent("what is super junior?"))
# print(run_agent("hi!"))

def run_agent(input: str):
    """Main function for running agent with agent executor.
    
    Args:
        input: string
    """
    tools = [get_current_temperature, search_wikipedia]
    functions = [render.format_tool_to_openai_function(f) for f in tools]

    model = ChatOpenAI().bind(functions=functions)

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "You are helpful but sassy assistant"),
            ("user", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad")
        ]
    )

    chain = prompt | model | OpenAIFunctionsAgentOutputParser()
    agent_chain = RunnablePassthrough.assign(
            agent_scratchpad= lambda x: format_to_openai_functions(x["intermediate_steps"])
        ) | chain
    agent_executor = AgentExecutor(agent=agent_chain, tools=tools, verbose=True)
    
    result = agent_executor.invoke(
        {
            "input": input
        }
    )
    
    return result

# print(run_agent("what is super junior?"))
# print(run_agent("hello. my name is Yoona"))
# print(run_agent("what is my name?"))

def run_agent(input: str):
    """Main function for running agent with agent executor, and with ch.
    
    Args:
        input: string
    """
    tools = [get_current_temperature, search_wikipedia]
    functions = [render.format_tool_to_openai_function(f) for f in tools]

    model = ChatOpenAI().bind(functions=functions)

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "You are helpful but sassy assistant"),
            MessagesPlaceholder(variable_name="chat_history"),
            ("user", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad")
        ]
    )

    agent_chain = RunnablePassthrough.assign(
        agent_scratchpad= lambda x: format_to_openai_functions(x["intermediate_steps"])
    ) | prompt | model | OpenAIFunctionsAgentOutputParser()
    memory = ConversationBufferMemory(return_messages=True,memory_key="chat_history")
    agent_executor = AgentExecutor(agent=agent_chain, tools=tools, verbose=True, memory=memory)
    
    result = agent_executor.invoke(
        {
            "input": input
        }
    )
    
    return result

# print(run_agent("what is super junior?"))
# print(run_agent("hello. my name is Yoona"))
# print(run_agent("what is my name?"))
