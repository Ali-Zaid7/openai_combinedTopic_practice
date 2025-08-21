```
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
    query=["What is weather in Karachi?", "What is weather in Antarctica north region?", "What is weather in Jeddah?"]
    for Q in query:
        result = await Runner.run(agent, Q)
        print(f"Question: {Q}")
        print(f"Answer: {result.final_output}")

if __name__ == "__main__":
    asyncio.run(main())

```

### **1. URL construction using f-string**

```python
url = f"http://api.weatherapi.com/v1/current.json?key={weather_api_key}&q={city}&aqi=no"
```
* `{weather_api_key}` → This inserts the value of the variable `weather_api_key` into the URL. This is your API key to access WeatherAPI.
* `{city}` → Inserts the value of the `city` variable, e.g., `"Karachi"`.
* `?key=...&q=...&aqi=no` → These are **query parameters** for the API request:

  * `key` → Your WeatherAPI key.
  * `q` → The city for which you want the weather.
  * `aqi=no` → Disables Air Quality Index in the response.

**Example after formatting:**

```text
http://api.weatherapi.com/v1/current.json?key=123456&q=Karachi&aqi=no
```

---

### **2. Try-except block**

```python
try:
    response = requests.get(url).json()
    temp_c = response["current"]["temp_c"]
    condition = response["current"]["condition"]["text"]
    return f"The current temperature in {city} is {temp_c}°C with {condition}."
except Exception as e:
    return f"Sorry could not fetch weather for {city}.\n\t Error: {e}"
```

#### **a. Try block**

* `requests.get(url)` → Sends an **HTTP GET request** to the API endpoint (`url`).
* `.json()` → Converts the API response from JSON format to a Python dictionary.

**Example JSON response from WeatherAPI:**

```json
{
  "location": { "name": "Karachi", "country": "Pakistan" },
  "current": {
    "temp_c": 35.0,
    "condition": { "text": "Sunny" }
  }
}
```

* `temp_c = response["current"]["temp_c"]` → Extracts the temperature in Celsius from the JSON.
* `condition = response["current"]["condition"]["text"]` → Extracts the weather condition (e.g., Sunny, Rainy).
* `return f"The current temperature in {city} is {temp_c}°C with {condition}."` → Returns a formatted string with the city, temperature, and condition.

**Example output:**

```text
The current temperature in Karachi is 35°C with Sunny.
```

---

#### **b. Except block**

```python
except Exception as e:
    return f"Sorry could not fetch weather for {city}.\n\t Error: {e}"
```

* Catches **any errors** that happen in the `try` block (like network issues, wrong city, or JSON parsing errors).
* `e` → The exception object containing the error message.
* Returns a friendly error message to the user.

**Example output if API fails:**

```text
Sorry could not fetch weather for Karachi.
    Error: HTTPSConnectionPool(host='api.weatherapi.com', port=443): Max retries exceeded
```

---

✅ **Summary:**

* The `url` line builds the API request URL with your API key and city.
* `try` block sends the request, extracts temperature and condition, and returns a readable string.
* `except` block handles any errors gracefully, returning an error message.

---
?key={weather_api_key}&q={city}&aqi=no → query parameters for the API:

key → API key (authenticates you)

q → city name

aqi=no → request option, here "no" air quality info

Resulting string is a fully formed URL that can be passed to requests.get(url) to fetch JSON weather data.