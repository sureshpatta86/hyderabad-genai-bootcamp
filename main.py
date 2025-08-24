import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

from typing import Annotated

from typing_extensions import TypedDict

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

load_dotenv()

class State(TypedDict):
    # Messages have the type "list". The `add_messages` function
    # in the annotation defines how this state key should be updated
    # (in this case, it appends messages to the list, rather than overwriting them)
    messages: Annotated[list, add_messages]


graph_builder = StateGraph(State)

model = init_chat_model("llama-3.3-70b-versatile", model_provider="groq")

#response = model.invoke("What is Gen AI?")
#print(response.content)

def chatbot(state: State):
    return {"messages": [model.invoke(state["messages"])]}


# The first argument is the unique node name
# The second argument is the function or object that will be called whenever
# the node is used.
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)
graph = graph_builder.compile()

try:
   img = graph.get_graph().draw_mermaid_png()
   with open("graph.png", "wb") as f:
       f.write(img)
except Exception:
   pass

# w → Write mode (creates the file if it does not exist, or overwrites if it does).
# b → Binary mode (means you are writing binary data, like images or audio—not text).


def stream_graph_updates(user_input: str):
   for event in graph.stream({"messages": [{"role": "user", "content": user_input}]}):
       for value in event.values():
           print("Assistant:", value["messages"][-1].content)




while True:
   try:
       user_input = input("User: ")
       if user_input.lower() in ["quit", "exit", "q"]:
           print("Goodbye!")
           break
       stream_graph_updates(user_input)
   except:
       # fallback if input() is not available
       user_input = "What do you know about LangGraph?"
       print("User: " + user_input)
       stream_graph_updates(user_input)
       break


