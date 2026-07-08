from typing import Annotated, TypedDict
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage, SystemMessage, ToolMessage
from langgraph.prebuilt import ToolNode, tools_condition
from app.core.config import settings
from app.tools.tools import TOOLS

# State definition
class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

# Initialize LLM
llm = ChatGroq(
    model=settings.MODEL_NAME,
    api_key=settings.GROQ_API_KEY,
    temperature=0
)
llm_with_tools = llm.bind_tools(TOOLS)

def chatbot(state: AgentState):
    sys_msg = SystemMessage(content='''You are an AI assistant helping a life science sales representative manage HCP (Healthcare Professional) interactions.
Your primary role is to process conversational input from the user and log interactions into the database.
Always confirm with the user before actually logging or editing an interaction.
Use the tools provided to:
- log_interaction: to save a completely populated interaction.
- edit_interaction: to update a specific field of an existing interaction.
- extract_entities: to extract structured data from raw chat input.
- fetch_past_interactions: to pull context about an HCP.
- suggest_follow_up: to generate tasks based on topics and outcomes.

If the user provides raw notes, extract the entities, ask for any missing required fields (hcp_name, interaction_type, interaction_date, interaction_time), and then propose the structured data. Once confirmed, use log_interaction.
''')
    messages = [sys_msg] + state["messages"]
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}

tool_node = ToolNode(TOOLS)

graph_builder = StateGraph(AgentState)
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("tools", tool_node)

graph_builder.add_edge(START, "chatbot")
graph_builder.add_conditional_edges(
    "chatbot",
    tools_condition,
)
graph_builder.add_edge("tools", "chatbot")

agent = graph_builder.compile()

def process_chat(messages_data: list[dict]):
    from langchain_core.messages import HumanMessage, AIMessage
    
    formatted_messages = []
    for msg in messages_data:
        if msg["role"] == "user":
            formatted_messages.append(HumanMessage(content=msg["content"]))
        elif msg["role"] == "assistant":
            formatted_messages.append(AIMessage(content=msg["content"]))
        # In a real app we'd also handle ToolMessages to reconstruct the full state graph history correctly
    
    state = {"messages": formatted_messages}
    result = agent.invoke(state)
    
    # Extract the last message content
    return result["messages"][-1].content
