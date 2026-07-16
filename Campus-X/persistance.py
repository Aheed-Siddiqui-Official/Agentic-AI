from langgraph.graph import StateGraph, START, END
from typing import TypedDict
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langgraph.checkpoint.memory import InMemorySaver

load_dotenv()

llm = ChatGroq(model="llama-3.3-70b-versatile")

class JokeState(TypedDict):
    topic : str
    joke: str
    explanation : str

def generate_joke(state:JokeState):

    prompt = f'generate a joke on the topic {state['topic']}'
    response = llm.invoke(prompt).content

    return {'joke':response}

def generate_explanation(state:JokeState):

    prompt = f'write an explanation for the joke - {state['joke']}'
    response = llm.invoke(prompt).content

    return {'explanation': response}

graph = StateGraph(JokeState)

graph.add_node('generate_joke', generate_joke)
graph.add_node('generate_explanation', generate_explanation)

graph.add_edge(START, 'generate_joke')
graph.add_edge("generate_joke", 'generate_explanation')
graph.add_edge("generate_explanation", END)

checkpointer = InMemorySaver()

workflow = graph.compile(checkpointer=checkpointer)

# thread 1
config1 = {"configurable" : {"thread_id": "1"}}
print(workflow.invoke({'topic':'pizza'}, config=config1))

workflow.get_state(config1)

print(list(workflow.get_state_history(config1)))

# thread 2
config2 = {"configurable" : {"thread_id": "2"}}
print(workflow.invoke({'topic':'pasta'}, config=config2))

workflow.get_state(config2)

print(list(workflow.get_state_history(config2)))