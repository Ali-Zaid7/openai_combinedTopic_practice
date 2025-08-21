# Assignment 6
from project import model
from agents import Agent, Runner,function_tool
import asyncio,json,requests,os

weather_api_key =os.getenv("WEATHER_API_KEY")

@function_tool
def add(a:int, b:int)->int:
    """Returns the sum of numbers"""
    result = a+b
    return json.dumps({"error":False , "message": f"The sum of {a} and {b} is {a+b}"})

@function_tool
def weather_tool(city:str)->str:
    """Returns the temperature of city"""
    try:
        url=f"http://api.weatherapi.com/v1/current.json?key={weather_api_key}&q={city}&qi=no"
        response=requests.get(url).json()
        temp_c =response["current"]["temp_c"]
        condition=response["current"]["condition"]["text"]
        return json.dumps({"error": False, "message":f"The weather in {city} is {temp_c}°C with {condition}"})
    
    except Exception as e:
        return json.dumps({"error":True, "message":f"Could not fetch the weather of {city}. \nError: {e}"})

agent = Agent(name="Weather agent",model=model,tools=[weather_tool,add])

async def main():
    query=["What is weather in Karachi?", "What is weather in Antarctica north region?", "Sum of 7 and 3"]
    for Q in query:
        result = await Runner.run(agent, Q)
        print(f"Question: {Q}")
        print(f"Answer: {result.final_output}")

if __name__ == "__main__":
    asyncio.run(main())

#Output
# Question: What is weather in Karachi?
# Answer: The weather in Karachi is 29.0°C with moderate or heavy rain with thunder.
# Question: What is weather in Antarctica north region?
# Answer: I can only provide weather for a specific city. Is there a particular city in mind?
# Question: Sum of 7 and 3
# Answer: The sum of 7 and 3 is 10.