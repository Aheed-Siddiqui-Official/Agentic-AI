### Setting Up =>

uv venv, uv pip install -r requirments.txt

### 

### LangGraph =>  Creating orchestrating workflows

Nodes, edges, graph, workflows



Gen AI

Ai that gen text, code, images, audio, video

prompt response

Input and output

answer question

no memory between calls

stateless

reactive



Agentic AI

ai that take actions on giving the goal

figure out the steps and give output

tools, apis, reads and writes data decides what to do next and can do loop until the goal is done

the ai has control of steps human just sets the goal

solve problem

memory involved

stateful

proactive



Yes, you were building agents  but they were "agent-shaped," not fully agentic

What you built in your LangChain course using create\_agent() is technically called an agent, but it sits at the beginning of the agentic AI spectrum, not the full thing. Let me show you the AI agent spectrum



#### AI Agent Spectrum

* Pure Generation
* Tool Using LLM
* React Agent
* Stateful Agent
* Multi Agent System
* Autonomous Agent



#### Why langraph?

* So lets go to varkala a place where clean beaches exists.
* but you dont want to book flight , book places or do anything so you spend 1 month to create a system that does this automatically (typical developer) so lets see the workflow how it is going to look like. 
* ok whole workflow is ready but lets get the things that Langchain will struggle and langgraph will excel in them. 
* Handling Loops Becomes Messy
* In LangChain, workflows are mostly linear.
* When an AI needs to retry, re-evaluate, or loop based on user feedback, we have to manually manage loops and conditions, which quickly makes the code complex and difficult to maintain.
* In LangGraph, loops are a native part of the workflow, so instead of manually managing while loops and conditions, we simply define nodes, edges, and conditional paths if the user rejects the itinerary, the workflow automatically returns to the planner node, otherwise it proceeds to the next step, making the system cleaner, easier to visualize, debug, and scale for multi-agent workflows.
* In LangChain, workflows are expected to run continuously, so tasks like waiting 24 hours for hotel booking availability become difficult to manage. We need external databases, schedulers to save and resume the workflow manually, which increases system complexity.
* Loops \& Re-evaluation
* Multi-Agent State Management
* Long Waiting Tasks
* Human-in-the-Loop Approval
* Scalability
* LangChain helps you call LLMs.
* LangGraph helps you orchestrate intelligent systems.
* The moment your AI needs memory, decisions, retries, waiting, or multiple agents you are no longer building a chain. You are building a graph.



### Workflows :-

#### Sequential Workflows :-

In LangGraph, a Sequential Workflow is the simplest, most straightforward way to connect tasks. It is a linear pipeline where data flows in a single direction from one step to the next like an assembly line in a factory.



Making a Cake

Ingredients -> baking -> icing/frosting



Each step should wait before completing of the upcoming step.



* A blog writing pipeline: topic → outline → draft → proofread → final article
* A data processing pipeline: raw data → clean → transform → summarize → output
* A translation pipeline: text → translate → grammar check → format → output



Goal =>

1. State(current position moving to next stage with previous information and adding new info init) 
2. Node(each working stage e.g. robot mixing dough, updates the state using edges)
3. Edges(route, hallways connecting robots, tell robots after you finish send the data/state to next robot)



e.g. research node -> draft node -> summarize node



#### Project sequential workflow :-

Raw Data -> Editor Node -> Script Writer Node -> Hinglish Node -> O/P





























