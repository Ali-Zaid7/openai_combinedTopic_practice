# Callable
In Python, Callable is a type hint that means:
"This thing is a function (or anything else you can call with parentheses)."
```
from typing import Callable
Callable[[ArgType1, ArgType2, ...], ReturnType]
```

| Config                                                               | Outcome                                     |
| -------------------------------------------------------------------- | ------------------------------------------- |
| `tool_choice="auto"` + `reset_tool_choice=True` + `StopAtTools(...)` | ✅ Balanced — use tool, then behave normally |
| `tool_choice="required"` + `reset_tool_choice=False`                 | ❌ Risk of infinite loop                     |
| `tool_choice="none"`                                                 | 🚫 No tools allowed                         |
| `parallel_tool_calls=True`                                           | ⚡ Multiple tool calls at once               |



| `tool_choice` | `reset_tool_choice` | `tool_use_behavior`          | 💡 Expected Outcome                                                    |
| ------------- | ------------------- | ---------------------------- | ---------------------------------------------------------------------- |
| `"auto"`      | `False`             | `None`                       | Model **may** call tools, continues with tool use freely               |
| `"auto"`      | `True`              | `StopAtTools(["tool_name"])` | Stops after tool is called; later turns behave normally again          |
| `"required"`  | `False`             | `None`                       | Model is **forced** to call tool on every turn — can lead to **loops** |
| `"required"`  | `True`              | `StopAtTools(["tool_name"])` | Tool is called, then `tool_choice` resets to `None`; avoids loops      |
| `"none"`      | `--`                | Any                          | Tools are **disabled** — model must respond without using any tool     |
| `None`        | `--`                | Any                          | Equivalent to `"auto"`                                                 |


# Dynamic Instructions
```
from project import model
from agents import Agent, Runner

def get_system_prompt(ctx, agent):
    print("\nContext: ", ctx)
    print("\nAgent: ", agent)
    return "You are helpful Assistant"

agent = Agent(name="Haiku Agent",model=model,
              instructions=get_system_prompt)

res= Runner.run_sync(agent, "Hi")
print(res.final_output)
```

Context:  RunContextWrapper(context=None, usage=Usage(requests=0, input_tokens=0, input_tokens_details=InputTokensDetails(cached_tokens=0), output_tokens=0, output_tokens_details=OutputTokensDetails(reasoning_tokens=0), total_tokens=0))

Agent:  Agent(name='Haiku Agent', instructions=<function get_system_prompt at 0x000001E3C8338AE0>, prompt=None, handoff_description=None, handoffs=[], model=<agents.models.openai_chatcompletions.OpenAIChatCompletionsModel object at 0x000001E3CDA60530>, model_settings=ModelSettings(temperature=None, top_p=None, frequency_penalty=None, presence_penalty=None, tool_choice=None, parallel_tool_calls=None, truncation=None, max_tokens=None, reasoning=None, metadata=None, store=None, include_usage=None, response_include=None, extra_query=None, extra_body=None, extra_headers=None, extra_args=None), tools=[], mcp_servers=[], mcp_config={}, input_guardrails=[], output_guardrails=[], output_type=None, hooks=None, tool_use_behavior='run_llm_again', reset_tool_choice=True)
Hi there! How can I help you today?


```
def get_system_prompt(agent , ctx):
    print("\nContext: ", ctx)
    print("\nAgent: ", agent)
    return "You are helpful Assistant"

#Output:
# Context:  Agent(name='Haiku Agent', instructions=<function get_system_prompt at 0x0000023B33FE8AE0>, prompt=None, handoff_description=None, handoffs=[], model=<agents.models.openai_chatcompletions.OpenAIChatCompletionsModel object at 0x0000023B39750E60>, model_settings=ModelSettings(temperature=None, top_p=None, frequency_penalty=None, presence_penalty=None, tool_choice=None, parallel_tool_calls=None, truncation=None, max_tokens=None, reasoning=None, metadata=None, store=None, include_usage=None, response_include=None, extra_query=None, extra_body=None, extra_headers=None, extra_args=None), tools=[], mcp_servers=[], mcp_config={}, input_guardrails=[], output_guardrails=[], output_type=None, hooks=None, tool_use_behavior='run_llm_again', reset_tool_choice=True)

# Agent:  RunContextWrapper(context=None, usage=Usage(requests=0, input_tokens=0, input_tokens_details=InputTokensDetails(cached_tokens=0), output_tokens=0, output_tokens_details=OutputTokensDetails(reasoning_tokens=0), total_tokens=0))
# Hi there! How can I help you today?
```


```
def get_system_prompt(ctx:RunContextWrapper, agent:Agent):
    print("\nContext: ", ctx.context)
    print("\nAgent: ", agent)
    return "You are helpful Assistant"

#Output
# Context:  None

# Agent:  Agent(name='Haiku Agent', instructions=<function get_system_prompt at 0x000001C1CB458AE0>, prompt=None, handoff_description=None, handoffs=[], model=<agents.models.openai_chatcompletions.OpenAIChatCompletionsModel object at 0x000001C1D0B6B1D0>, model_settings=ModelSettings(temperature=None, top_p=None, frequency_penalty=None, presence_penalty=None, tool_choice=None, parallel_tool_calls=None, truncation=None, max_tokens=None, reasoning=None, metadata=None, store=None, include_usage=None, response_include=None, extra_query=None, extra_body=None, extra_headers=None, extra_args=None), tools=[], mcp_servers=[], mcp_config={}, input_guardrails=[], output_guardrails=[], output_type=None, hooks=None, tool_use_behavior='run_llm_again', reset_tool_choice=True)
# Hi there! How can I help you today?
```

# Error!
```
from agents import Agent, Runner, RunContextWrapper

def get_system_prompt(agent:Agent , ctx:RunContextWrapper):
    print("\nContext: ", ctx.context)
    print("\nAgent: ", agent)
    return "You are helpful Assistant"

    Output:
    
Traceback (most recent call last):
  File "C:\Users\TEAM LAPTOPS\Desktop\cls\dynamic.py", line 12, in <module>
    res= Runner.run_sync(agent, "Hi")
         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\TEAM LAPTOPS\.venv\Lib\site-packages\agents\run.py", line 252, in run_sync
    return runner.run_sync(
           ^^^^^^^^^^^^^^^^
  File "C:\Users\TEAM LAPTOPS\.venv\Lib\site-packages\agents\run.py", line 491, in run_sync
    return asyncio.get_event_loop().run_until_complete(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\TEAM LAPTOPS\AppData\Roaming\uv\python\cpython-3.12.9-windows-x86_64-none\Lib\asyncio\base_events.py", line 691, in run_until_complete
    return future.result()
           ^^^^^^^^^^^^^^^
  File "C:\Users\TEAM LAPTOPS\.venv\Lib\site-packages\agents\run.py", line 397, in run
    input_guardrail_results, turn_result = await asyncio.gather(
                                           ^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\TEAM LAPTOPS\.venv\Lib\site-packages\agents\run.py", line 900, in _run_single_turn
    system_prompt, prompt_config = await asyncio.gather(
                                   ^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\TEAM LAPTOPS\.venv\Lib\site-packages\agents\agent.py", line 247, in get_system_prompt
    return cast(str, self.instructions(run_context, self))
                     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\TEAM LAPTOPS\Desktop\cls\dynamic.py", line 5, in get_system_prompt 
    print("\nContext: ", ctx.context)
                         ^^^^^^^^^^^
AttributeError: 'Agent' object has no attribute 'context'
```

# Instruction parameter 
```
    instructions: (
        str
        | Callable[
            [RunContextWrapper[TContext], Agent[TContext]],
            MaybeAwaitable[str],
        ]
        | None
    ) = None
```

# What is MaybeAwaitable refers to
Allows both
```
def get_system_prompt(ctx:RunContextWrapper, agent:Agent):
    print("\nContext: ", ctx.context)
    print("\nAgent: ", agent)
    return "You are helpful Assistant"

```
or
```
async def get_system_prompt(ctx:RunContextWrapper, agent:Agent):
    print("\nContext: ", ctx.context)
    print("\nAgent: ", agent)
    return "You are helpful Assistant"

```

# 🔹 How ctx and agent are passed to get_system_prompt?
Because you passed a function to instructions=..., the Agents SDK will:

Automatically call your function at runtime to generate the system prompt.

It passes:

ctx: the current RunContextWrapper, so your function can access or modify context data.

agent: the current Agent instance, in case you need its tools, settings, or name.

# In python everything is object:
```
#Same code upper
res= Runner.run_sync(agent, "Hi", context="Ali Zaid")
print(res.final_output)

resp= Runner.run_sync(agent, "Hi", context=["Ali Zaid",'Mahad',"etc"])
print(resp.final_output)

# Context:  Ali Zaid

# Agent:  Agent(name='Haiku Agent', instructions=<function get_system_prompt at 0x000001AFA24A8AE0>, prompt=None,
#  handoff_description=None, handoffs=[], model=<agents.models.openai_chatcompletions.OpenAIChatCompletionsModel object at
#  0x000001AFA7C10C20>, model_settings=ModelSettings(temperature=None, top_p=None, frequency_penalty=None, presence_penalty=None,
#  tool_choice=None, parallel_tool_calls=None, truncation=None, max_tokens=None, reasoning=None, metadata=None, store=None, 
# include_usage=None, response_include=None, extra_query=None, extra_body=None, extra_headers=None, extra_args=None), tools=[],
#  mcp_servers=[], mcp_config={}, input_guardrails=[], output_guardrails=[], output_type=None, hooks=None, 
# tool_use_behavior='run_llm_again', reset_tool_choice=True)
# Hi there! How can I help you today?

#Context:  ['Ali Zaid', 'Mahad', 'etc']
#...
```

In Python, everything is an object, so yes, you can pass plain values like strings or lists as context. But in the Agents SDK, to use context effectively (especially with RunContextWrapper), the best practice is:

✅ Use a @dataclass, regular class,TypeClass or a Pydantic model for context.
Why?
Because:

It gives your tools and instructions a structured schema to work with.

The SDK can track, update, or inject fields more reliably.

It ensures type safety and code clarity when accessing things like ctx.context.name.


# Tools Properties
```By default
from project import model
from agents import Agent, Runner, enable_verbose_stdout_logging,function_tool
from dataclasses import dataclass

enable_verbose_stdout_logging()
@function_tool(is_enabled=True)
def get_weather(city:str)->str:
    return f"The weather in {city} is Suuny"

# Create the agent
agent = Agent(
    name="Haiku Agent",tools=[get_weather],
    model=model,
    instructions="Help Users"
)

res = Runner.run_sync(agent, "What is the weather in Berlin")
print(res.final_output)#Output:The weather in Berlin is Sunny.
```
#🔒 is_enabled=False means:
It hides the tool from the LLM — even if it wants to call it, it can’t.
```
@function_tool(is_enabled=True)
def get_weather(city:str)->str:
    return f"The weather in {city} i...

    #Output:  **Current weather:** Since I don't have real-time access, I can't tell you...
```

# vs tool_choice="none"
```
agent = Agent(
    name="Haiku Agent",tools=[get_weather],
    model=model,model_settings=ModelSettings(tool_choice="none"),
    instructions="Help Users")
#LLM knows tool is present but hasnt permission but In is_enabled=False it cant see tools
```

---

## 🎯 What is `@function_tool`?

It turns a normal Python function into a **tool** that your agent can call.

```python
from agents import function_tool

@function_tool
def get_weather(city: str) -> str:
    return f"The weather in {city} is sunny."
```

After this, `get_weather` is a callable **tool** your agent can use.

---

## 📘 Full Signature

```python
def function_tool(
    *,
    name_override: str | None = None,
    description_override: str | None = None,
    docstring_style: DocstringStyle | None = None,
    use_docstring_info: bool = True,
    failure_error_function: ToolErrorFunction | None = None,
    strict_mode: bool = True,
    is_enabled: bool | Callable = True,
) -> Callable
```

Let’s go through each parameter **with a simple chat-style learning tone**.

---

## 🔍 Parameters Explained

---

### 1️⃣ `name_override`

> 🔤 Give a **custom name** to the tool.

```python
@function_tool(name_override="fetch_weather_info")
def get_weather(city: str) -> str:
    return f"The weather in {city} is sunny."
```

✅ Now the LLM sees this tool as `fetch_weather_info`, not `get_weather`.

---

### 2️⃣ `description_override`

> 📝 Use your own **description** instead of relying on the function’s docstring.

```python
@function_tool(description_override="Gets the current weather of a city")
def get_weather(city: str) -> str:
    ...
```

✅ Useful when the function’s name or docstring isn’t enough.

---

### 3️⃣ `docstring_style`

> 🧪 Choose how the docstring should be **parsed**.

* Options: `"reST"`, `"google"`, `"numpy"`
* Usually used for complex tools with detailed docs.

✅ Skip this unless you're writing very structured docstrings.

---

### 4️⃣ `use_docstring_info=True`

> 📚 If True, the LLM gets info from the function’s docstring to understand:

* What it does
* What the inputs/outputs are

```python
@function_tool
def get_weather(city: str) -> str:
    """Returns weather for a city."""
    return ...
```

✅ This is **True by default** and helps LLM understand the tool better.

---

### 5️⃣ `failure_error_function`

> 🔁 A **custom error handler** when the tool fails (e.g., crashes).

```python
def on_tool_error(ctx, agent, error):
    return "Sorry, something went wrong."

@function_tool(failure_error_function=on_tool_error)
def get_weather(city: str) -> str:
    raise RuntimeError("Oops")
```

✅ The LLM will get the custom message instead of a raw Python error.

---

### 6️⃣ `strict_mode=True`

> 🔒 If True, the input must match the expected types exactly.

* If `False`, LLM can send more flexible (but potentially unsafe) inputs.

```python
@function_tool(strict_mode=False)
def get_weather(city: str) -> str:
    ...
```

✅ This makes the tool more forgiving but possibly risky. Use carefully.

---

### 7️⃣ `is_enabled=True` (🔥 Your Main Question)

> 🚦 Controls whether the tool is available to the LLM.

✅ Options:

* `True`: Tool is always usable.
* `False`: Tool is **disabled** — LLM can’t use it.
* `Callable`: Dynamically decide based on context.

---

#### 🧪 Example 1: Disable a tool

```python
@function_tool(is_enabled=False)
def get_secret_data():
    return "Top secret stuff"
```

✅ The agent **cannot use this tool**.

---

#### 🧪 Example 2: Enable dynamically

```python
def enable_weather(ctx, agent):
    return "weather" in ctx.latest_input.lower()

@function_tool(is_enabled=enable_weather)
def get_weather(city: str) -> str:
    ...
```

✅ The tool is **enabled only if the user mentions "weather"**.

---

## ✅ Summary Table

| Parameter                | Purpose                                  | Default |
| ------------------------ | ---------------------------------------- | ------- |
| `name_override`          | Rename the tool                          | None    |
| `description_override`   | Custom description                       | None    |
| `docstring_style`        | Docstring format style                   | None    |
| `use_docstring_info`     | Use docstring for tool info              | True    |
| `failure_error_function` | Handle tool errors                       | None    |
| `strict_mode`            | Enforce strict input types               | True    |
| `is_enabled`             | Enable/disable tool (can be dynamic too) | True    |

---

## ✅ Mini Chat Summary

👤 **You**: What does `is_enabled=False` do?
🤖 **Me**: It hides the tool from the LLM — even if it wants to call it, it can’t.
👤 **You**: Can I enable it dynamically?
🤖 **Me**: Yes! Use a function: `is_enabled = lambda ctx, agent: "weather" in ctx.latest_input`
👤 **You**: Cool, how can I rename a tool?
🤖 **Me**: Use `name_override="my_name"`
👤 **You**: And custom error messages?
🤖 **Me**: Use `failure_error_function=my_error_handler`

---
