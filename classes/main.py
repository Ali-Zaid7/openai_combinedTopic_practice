from project import model
from agents import Agent, function_tool,Runner,enable_verbose_stdout_logging,ModelSettings
from agents.agent import StopAtTools

enable_verbose_stdout_logging()
@function_tool
def get_weather(city:str)->str:
    return f"The weather in [city] is sunny"

@function_tool
def get_support_details(city:str)->str:
    return f"The support details for {city} is 123455"

agent = Agent(name="Haiku Agent",instructions="Always responds in Haiku",
               tools=[get_support_details,get_weather], model=model,
               tool_use_behavior=StopAtTools(stop_at_tool_names=["get_support_details"]),
               model_settings=ModelSettings(tool_choice="none",parallel_tool_calls=False),
               reset_tool_choice=False,) 
            #    tool_use_behavior="stop_on_first_tool")
            #    model_settings=ModelSettings(tool_choice="required"))
#stp_at.. stops LLM to reedit the query answer after 1st tool call
res= Runner.run_sync(agent, "Hi", max_turns=2)
print(res.final_output)
