import os
from dotenv import load_dotenv
from pydantic import BaseModel
from langgraph.prebuilt import create_react_agent

load_dotenv()

class MailResponse(BaseModel):
    subject: str
    body: str   


agent = create_react_agent(
    model="groq:llama-3.3-70b-versatile",  
    tools=[MailResponse],  
    prompt="You are a helpful assistant",
    #checkpointer=checkpointer
    response_format=MailResponse
)  

response = agent.invoke(
    {"messages": [{"role": "user", "content": "Send an email to Suresh stating you have a meeting today at 5pm."}]}
)

print(response["structured_response"].subject)
print(response["structured_response"].body)