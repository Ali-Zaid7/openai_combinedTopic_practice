from project import model
import asyncio
from agents.extensions import handoff_filters
from agents import Agent, handoff,Runner,enable_verbose_stdout_logging,function_tool

@function_tool
def weather(city:str)->str:
    return f"The weather in {city} is dry hot"

enable_verbose_stdout_logging()
refund_agent = Agent(name="Refund agent", instructions="Answer briefly to the user queries with dummy details about dummy refund refunds.",model=model)

general_agent = Agent(name="General agent", tools=[weather],
              handoffs=[handoff(agent=refund_agent, tool_name_override="refund_order_agent",
              tool_descr=iption_override="Handles the refund request",is_enabled=True, input_filter=handoff_filters.remove_all_tools)]  ,model=model)

async def main():
    res = await Runner.run(general_agent, """ What is the weather in Karachi also I want to 
                           refund my order of T-shirt due to its small unfitable size of 
                           100inches also give detais about order id:123456 and amount 100 """)
    print(res.final_output)
    print("Last Agent: ",res.last_agent.name)

if __name__ == "__main__":
    asyncio.run(main())