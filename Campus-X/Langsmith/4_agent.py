import os
import requests
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.tools import tool
from langchain_core.prompts import PromptTemplate
from langchain_classic.agents import create_react_agent, AgentExecutor
from langsmith import Client
from ddgs import DDGS  # Clean alternative to legacy DuckDuckGoSearchRun

load_dotenv()

# --- 1. Custom Robust Web Search Tool ---
@tool
def native_web_search(query: str) -> str:
    """
    Search the web for current events, release dates, or general knowledge questions.
    """
    with DDGS() as ddgs:
        results = [r["body"] for r in ddgs.text(query, max_results=3)]
        return "\n\n".join(results)

# --- 2. Custom Weather Retrieval Tool ---
@tool
def get_weather_data(city: str) -> str:
    """
    This function fetches the current weather data for a given city
    """
    url = f'https://api.weatherstack.com/current?access_key=f07d9636974c4120025fadf60678771b&query={city}'
    response = requests.get(url)
    return str(response.json())

# --- 3. Initialize Language Model Configuration ---
# Ensure GROQ_API_KEY is present in your .env file
llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)

# --- 4. Safely Fetch Public Prompt Template ---
client = Client()
prompt = client.pull_prompt("hwchase17/react", dangerously_pull_public_prompt=True)

# List of initialized tools
tools_list = [native_web_search, get_weather_data]

# --- 5. Construct Agent Runtime Pipeline ---
agent = create_react_agent(
    llm=llm,
    tools=tools_list,
    prompt=prompt
)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools_list,
    verbose=True,
    max_iterations=5,
    handle_parsing_errors=True  # Automatically manages structural anomalies
)

# --- 6. Execution Loop Execution Tracing ---
if __name__ == "__main__":
    user_query = "What is the birthdate and place of salman khan and current temperature of there?"
    print(f"Executing Agent Pipeline for query: '{user_query}'...\n")
    
    response = agent_executor.invoke({"input": user_query})
    
    print("\n--- Final Extracted Answer ---")
    print(response['output'])
