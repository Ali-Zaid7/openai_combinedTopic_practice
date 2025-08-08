import asyncio,random
from project import model
from agents import Agent, Runner,function_tool,ItemHelpers
from openai.types.responses import ResponseTextDeltaEvent

@function_tool
def how_many_jokes()->int:
    return random.randint(1,10)

async def main():
    agent=Agent(name="Joker",tools=[how_many_jokes],
                 instructions="First call the `how_many_jokes` tool, then tell that many jokes.")
    
    result = Runner.run_streamed(agent, "Hi hello kese ho")
    print("====Run Starting====")
    async for event in result.stream_events():
        # We'll ignore the raw responses event deltas
        if event.type == "raw_response_event":
            continue
        elif event.type == "agent_updated_stream_event":
            print(f"Agent updated: {event.new_agent.name}")
        elif event.type == "run_item_stream_event":
            if event.item.type == "tool_call_item":
                print("-- Tool was called")
            elif event.item.type == "tool_call_output_item":
                print(f"--Tool output: {event.item.output}")
            elif event.item.type == "message_output_item":
                print(f"-- Message output: \n {ItemHelpers.text_message_output(event.item)}")
            else:
                pass #Ignore other event types

try:
    asyncio.run(main())
except:
    pass
print("=== Run complete ===")

