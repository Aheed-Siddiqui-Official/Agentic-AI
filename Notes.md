### Setting Up =>

uv venv, uv pip install -r requirments.txt

### 

### LangGraph =>  Creating orchestrating(the coordination of multiple autonomous AI agents—each specialized in a specific task—so they can collaborate to achieve complex goals) workflows

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

1. #### Sequential Workflows :-

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



#### 2\. Parallel Workflows :-

Multiple task running parallelly in langchain we cant do this that's why langgraph is used



* In LangGraph, a Parallel Workflow works exactly like Scenario B:
* In LangGraph, a Parallel Workflow (often called a Fan-Out / Fan-In pattern) is when a single node splits the flow into two or more independent branches that execute concurrently.
* Later, those branches merge back into a single point (called a Join Node) before the graph completes.
* In a parallel workflow, the State becomes even more magical. When the graph splits, multiple nodes are writing to the State simultaneously. LangGraph handles this safely by letting Node A write to its key (e.g., article\_text) and Node B write to its key (e.g., tweet\_text) without overriding or breaking each other's data.
* You define separate, specialized functions for each task that can run independently. yup not that big difference they are at the end python functions.
* In a parallel workflow, edges change from a simple "A to B" pathway into two specialized structural movements: Fan-Out and Fan-In.
* Fan-Out (The splitter)
* This occurs when a single node connects to multiple downstream nodes. Instead of creating a chain, you point one source to multiple targets. LangGraph detects this and automatically fires those target nodes concurrently.
* you will see it in code.



#### Fan-In (The Merger) :-

This occurs when multiple parallel nodes point to a single destination node. This acts as a synchronization barrier. LangGraph will automatically pause the workflow at this junction and wait until every single parallel branch completes its task before letting the final node execute.



#### Reducers :-

when multiple nodes target a single value of state in a class that cause overriding and for that reason reducers are used



#### 3\. Conditional Workflows :-



* Conditional edges
* Router functions
* LLM-based decision making
* RAG inside LangGraph (retrieval as a conditional path)
* add\_messages reducer



In a sequential workflow, the path is fixed - A → B → C, every single time.

In a conditional workflow, the path changes - A → (check something) → go to B or go to C depending on the answer.



##### Two main things in conditional workflow

###### Router Function

a router function regular python function read current state and return name of next node

This function doesn't do any real work. It only makes a decision  "based on what I see in the state, where should we go next?"



###### Edges

Instead of add\_edge (which always goes to the same node), you use add\_conditional\_edges (which calls the router function to decide).



* Rule based decision
* LLM based decision



so we are going to create a smart college chatbot you can create it for your own college as well and show it as a major or minor project.



FAISS vector store works in your internal storage like ram but chroma db works in you own folder and makes a new folder in the current directory both are vector stores



add\_messages reducer6



#### 4\. Iterative Workflows :-



reactive loop

feedback loop till some limits

tools also used

multi agent post generator



#### 5\. Human in the loop :-



Human in the loop (HITL) 



Look, let’s be honest about real-world scenarios: You simply cannot trust an AI blindly.



That is exactly why you need human approval for critical tasks. Imagine you are executing a full, end-to-end workflow, and something high-stakes comes up. You can't just let the AI run wild. You have to stop the workflow right in the middle, pause it, and wait for a human to give the green light.



In the world of AI architecture, this exact mechanism is known as Human-in-the-Loop (HITL).



for human in the loop you need 2 new things 



1\. interrupt() the pause function



Inside a node, when you call interrupt(some\_data), LangGraph:



Stops execution immediately

Sends some\_data up to your code (so you can show it to the user)

Waits for input

 



2\. Command(resume=...) — the resume function



After the graph is paused, you resume it by calling app.invoke() again but with a Command:









