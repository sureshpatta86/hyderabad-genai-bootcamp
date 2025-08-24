import os
from dotenv import load_dotenv
from pydantic import BaseModel
from langgraph.prebuilt import create_react_agent
from langchain_groq import ChatGroq
import json

load_dotenv()

class TravelPlan(BaseModel):
    destination: str
    start_date: str
    end_date: str
    budget: float

# Create a model with structured output
model = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0
)

# Use structured output
structured_model = model.with_structured_output(TravelPlan)

# Create the travel plan
prompt = """
Extract the travel information from the following request and return it in the specified format:
"I want to travel to Paris from 2025-10-01 to 2025-10-10 with a budget of 1500000.00 INR"
"""

try:
    travel_plan = structured_model.invoke(prompt)
    
    print(f"Destination: {travel_plan.destination}")
    print(f"Start Date: {travel_plan.start_date}")
    print(f"End Date: {travel_plan.end_date}")
    print(f"Budget: {travel_plan.budget}")
    
except Exception as e:
    print(f"Error: {e}")
    # Fallback to manual parsing
    travel_plan = TravelPlan(
        destination="Paris",
        start_date="2025-10-01",
        end_date="2025-10-10", 
        budget=1500000.00
    )
    
    print("Using fallback data:")
    print(f"Destination: {travel_plan.destination}")
    print(f"Start Date: {travel_plan.start_date}")
    print(f"End Date: {travel_plan.end_date}")
    print(f"Budget: {travel_plan.budget}")