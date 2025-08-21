#Assignment#7

from agents import Agent, Runner, function_tool
from tavily import TavilyClient
from project import model
import asyncio, os
from dotenv import load_dotenv

load_dotenv(True)
tavily_api_key = os.getenv("TAVILY_API_KEY")
tavily_client = TavilyClient(api_key=tavily_api_key)

# Tool for the agent that uses Gemini first, then Tavily fallback automatically
@function_tool
def web_search_tool(query: str, agent_response: str = None) -> str:
    """Tool that queries Tavily if agent_response is None or not informative."""
    if not agent_response or "i don't know" in agent_response.lower() or "unable" in agent_response.lower():
        # Call Tavily for live results
        tavily_result = tavily_client.search(query)
        return f"Tavily says: {tavily_result}"
    return agent_response

agent = Agent(name="Agent", model=model, tools=[web_search_tool])

async def main():
    query = "who us engineer Moham Ali mirza and what is his slogan"
    
    # Agent will now use web_search_tool, which internally checks Tavily if needed
    agent_res = await Runner.run(agent, query)
    print("FINAL OUTPUT:", agent_res.final_output)

if __name__ == "__main__":
    asyncio.run(main())

# Output
# FINAL OUTPUT: Engineer Muhammad Ali Mirza is a Pakistani Islamic cleric and mechanical engineer, born on October 4, 1977, in Jhelum, Punjab.
# He obtained his mechanical engineering degree from the University of Engineering and Technology, Taxila. He is also known as Engineer Ali Mirza.
# While his "slogan" is mentioned in several search results, the exact slogan itself is not explicitly stated in the provided information.
