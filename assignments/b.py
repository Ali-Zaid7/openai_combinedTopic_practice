# Assignment 4
from project import model
from agents import Agent, Runner,ModelSettings,function_tool
import asyncio, os,json,requests

weather_api_key =os.getenv("WEATHER_API_KEY")

@function_tool
def weather_tool(city:str)->str:
    """Returns the temperature of city"""
    url = f"http://api.weatherapi.com/v1/current.json?key={weather_api_key}&q={city}&aqi=no"

    try:
        response=requests.get(url).json()
        temp_c= response["current"]["temp_c"]
        condition= response["current"]["condition"]["text"]
        return f"The current temperature in {city} is {temp_c}°C with {condition}."
    
    except Exception as e:
        return f"Sorry could not fetch weather for {city}.\n\t Error: {e}"

agent = Agent(name="Weather agent",model=model,tools=[weather_tool],
    model_settings=ModelSettings(temperature=0.0))

async def main():
    query=["What is weather in Karachi?", "What is weather in Berlin?", "What is weather in Pluto?"]
    for Q in query:
        result = await Runner.run(agent, Q)
        print(f"Question: {Q}")
        print(f"Answer: {result.final_output}")

if __name__ == "__main__":
    asyncio.run(main())

# #Output
# Question: What is weather in Karachi?
# Answer: The current temperature in Karachi is 30.2°C with Patchy light rain with thunder.
# Question: What is weather in Berlin?
# Answer: The current temperature in Berlin is 23.3°C with Sunny.
# Question: What is weather in Pluto?
# Answer: I am sorry, I can only provide the weather for cities on Earth. I cannot provide the weather for Pluto.