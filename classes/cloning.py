from project import model
from agents import Agent, Runner,ModelSettings,function_tool

@function_tool#(is_enabled=False)
def calculator(a , b):
    return f"The result of calculator output is {a and b}"

@function_tool#(is_enabled=False)
def weather_tool(city:str)->str:
    return f"The weather of the {city} is dry hot"

orignal_agent = Agent(name="Orignal agent",model=model,
                      tools=[calculator,weather_tool],
                      model_settings=ModelSettings(temperature=0.7),
                   instructions="You`re helpful assistant.")

cloned_agent= orignal_agent.clone(name="Cloned", instructions="You`re creative.")

creative_agent=orignal_agent.clone( model=model,model_settings=ModelSettings(temperature=0.3),)
res= Runner.run_sync(creative_agent, "How`re you?", max_turns=2)
print(res.final_output)