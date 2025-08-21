# Assignment 3
from project import model
from agents import Agent, Runner,ModelSettings,function_tool
import asyncio

@function_tool#(is_enabled=False)
def add(a:int , b:int)->int:
    return a+b

@function_tool#(is_enabled=False)
def weather_tool(city:str)->str:
    return f"The weather of the {city} is dry hot"

math_agent = Agent(name="Orignal agent",model=model,tools=[add],
    model_settings=ModelSettings(temperature=0.1),instructions="You`re helpful math assistant.")

async def main():
    query=["What is 5+7?", "Calculate 12 +30", "Add 100 and 20"]
    for Q in query:
        result = await Runner.run(math_agent, Q)
        print(f"Question: {Q}")
        print(f"Answer: {result.final_output}")

if __name__ == "__main__":
    asyncio.run(main())

# Output
# Question: What is 5+7?
# Answer: The sum of 5 and 7 is 12.

# Question: Calculate 12 +30
# Answer: The sum of 12 and 30 is 42.

# Question: Add 100 and 20
# Answer: The sum of 100 and 20 is 120.