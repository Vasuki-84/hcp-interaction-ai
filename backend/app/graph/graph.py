from typing import Annotated, TypedDict
from urllib import response
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage, SystemMessage, ToolMessage, AIMessage
from langgraph.prebuilt import ToolNode, tools_condition
from app.core.config import settings
from app.tools.tools import TOOLS
class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

# Initialize LLM

# PART 1:
llm = ChatGroq(
    model=settings.MODEL_NAME,
    api_key=settings.GROQ_API_KEY,
    temperature=0
)

# PART 2: 
llm_with_tools = llm.bind_tools(TOOLS)


#  PART 3: 
def chatbot(state: AgentState):
    from datetime import datetime
    current_dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    sys_msg = SystemMessage(content=f'''You are an AI assistant helping a life science sales representative manage HCP (Healthcare Professional) interactions.
Current Date and Time: {current_dt}

Your primary role is to process conversational input from the user and populate interactions for them to review.
Always confirm with the user before actually editing an existing interaction.
Use the tools provided to:
- extract_entities: to extract structured data from raw chat input and auto-populate the UI form for the user to review.
- edit_interaction: to update a specific field of an existing interaction.
- fetch_past_interactions: to pull context about an HCP.
- suggest_follow_up: to generate tasks based on topics and outcomes.
- log_interaction: DO NOT CALL THIS TOOL to save new interactions. The user will save the interaction manually after you populate the form.

When the user provides interaction notes:

- Always call extract_entities.
- Fill EVERY field that is mentioned.
- Return "" only if the field is not mentioned.

Important extraction rules:

- outcomes:
  Final result or decision of the meeting.
  Examples:
  agreed to evaluate the product
  proposal accepted
  proposal rejected
  concerns raised
  decided not to prescribe

- follow_up_actions:
  Future actions after the meeting.
  Examples:
  send clinical trial data tomorrow
  email brochure
  call next week
  schedule follow-up meeting

These two fields are completely independent.
Never copy one into the other.

When extracting entities, strictly follow these field mapping rules:
- hcp_name: Main HCP only.
- attendees: ADDITIONAL attendees only. NEVER include the main HCP here. Leave empty if no one else is mentioned.
- interaction_date & interaction_time: Always extract if explicitly mentioned (e.g., 'February 20, 2024', 'today', '10 AM', '2:30 PM').
- outcomes: ALWAYS extract if a meeting result, decision, agreement, or request is mentioned (e.g., 'agreed to evaluate the product', 'proposal accepted', 'concerns raised'). Keep distinct from follow-up actions.
- follow_up_actions: ALWAYS extract if a future action, next step, or planned task is mentioned (e.g., 'will follow up next Monday', 'send clinical data'). Keep distinct from outcomes.
NEVER hallucinate values. If a field is not mentioned, leave it empty instead of filling it with another field's value.

When inferring sentiment, use the following explicit rules:
Positive: doctor showed interest, successful meeting, positive feedback, agreement, appreciation, acceptance, productive discussion, willingness for follow-up.
Negative: rejection, complaint, dissatisfaction, poor feedback, refusal, concern, issue, conflict, unsuccessful meeting.
Neutral: factual conversations, factual descriptions only, meeting happened, products discussed, marketing materials shared, samples distributed, follow-up mentioned, no positive or negative emotional language.
If the text contains both positive and negative signals, choose the strongest one.
If there is insufficient evidence, ALWAYS return Neutral. There must never be a default value of Negative when sentiment is missing, uncertain, or purely factual. Use Neutral as the fallback.
Do not hardcode examples. Use reasoning from the conversation text.
''')
    messages = [sys_msg] + state["messages"]
    response = llm_with_tools.invoke(messages)
    print("\n========== TOOL CALL ==========")

    if hasattr(response, "tool_calls"):
       print(response.tool_calls)

    print("===============================\n")
    return {"messages": [response]}

# PART 4:
tool_node = ToolNode(TOOLS)

#  PART 5:
def after_tools(state: AgentState):
    # Terminate the graph immediately after extract_entities to prevent LLM errors on the second pass.
    for msg in reversed(state["messages"]):
        if isinstance(msg, AIMessage):
            if msg.tool_calls:
                for tc in msg.tool_calls:
                    if tc["name"] == "extract_entities":
                        return END
            break
    return "chatbot"

# PART  6:
graph_builder = StateGraph(AgentState)
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("tools", tool_node)

graph_builder.add_edge(START, "chatbot")
graph_builder.add_conditional_edges(
    "chatbot",
    tools_condition,
)
graph_builder.add_conditional_edges("tools", after_tools)

agent = graph_builder.compile()

# PART 7:
def process_chat(messages_data: list[dict]):
    from langchain_core.messages import HumanMessage, AIMessage
    from app.core.logger import logger
    
    logger.info("--- Starting AI Interaction Processing ---")
    
    formatted_messages = []
    for msg in messages_data:
        if msg["role"] == "user":
            formatted_messages.append(HumanMessage(content=msg["content"]))
        elif msg["role"] == "assistant":
            formatted_messages.append(AIMessage(content=msg["content"]))
    
    state = {"messages": formatted_messages}
    try:
        result = agent.invoke(state)
        logger.info("LangGraph execution completed successfully.")
    except Exception as e:
        logger.error(f"LLM or Tool invocation error: {str(e)}")
        return {
            "response": "I apologize, but I encountered an error while processing the interaction data. Could you please provide the details again or rephrase?",
            "extracted_data": {
                "hcp_name": "",
                "interaction_type": "",
                "interaction_date": "",
                "interaction_time": "",
                "attendees": "",
                "topics_discussed": "",
                "materials_shared": "",
                "samples_distributed": "",
                "sentiment": "Neutral",
                "outcomes": "",
                "follow_up_actions": ""
            }
        }
    
    response_text = ""
    extracted_data = None
    
    new_messages = result["messages"][len(state["messages"]):]
    
    # Detailed Logging for AI Output
    for msg in new_messages:
        if isinstance(msg, AIMessage):
            logger.info(f"AI Raw Output Content: {msg.content}")
            if msg.tool_calls:
                logger.info(f"AI Tool Calls: {msg.tool_calls}")
        if hasattr(msg, 'name') and msg.name:
            logger.info(f"Tool Output ({msg.name}): {msg.content}")

    # Extract the entities if the tool was called
    for msg in new_messages:
        if isinstance(msg, AIMessage) and msg.tool_calls:
            for tc in msg.tool_calls:
                if tc["name"] == "extract_entities":
                    extracted_data = tc["args"]
                    logger.info(f"Structured Extraction JSON: {extracted_data}")

    # Normalize JSON payload
    if extracted_data is not None:
        import datetime
        d = extracted_data.get("interaction_date") or ""
        t = extracted_data.get("interaction_time") or ""
        
        # Explicit relative date normalization
        if d:
            d_lower = d.lower()
            today = datetime.date.today()
            if "today" in d_lower:
                d = today.strftime("%Y-%m-%d")
            elif "yesterday" in d_lower:
                d = (today - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
            elif "tomorrow" in d_lower:
                d = (today + datetime.timedelta(days=1)).strftime("%Y-%m-%d")

        # Explicit relative time normalization
        if t:
            t_upper = t.upper()
            if "10 AM" in t_upper:
                t = "10:00"
            elif "2 PM" in t_upper:
                t = "14:00"
            elif "2:30 PM" in t_upper:
                t = "14:30"
            elif "NOON" in t_upper:
                t = "12:00"
                
        outcomes = extracted_data.get("outcomes") or ""
        follow_up = extracted_data.get("follow_up_actions") or ""
        
        # Never allow outcomes and follow_up_actions to copy each other
        if outcomes and follow_up and outcomes.strip().lower() == follow_up.strip().lower():
            follow_up = "" # Outcomes take precedence based on assignment

        normalized_data = {
            "hcp_name": extracted_data.get("hcp_name") or "",
            "interaction_type": extracted_data.get("interaction_type") or "",
            "interaction_date": d,
            "interaction_time": t,
            "attendees": extracted_data.get("attendees") or "",
            "topics_discussed": extracted_data.get("topics_discussed") or "",
            "materials_shared": extracted_data.get("materials_shared") or "",
            "samples_distributed": extracted_data.get("samples_distributed") or "",
            "sentiment": extracted_data.get("sentiment") or "Neutral",
            "outcomes": outcomes,
            "follow_up_actions": follow_up
        }
        extracted_data = normalized_data
        response_text = "I extracted the interaction details successfully. Please review the populated form and click Save Interaction."

    else:
        # Set the appropriate conversational response if no extraction tool was used
        for msg in reversed(result["messages"]):
            if isinstance(msg, AIMessage) and msg.content:
                response_text = msg.content
                break
                
    logger.info(f"Frontend Payload -> Response: {response_text}, Extracted Data: {extracted_data}")
    logger.info("--- End AI Interaction Processing ---")
    return {"response": response_text, "extracted_data": extracted_data}