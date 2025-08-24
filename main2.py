import os
from dotenv import load_dotenv
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import InMemorySaver

load_dotenv()

checkpointer = InMemorySaver()

agent = create_react_agent(
    model="groq:llama-3.3-70b-versatile",  
    tools=[],  
    prompt="You are a helpful assistant",
    checkpointer=checkpointer
)

config = {"configurable": {"thread_id": "1"}}

# Run the agent
response =agent.invoke(
    {"messages": [{"role": "user", "content": "who is Modi"}]},
    {"configurable": {"thread_id": "1"}}
)

print(response["messages"][-1].content)

response =agent.invoke(
    {"messages": [{"role": "user", "content": "whats his age now?"}]},
    {"configurable": {"thread_id": "2"}}
)

print(response["messages"][-1].content)