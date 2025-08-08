from project import model
from agents import Agent, Runner, enable_verbose_stdout_logging,function_tool,ModelSettings
from dataclasses import dataclass

enable_verbose_stdout_logging()
@function_tool(is_enabled=True)
def get_weather(city:str)->str:
    return f"The weather in {city} is Suuny"

# Create the agent
agent = Agent(
    name="Haiku Agent",tools=[get_weather],
    model=model,
    model_settings=ModelSettings(tool_choice="none"),
    instructions="Help Users"
)

res = Runner.run_sync(agent, "What is the weather in Berlin")
print(res.final_output)#Output:The weather in Berlin is Sunny.
print(res.last_agent.name)