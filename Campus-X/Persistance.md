# Campus X

Persistence refers to the ability to save and restore state of workflow overtime



concept of graph => execution order nodes and edges

concept of state => every node in state can read and write



final state removed after langgraph execution finishes



with persistence we can store data



with persistence we can store just not final values but intermediate value too



if server crashed we can resume from previous node so workflow will not start from scratch it will start from node



this is called fault tolerance and big feature of langgraph



can help to build chatbots



we can save the values in db or ram



Check pointer divides whole graph execution in check points



graph each super step become check pointer



threads is invoking a function multiple times



we alot a thread id unique using persistence to fetch the required thread

redis checkpointer
postgres checkpointer

benifits of persistance

STM
Fault tolerance
HITL
time travel





