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
