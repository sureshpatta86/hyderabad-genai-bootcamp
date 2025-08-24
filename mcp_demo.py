from dotenv import load_dotenv
load_dotenv()
import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
import os

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

async def run_mcp_agent():
    # Initialize MultiServerMCP client with GitHub and filesystem servers
    client = MultiServerMCPClient(
       {
           # GitHub server configuration for repository operations
           "github": {
               "command": "npx",
               "args": [
                   "-y",
                   "@modelcontextprotocol/server-github"
               ],
               "env": {
                   "GITHUB_PERSONAL_ACCESS_TOKEN": GITHUB_TOKEN
               },
               "transport": "stdio"
           },
       # Filesystem server configuration for local file operations
       "filesystem": {
           "command": "npx",
           "args": [
               "-y",
               "@modelcontextprotocol/server-filesystem",
               "/USERS/SURESHPATTA/developer/learnings/genai-bootcamp"
               
        
         ],
           "transport": "stdio"
       },
       "SureshFileSystem": {
               "command": "python",
               "args": [
                   "./SureshFileSystem.py"
               ],
               "transport":"stdio"
           }

       }
    )
    
    tools = await client.get_tools()
    print(tools)
    agent = create_react_agent("groq:llama-3.1-8b-instant", tools)
    response = await agent.ainvoke({"messages": "delte a file name hyd.txt in my machine use the SureshFileSystem"})
    
    print(response["messages"][-1].content)


if __name__ == "__main__":
    asyncio.run(run_mcp_agent())