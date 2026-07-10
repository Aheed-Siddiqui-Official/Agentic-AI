import os
from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode
from langchain_groq import ChatGroq
from langchain_tavily import TavilySearch
from dotenv import load_dotenv

load_dotenv()

# ====================== TOOLS ======================
search_tool = TavilySearch(
    max_results=3,
    search_depth="advanced",
    include_answer=True,
)

tools = [search_tool]

# ====================== LLMs ======================
writer_llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.7,
    max_tokens=1024,
)

writer_llm_with_tools = writer_llm.bind_tools(tools, tool_choice="auto")

reviewer_llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.1,
)

# ====================== STATE ======================
class State(TypedDict):
    topic: str
    messages: Annotated[list, add_messages]
    draft: str
    review_feedback: str
    is_approved: bool
    attempt: int


# ====================== PROMPTS ======================
WRITER_SYSTEM_PROMPT = """You are an expert LinkedIn content writer. 
Your job is to write engaging, professional LinkedIn posts.
If the topic needs current info, statistics or trends, use the web search tool first.
Rules:
- Strong hook in first line
- One clear takeaway
- Short paragraphs, easy to skim
- ~150-200 words
- End with question or CTA
- No hashtags"""

REVIEWER_SYSTEM_PROMPT = """You are a strict LinkedIn content reviewer.
Evaluate the post against these criteria:
1. Strong hook
2. One clear valuable takeaway
3. Easy to skim (short paragraphs)
4. ~150-200 words
5. Ends with engaging question/CTA
6. Professional but human tone
7. No hashtags

Respond EXACTLY in this format:
VERDICT: APPROVED or REJECTED
FEEDBACK: <one short paragraph>"""

# ====================== NODES ======================
def writer_node(state: State):
    attempt = state.get("attempt", 0) + 1
    topic = state["topic"]
    previous_feedback = state.get("review_feedback", "")

    if attempt == 1:
        user_message = f"Write a LinkedIn post on: {topic}. Use search if you need fresh data."
    else:
        user_message = f"""Previous draft was rejected. 
Here is the feedback: {previous_feedback}

Write an improved version that fixes every issue."""

    messages = [
        ("system", WRITER_SYSTEM_PROMPT),
        ("human", user_message)
    ]

    response = writer_llm_with_tools.invoke(messages)

    return {
        "messages": messages + [response],  # Important: pass full history
        "attempt": attempt,
    }


tool_node = ToolNode(tools)


def extract_draft_node(state: State):
    last_message = state["messages"][-1]
    draft = last_message.content if hasattr(last_message, "content") else str(last_message)
    
    print("\n=== GENERATED DRAFT ===\n")
    print(draft)
    print("\n=======================\n")

    return {"draft": draft}


def reviewer_node(state: State):
    draft = state["draft"]

    prompt = f"Review this LinkedIn post:\n\n{draft}"

    response = reviewer_llm.invoke([
        ("system", REVIEWER_SYSTEM_PROMPT),
        ("human", prompt)
    ])

    review_text = response.content.strip()
    is_approved = "APPROVED" in review_text.upper()

    if "FEEDBACK:" in review_text:
        feedback = review_text.split("FEEDBACK:", 1)[1].strip()
    else:
        feedback = review_text

    verdict = "APPROVED" if is_approved else "REJECTED"
    print(f"[Verdict: {verdict}]")
    print(f"[Feedback: {feedback[:300]}...]\n")

    return {
        "review_feedback": feedback,
        "is_approved": is_approved,
    }


# ====================== ROUTERS ======================
def should_use_tool(state: State):
    last_message = state["messages"][-1]
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools"
    return "extract_draft"


def should_stop_looping(state: State):
    if state.get("is_approved"):
        print("✅ Post approved!")
        return END
    if state.get("attempt", 0) >= 3:
        print("Reached maximum attempts.")
        return END
    return "writer"


# ====================== GRAPH ======================
graph = StateGraph(State)

graph.add_node("writer", writer_node)
graph.add_node("tools", tool_node)
graph.add_node("extract_draft", extract_draft_node)
graph.add_node("reviewer", reviewer_node)

graph.add_edge(START, "writer")
graph.add_conditional_edges("writer", should_use_tool)
graph.add_edge("tools", "extract_draft")   # After tool → extract draft
graph.add_edge("extract_draft", "reviewer")
graph.add_conditional_edges("reviewer", should_stop_looping, {
    "writer": "writer",
    END: END
})

app = graph.compile()

# ====================== RUN ======================
if __name__ == "__main__":
    print("=" * 55)
    print("Welcome to the LinkedIn Post Generator")
    print("=" * 55)
    print("This tool will draft, review, and iterate until publish-ready.\n")

    topic = input("What topic do you want a LinkedIn post about?\n> ").strip()

    if not topic:
        print("No topic given.")
    else:
        print("\nStarting generation...\n")

        initial_state = {
            "topic": topic,
            "messages": [],
            "draft": "",
            "review_feedback": "",
            "is_approved": False,
            "attempt": 0,
        }

        final_state = app.invoke(initial_state)

        print("\n" + "=" * 55)
        print("FINAL LINKEDIN POST")
        print("=" * 55)
        print(final_state.get("draft", "No draft generated."))
        print("=" * 55)
        print(f"Total attempts: {final_state.get('attempt', 0)}")
        print(f"Approved: {final_state.get('is_approved', False)}")