```For all Model is imported by Project.py
import os
from pydantic import BaseModel
from agents import(
    AsyncOpenAI,
    OpenAIChatCompletionsModel,
    RunConfig,
    set_default_openai_client,
    set_tracing_disabled
)
from dotenv import load_dotenv

load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")


if not gemini_api_key:
  raise ValueError("API key is Missing!")

external_clients = AsyncOpenAI(api_key=gemini_api_key, base_url="https://generativelanguage.googleapis.com/v1beta/openai/")
model =OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=external_clients)
config =RunConfig

set_default_openai_client(external_clients)
set_tracing_disabled(True)
```

```
from agents import Agent, handoff,Runner

billing_agent = Agent(name="Billing agent")
refund_agent = Agent(name="Refund agent")

triage_agent = Agent(name="Triage agent", handoffs=[billing_agent, refund_agent])

async def main():
    res = await Runner.run(triage_agent, "I want to refund my order also give detais about order id:123456 and amount 100",model=model)
    print(res.final_output)
    print("Last Agent: ",res.last_agent.name)

if __name__ == "__main__":
    asyncio.run(main())
    #Handoffs to both agent
```

```
from project import model
import asyncio
from agents import Agent, handoff,Runner,enable_verbose_stdout_logging

enable_verbose_stdout_logging()
refund_agent = Agent(name="Refund agent",model=model)

general_agent = Agent(name="General agent", handoffs=[handoff(agent=refund_agent)]  ,model=model)

async def main():
    res = await Runner.run(general_agent, "I want to refund my order of id:1234467")
    print(res.final_output)
    print("Last Agent: ",res.last_agent.name)

if __name__ == "__main__":
    asyncio.run(main())

#Output:Okay, I'm transferring you to a refund agent who can help you with order ID 1234467. Please wait a moment.
#Last Agent:  Refund agent
#Qury="Hi" the general agent answering 
```
```
Tools:
[
  {
    "type": "function",
    "function": {
      "name": "transfer_to_refund_agent",
      "description": "Handoff to the Refund agent agent to handle the request. ",
      "parameters": {
        "additionalProperties": false,
        "type": "object",
        "properties": {},
        "required": []
      }
    }
  }
]
```

# Name and description overeide:
```
from project import model
import asyncio
from agents import Agent, handoff,Runner,enable_verbose_stdout_logging

enable_verbose_stdout_logging()
refund_agent = Agent(name="Refund agent",model=model)

general_agent = Agent(name="General agent", handoffs=[handoff(agent=refund_agent, tool_name_override="refund_order_agent",
              tool_description_override="Handles the refund request")]  ,model=model)

async def main():
    res = await Runner.run(general_agent, "I want to refund my order also give detais about order id:123456 and amount 100")
    print(res.final_output)
    print("Last Agent: ",res.last_agent.name)

if __name__ == "__main__":
    asyncio.run(main())
```
```
Tools:
[
  {
    "type": "function",
    "function": {
      "name": "refund_order_agent",  
      "description": "Handles the refund request",
      "parameters": {
        "additionalProperties": false,
        "type": "object",
        "properties": {},
        "required": []
      }
    }
  }
]
Stream: False
Tool choice: NOT_GIVEN
Response format: NOT_GIVEN

LLM resp:
{
  "content": "I can refund your order. However, I do not have the ability to access order details such as order ID and amount. I can proceed with the refund without this information. Would you like me to do that?\n",
  "refusal": null,
  "role": "assistant",
  "annotations": null,
  "audio": null,
  "function_call": null,
  "tool_calls": null
}

Resetting current trace
I can refund your order. However, I do not have the ability to access order details such as order ID and amount. I can proceed with the refund without this information. Would you like me to do that?

Last Agent:  General agent
```
# Note: 
The name given to agent represents as f"transfer to {Agent name}" but in override it don`t includes Transfer to.. with name.

# Remove all tools
remove_all_tools() returns a HandoffInputFilter instance that, when applied, clears the tools list in HandoffInput and records the change in the handoff history.
```
from project import model
import asyncio
from agents.extensions import handoff_filters
from agents import Agent, handoff,Runner,enable_verbose_stdout_logging,function_tool

@function_tool
def weather(city:str)->str:
    return f"The weather in {city} is dry hot"

enable_verbose_stdout_logging()
refund_agent = Agent(name="Refund agent",instructions="Answer briefly to the user queries with dummy details about dummy refund refunds.",model=model)

general_agent = Agent(name="General agent", tools=[weather],
              handoffs=[handoff(agent=refund_agent, tool_name_override="refund_order_agent",
              tool_description_override="Handles the refund request",is_enabled=True, input_filter=handoff_filters.remove_all_tools)]  ,model=model)

async def main():
    res = await Runner.run(general_agent, """What is the weather in Karachi also I want to refund my order of T-shirt due to its small unfitable size of 100inches" \
     also give detais about order id:123456 and amount 100""")
    print(res.final_output)
    print("Last Agent: ",res.last_agent.name)

if __name__ == "__main__":
    asyncio.run(main())
```

```
Tracing is disabled. Not creating span <agents.tracing.span_data.FunctionSpanData object at 0x000001B7AAD01900>
Invoking tool weather with input {"city":"Karachi"}
Tool call args: ['Karachi'], kwargs: {}
Tool weather returned The weather in Karachi is dry hot
Tracing is disabled. Not creating span <agents.tracing.span_data.HandoffSpanData object at 0x000001B7AC8BB990>
Filtering inputs for handoff
Tracing is disabled. Not creating span <agents.tracing.span_data.AgentSpanData object at 0x000001B7AAC4E800>
Running agent Refund agent (turn 2)
Tracing is disabled. Not creating span <agents.tracing.span_data.GenerationSpanData object at 0x000001B7AC3E1A90>
[
  {
    "content": "Answer briefly to the user queries with dummy details about dummy refund refunds.",
    "role": "system"
  },
  {
    "role": "user",
    "content": "What is the weather in Karachi also I want to refund my order of T-shirt due to its small unfitable size of 100inches\"      also give detais about order id:123456 and amount 100"    
  }
]
Tools:
[]
Stream: False
Tool choice: NOT_GIVEN
Response format: NOT_GIVEN

LLM resp:
{
  "content": "The weather in Karachi is sunny with a high of 35°C.\n\nRegarding your refund request for order #123456:\n\n*   **Status:** Refund approved.\n*   **Amount:** $100.\n*   **Reason:** Size issue (100 inches).\n*   **Expected Refund Date:** Within 7-10 business days. You will receive an email confirmation once the refund is processed.",
  "refusal": null,
  "role": "assistant",
  "annotations": null,
  "audio": null,
  "function_call": null,
  "tool_calls": null
}

Resetting current trace
The weather in Karachi is sunny with a high of 35°C.

Regarding your refund request for order #123456:

*   **Status:** Refund approved.
*   **Amount:** $100.
*   **Reason:** Size issue (100 inches).
*   **Expected Refund Date:** Within 7-10 business days. You will receive an email confirmation once the refund is processed.
Last Agent:  Refund agent
```

### Note:
The remove all tools function apply of agent which is to handoffn task.


---

## 1️⃣ General Temperature Range (for most LLMs)

| Temperature   | Effect                                                    | Use Case                                 |
| ------------- | --------------------------------------------------------- | ---------------------------------------- |
| **0.0 – 0.3** | Deterministic, almost no randomness                       | Math, programming, data extraction       |
| **0.4 – 0.7** | Balanced between accuracy and creativity                  | General-purpose Q\&A                     |
| **0.8 – 1.0** | Creative, exploratory                                     | Storytelling, brainstorming, copywriting |
| **> 1.0**     | Highly random (only supported in Gemini and a few models) | Extreme brainstorming, unusual outputs   |

---

## 2️⃣ Gemini's Range

* **Min:** `0.0` → same as other LLMs (fully deterministic).
* **Max:** `2.0` → allows **twice the randomness** of OpenAI's 1.0 limit.

  * At `2.0`, the model becomes very "unpredictable" and experimental.
  * Useful for generating diverse or unconventional ideas (but bad for precision tasks).

---

### Example:

| Temperature | Gemini behavior (example: "Derivative of Sinx")                                 |
| ----------- | ------------------------------------------------------------------------------- |
| 0.1         | "cos(x)"                                                                        |
| 0.7         | "cos(x) because that's the derivative of sin(x). Here's a quick explanation…"   |
| 1.5         | "Well… if you think about it, sin(x) relates to wave motion… \[extra creative]" |
| 2.0         | "Imagine sin(x) is a dancer… its derivative is the rhythm!"                     |

---

✅ **Best practice for Gemini:**

* For **math/precision:** `0.0 – 0.2`
* For **general Q\&A:** `0.3 – 0.7`
* For **creative writing/brainstorming:** `0.8 – 1.5`
* For **wild idea generation:** `1.6 – 2.0` (experimental only)

---

```
from project import model
from agents import Agent, Runner,ModelSettings,enable_verbose_stdout_logging

enable_verbose_stdout_logging()
agent_focused=Agent(name="Math Tutor", instructions="You are a precise math tutor.",
                    model=model, model_settings=ModelSettings(temperature=2.0))

agent_creator = Agent(name="Story Teller", instructions="You`re creative storyteller",
                       model=model, model_settings=ModelSettings(temperature=0.0))

triage_agent = Agent(name="Story Teller", instructions="Route to agents according to user query",handoffs=[agent_focused,agent_creator],model=model)

res = Runner.run_sync(triage_agent,"Tell me a story about derivative of Sin(x)")
print(res.final_output)
print(res.last_agent.name)

# Low (0.1-0.3): Math, facts, precise instructions
# Medium (0.4-0.6): General conversation, explanations
# High (0.7-0.9): Creative writing, brainstorming
#Note: For gemini temprature range extends to 2.0
```

```
from project import model
from agents import Agent, Runner,ModelSettings, function_tool,enable_verbose_stdout_logging

enable_verbose_stdout_logging()
@function_tool#(is_enabled=False)
def calculator(a , b):
    return f"The result of calculator output is {a and b}"
@function_tool#(is_enabled=False)
def weather_tool(city:str)->str:
    return f"The weather of the {city} is dry hot"

# Agent can decide when to use tools (default)
agent_none = Agent(name="Smart Assistant",model=model,tools=[calculator, weather_tool],model_settings=ModelSettings(tool_choice="required"))

res = Runner.run_sync(agent_none,"Hi")
print(res.final_output)
```

```
from project import model
from agents import Agent, Runner,ModelSettings,enable_verbose_stdout_logging

enable_verbose_stdout_logging()

creative_writer = Agent(
    name="Creative Writer",model=model,
    instructions="You are a creative storyteller. Write engaging, imaginative stories.",
    model_settings=ModelSettings(
        temperature=0.8,  # Very creative
        max_tokens=300    # Short but creative
    )
)

result = Runner.run_sync(creative_writer, "Write a short story about a robot learning to paint")
print(result.final_output)
```

```
from project import model
from agents import Agent, Runner,ModelSettings,enable_verbose_stdout_logging,function_tool

# enable_verbose_stdout_logging()
@function_tool
def rectangle_area(width:float, length: float)->str:
    """Returns the area of Rectangle"""
    return f"The area of Rectangle is {width*length} square units"

tool_user = Agent(name="Tool user", instructions="You are helpful assistant",model=model, tools=[rectangle_area],
                   model_settings=ModelSettings(tool_choice="required"), reset_tool_choice=False)

result = Runner.run_sync(tool_user, "Write a short story about a robot learning to paint")
print(result.final_output)

#Output: Error ....   raise MaxTurnsExceeded(f"Max turns ({max_turns}) exceeded")
#agents.exceptions.MaxTurnsExceeded: Max turns (10) exceeded
```

```
from project import model
from agents import Agent, Runner,ModelSettings,enable_verbose_stdout_logging,function_tool

# enable_verbose_stdout_logging()
@function_tool
def rectangle_area(width:float, length: float)->str:
    """Returns the area of Rectangle"""
    return f"The area of Rectangle is {width*length} square units"

# Agent that MUST use tools
tool_user = Agent( name="Tool User",instructions="You are a helpful assistant. Always use tools when available.",
    tools=[rectangle_area], model_settings=ModelSettings(tool_choice="required"),model=model)

result = Runner.run_sync(tool_user, "What's the area of length=2m and width=5m rectangle?")
print(result.final_output)
```

```
from project import model
from agents import Agent, Runner,ModelSettings,enable_verbose_stdout_logging,function_tool

# enable_verbose_stdout_logging()
@function_tool
def weather_tool(city: str) -> str:
    return f"The weather in {city} is sunny with 25°C."

# Tool 2: Calculator
@function_tool
def calculator(a: float, b: float) -> str:
    return f"The sum of {a} and {b} is {a + b}."

@function_tool
def translator(text:str, language:str)->str:
    return f"The translation of {text} in {language} is: '{text[::-1]}' (pretend translation)"

parallel_agent = Agent(name="Tool User",instructions="You are a helpful assistant. Always use tools when available.",model=model,
    tools=[weather_tool , translator, calculator], model_settings=ModelSettings(tool_choice="auto", parallel_tool_calls=False))

result = Runner.run_sync(parallel_agent, "What is the calculator output of 3 and 4 , and what is the weather in Jeddah and also tell the translation of I love you in the Arabic")
print(result.final_output)

#text[start:stop:step]  -->  text[::-1] --> Starts from end | Steps backward by -1 | Result: Reversed String
```

# Note: parallel_tool_calls is enabled by default (True). Gemini does not support parallel_tool_calls=False.

```
from project import model
from agents import Agent, Runner,ModelSettings,enable_verbose_stdout_logging

# enable_verbose_stdout_logging()
Focused_agent = Agent(name="Focused_agent", model=model, 
                      model_settings=ModelSettings(top_p=0.3, # least diverse from topic
                                                     frequency_penalty=0.5,#discourages the model from repeating the same tokens frequently by reducing the probability of tokens that have already appeared often.
                                                     presence_penalty=0.3)) #Similar to frequency_penalty, but it penalizes the presence of any token that has already appeared at all — even once.

result = Runner.run_sync(Focused_agent, "Write a novel on evil love")
print(result.final_output)
```

# Local Context
```
from project import model
from dataclasses import dataclass
from agents import Agent,RunContextWrapper, Runner,function_tool,enable_verbose_stdout_logging

enable_verbose_stdout_logging()

@dataclass
class UserInfo:
    name:str
    role:str

@function_tool
def greet_user(ctx:RunContextWrapper[UserInfo],greeting:str)->str:
    return f"{greeting}, {ctx.context.name}, You are a {ctx.context.role}."

agent = Agent(name="Greet Agent",tools=[greet_user], model=model,
               instructions="Greet the user properly with their name and role")

usr_context = UserInfo(name="Ali", role="Developer")

result = Runner.run_sync(agent, "Salam How are U?", context=usr_context)
print(result.final_output) 
```

# Agent/llm Context
```
from project import model
from dataclasses import dataclass
from agents import Agent,RunContextWrapper, Runner,function_tool,enable_verbose_stdout_logging

# enable_verbose_stdout_logging()
@dataclass
class UserInfo:
    name:str
    role:str

@function_tool
def greet_user(ctx:RunContextWrapper[UserInfo],greeting:str)->str:
    return f"{greeting}, {ctx.context.name}, You are a {ctx.context.role}."

usr_context = UserInfo(name="Ali", role="Developer")

agent = Agent[usr_context](name="Greet Agent",tools=[greet_user], model=model,
               instructions="Greet the user properly with their name and role")

result = Runner.run_sync(agent, "Hi? ")
print(result.final_output)
```

```
from project import model
from dataclasses import dataclass
from agents import Agent,RunContextWrapper, Runner,function_tool,enable_verbose_stdout_logging

# enable_verbose_stdout_logging()
@dataclass
class UserInfo:
    name:str
    email:str|None =None

@function_tool
def search(local_ctx:RunContextWrapper[UserInfo], query:str)->str:
    import time
    time.sleep(30) # Stimulates a delay for the search operation.
    return "No results found."

def special_prompt(special_context: RunContextWrapper[UserInfo],agent:Agent[UserInfo])->str:
    # who is user?
    # which agent

    print(f"\n User: {special_context.context},\n Agent: {agent.name}.\n")
    return f"You`re a math expert. User: {special_context.context.name}.Please assist with math-related queries."

math_agent:Agent = Agent(name="Genius", instructions=special_prompt,model=model, tools=[search])
# [{"role": "system", "content": "..."}, {"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}]

user_context=UserInfo(name="Ali",email="ali@g..")

result = Runner.run_sync(math_agent, "Search for the best math tutor in my area",context=user_context)
print(f"\n\n Output: {result.final_output}")
#Output: 
 User: UserInfo(name='Ali', email='ali@g..'),
 Agent: Genius.



 Output: I am sorry, I cannot fulfill this request. The available tools lack the desired functionality.

```

```
class Person:
    name = "Ali"

p = Person()
print(getattr(p, 'name', 'Unknown'))     # → Ali
print(getattr(p, 'age', 18))             # → 18 (since 'age' doesn’t exist)
```

# 2. Context-Aware Instructions
```
from project import model
from dataclasses import dataclass
from agents import Agent,RunContextWrapper, Runner,function_tool,enable_verbose_stdout_logging

def context_aware(context: RunContextWrapper, agent: Agent) -> str:
    # Check how many messages in the conversation
    message_count = len(getattr(context, 'messages', []))
    
    if message_count == 0:
        return "You are a welcoming assistant. Introduce yourself!"
    elif message_count < 3:
        return "You are a helpful assistant. Be encouraging and detailed."
    else:
        return "You are an experienced assistant. Be concise but thorough."

agent = Agent(name="Context Aware Agent", model=model, instructions=context_aware)

res = Runner.run_sync(agent, "Hi How are u?")
print(res.final_output)
```
# 3. Time-Based Instructions
```
from project import model
from agents import Agent,RunContextWrapper, Runner,function_tool,enable_verbose_stdout_logging
import datetime

def time_based(ctx:RunContextWrapper, agent:Agent) ->str:
    current_hour = datetime.datetime.now().hour

    if 6 <= current_hour < 12:
        return f"You are {agent.name}, Good morning! Be energetic and positive"
    elif 12 <= current_hour < 17:# 12 to 4:59
        return f"You`re {agent.name}, Good afternoon! Be focused and product"
    else: # 4:59 +
        return f"You are {agent.name}, Good evening! Be angry and barbarist ready to eat someone."
    
agent = Agent(name="Time Aware Agent", instructions=time_based, model=model)
res=Runner.run_sync(agent, "How are u? my friend")

print(res.final_output)
```

# Stateful Instructions(Remember Interactions)
```
from project import model
from agents import Agent,RunContextWrapper, Runner,function_tool,enable_verbose_stdout_logging

enable_verbose_stdout_logging()
class StatefulInstructions:
    def __init__(self):
        self.interaction_count = 0

    def __call__(self, context:RunContextWrapper, agent:Agent)->str:
        self.interaction_count += 1

        if self.interaction_count ==1:
            return "You are a learning assistant.This is our first interaction. be welcoming!"
        
        elif self.interaction_count <= 3:
            return f"You are a learning assistant. This is interaction #{self.interaction_count}- build on our conversation."

        else:
            return f"You are experienced assistant. We`ve had {self.interaction_count} interactions - be efficient."
        

instruction_gen = StatefulInstructions()
agent = Agent(name="Stateful Agent",instructions=instruction_gen, model=model)
res = Runner.run_sync(agent, "How are u?")
print(res.final_output)
```

# 5. Async Dynamic Instructions
```
from project import model
from agents import Agent,RunContextWrapper, Runner,function_tool,enable_verbose_stdout_logging
import asyncio
import datetime

def explore_agent(ctx:RunContextWrapper, agent:Agent):
    current_time = datetime.datetime.now()
    return f"""You are {agent.name}, an Ai assistant with real-time capabilities.
    Current time: {current_time.strftime('%H:%M:%S')}
    Provide helpful and timely responses."""

agent = Agent(name="Stateful Agent",instructions=explore_agent, model=model)
res = Runner.run_sync(agent, "What is the current time?")
print(res.final_output)

# Output:The current time is 22:09.
```
# .strftime(...)
Stands for string format time. It converts a datetime into a formatted string .

'%H:%M'
%H → Hour (00–23), zero-padded
%M → Minute (00–59), zero-padded
: → Just a literal colon between them

# Agent Parameters
```
from project import model
from agents import Agent,RunContextWrapper, Runner

def explore_context(ctx:RunContextWrapper, agent:Agent):
    #Access converstion messages
    messages = getattr(ctx, "messages", [])
#If ctx.messages exists → messages becomes that list.
#If ctx.messages doesn’t exist → messages becomes an empty list [].
#getattr(obj, "attr", default)
    message_count = len(messages)

    user_name = getattr(ctx.context, 'name', 'User')
    #getattr(ctx.context, from it .name , by default .user)

    return f"You are {agent.name}. Taking to {user_name}. Message #{message_count}.Answer the user briefly by calling with his name and introducing your name"
agent = Agent(name="Stateful Agent",instructions=explore_context , model=model)
res = Runner.run_sync(agent, "Introduce yourself? and who I am ?and also tell how many messages I send to u?")
print(res.final_output)

#Output: Hello there! I'm Stateful Agent, an AI here to assist you. You are User, and this is the first message you've sent me.
```
```
from project import model
from agents import Agent,RunContextWrapper, Runner, function_tool

@function_tool
def add(a,b)->int:
    return f"The sum is {a+b}"

def explore_context(ctx:RunContextWrapper, agent:Agent):
    #Access agent properties.
    agent_name = agent.name
    tool_count = len(agent.tools)

    return f"You are {agent_name}. with {tool_count} tools. Be helpful by telling your name and tool counts briefly"
agent = Agent(name="Stateful Agent", tools=[add], instructions=explore_context , model=model)
res = Runner.run_sync(agent,"Introduce yourself? and who I am ?and also tell how many messages I send to u? how many tools I have")
print(res.final_output)

#Output: Hello, I am Stateful Agent. I don't have information about who you are or how many messages you've sent me, as I have no memory of past interactions. I have 1 tool.
```

# Exercise 1: Simple Dynamic Instructions
```
from project import model
from agents import Agent,RunContextWrapper, Runner, function_tool

def dynamic_instrt(ctx:RunContextWrapper, agent:Agent):
    return f"You`re {agent.name} help user in learning python."

agent = Agent(name="Stateful Agent", instructions=dynamic_instrt , model=model)
res = Runner.run_sync(agent,"What is callable")
print(res.final_output)
```

# Exercise 2: Message Count Aware
```
from project import model
from agents import Agent,RunContextWrapper, Runner, function_tool

def message_counter(ctx:RunContextWrapper, agent:Agent):
    message_ccount = len(getattr(ctx, "messages", []))
    
    if message_ccount ==0:
        return f"You're a helpful assistant. Welcome the user warmly and be curious to solve their queries."
    elif message_counter ==1:
        return f"Be fierce yet benevolent — like someone ready to devour challenges."
    else :
        return f"Say bye to user and force him to finsih conversation."

agent = Agent(name="Message Counter", instructions=message_counter , model=model)
res = Runner.run_sync(agent,"What is Function")
print(res.final_output)

#Output: Hello there! I'm happy to help you understand what "callable" means in programming...
```

### 🎓 Learning Progression
1. Start Simple: Basic dynamic instructions
2. Add Context: Use conversation history
3. Add Time: Time-based adaptations
4. Add State: Remember interactions
5. Go Async: Handle async operations

```
import asyncio
from project import model
from agents import Agent,RunContextWrapper, Runner, function_tool

def main():
    """Learn Dynamic Instructions with simple examles."""
    print("\n🎭 Dynamic Instructions: Make Your Agent Adapt")
    print("=" *50)

    #Example1: Basic Dynamic Instructions
    print("\n 🎭Example1: Basic Dynamic Instructions.")
    print("-"* 40)

    def basic_dynamic(ctx: RunContextWrapper, agent:Agent)->str:
        """Basic dynamic instructions function."""
        return f"You`re {agent.name}. Be helpful and friendly"
    
    agent_basic=Agent(name="Dynamic Agent", instructions=basic_dynamic ,model=model)
    result = Runner.run_sync(agent_basic, "Hi, Who are u?")
    print("Basic Dynamic Agent.")
    print(result.final_output)

    #Example2: Context Aware instructions
    print("\n Example2: Context Aware Instructions")
    print("-"*40)

    def context_aware(ctx:RunContextWrapper, agent:Agent)->str:
        """Context aware instructions based on message count."""
        message_count = len(getattr(ctx, "messages", []))

        if message_count == 0:
            return f"You`re welcoming assistant. Introduce Yourself."
        elif message_count <3:
            return f"You`re a helpful assistant. Be encourage and detailed"
        else:
            return f"You are an experienced assistant. Be concise but thorough."
        
    agent_context = Agent(name="Context Agent", instructions=context_aware, model=model)

    res1 = Runner.run_sync(agent_context, "Tell me about python.")
    res2 = Runner.run_sync(agent_context, "What is python functions.")
    res3 = Runner.run_sync(agent_context, "Now explain decorator in python.")
    print(res1.final_output)
    #print(res2.final_output)
    print(res3.final_output)

    #Example3: Time based instructions
    print("\n🎭 Example 3: Time-Based Instructions")
    print("-" * 40)
    
    import datetime
    def time_based(ctx:RunContextWrapper, agent:Agent)->str:
        """Time based instructions based on current hour."""
        current_hour = datetime.datetime.now().hour

        if 6<= current_hour < 12:
            return f"You are {agent.name}.Good Morning! Be energetic and positive."
        elif 12 <= current_hour <17:
            return f"You are {agent.name}.Good afternoon! Be focused and productive."
        else:
            return f"You are {agent.name}.Good evening! Be exhausted,drained and tired."
        
    agent_time=Agent(name="Time Aware Agent", instructions=time_based,model=model)
    res = Runner.run_sync(agent_time, "How are u? ")

    #Example4: Stateful Instructions
    print("\n🎭 Example 4: Stateful Instructions")
    print("-" * 40)

    class StatefulInstruction:
        """Stateful Instructions that remember interaction count."""
        def __init__(self):
            self.interaction_count = 0

        def __call__(self, ctx:RunContextWrapper, agent:Agent):
            self.interaction_count += 1

            if self.interaction_count == 1:
                return f"You are learning assistant .Good Morning! Be energetic and positive."
            elif self.interaction_count <= 3:
                return f"You are learning assistant.Good afternoon! This is interaction #{self.interaction_count} Be focused and productive."
            else:
                return f"You are learning assistant.Good evening! We've had {self.interaction_count} interactions  Be exhausted,drained and tired."

    instruction_gen = StatefulInstruction()

    agent_stateful = Agent(name="Stateful Agent",instructions=instruction_gen,model=model)
    res1 = Runner.run_sync(agent_stateful, "Tell me about python briefly.")
    res2 = Runner.run_sync(agent_stateful, "What is python functions briefly.")
    res3 = Runner.run_sync(agent_stateful, "Now explain decorator in python briefly.")
    print(res1.final_output)
    print(res2.final_output)
    print(res3.final_output)

    for i in range(3):#Start from 0 and go up to 2 (not including 3).
        resulf = Runner.run_sync(agent_stateful, f"Question {i+1}: Tell me about AI")
        print(resulf.final_output[:10] + "...")
        print()
        #Output
# 🎭 Example 4: Stateful Instructions
# ----------------------------------------
# Good after...
# Okay! Let'...
# Ugh, AI......

 #Example5: Exploring Context and Agent
    print("\n🎭 Example 5: Exploring Context and Agent")
    print("-+" * 40)
    def explore_context_and_agent(ctx:RunContextWrapper,agent:Agent)->str:
        "Explore what`s available in context and agent."
        message_count= len(getattr(ctx, "messages", []))

        agent_name= agent.name
        tool_count = len(agent.tools)

        return f"""You`re {agent.name} with {tool_count} tools.
        This is message #{message_count} in our conversation.
        Be helpful and informative!"""
    
    agent_explorer = Agent(name="Context Explorer", instructions=explore_context_and_agent,model=model)
    resf = Runner.run_sync(agent_explorer, "What can you tell me about yourself?")
    print(resf.final_output)

    print("\n 🎉 You've learned Dynamic Instructions!")
    print("💡 Try changing the functions and see what happens!")

if __name__ == "__main__":
    main()
```

# Streaming
```
import asyncio
from project import model
from agents import Agent, Runner
from openai.types.responses import ResponseTextDeltaEvent

async def main():
    agent=Agent(name="Joker", instructions="You`re a helpful assistant",model=model)

    result=Runner.run_streamed(agent, "Please tell me 5 jokes.")
    async for event in result.stream_events():
        if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
            print(event.data.delta, end="" , flush=True)

asyncio.run(main())
```


