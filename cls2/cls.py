
from model import model, external_client, set_default_openai_client
from agents import function_tool, Agent,Runner

@function_tool
def get_weather(city: str)->str:
    return f"The weather in {city} is sunny"

agent=Agent(name="Haiku agent",
             instructions="Always respond in haiku form",tools=[get_weather])

res= Runner.run_sync(agent, "What is the weather in Tokyo", )
print(res.final_output) 

