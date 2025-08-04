[Visit Colab link for further executions of cleint and models](https://colab.research.google.com/drive/1TBVPGIRN6Id2ma0fkR-0KoSW6APDXhE9#scrollTo=-KQW4vaOIR0d)

```
from agents import Agent, Runner,enable_verbose_stdout_logging
# set_tracing_disabled(True)
enable_verbose_stdout_logging()

agent=Agent(name="Agent_name", instructions="You are a helpful assistant", model=model)

result = Runner.run_sync(agent , "Write a haiku about beloved")
print(result.final_output)
print(result)#By default gpt-4o
```
#Output
 ```
Tracing is disabled. Not creating trace Agent workflow  
DEBUG:openai.agents:Tracing is disabled. Not creating trace Agent workflow  

Setting current trace: no-op  
DEBUG:openai.agents:Setting current trace: no-op  

Tracing is disabled. Not creating span <agents.tracing.span_data.AgentSpanData object at 0x7cf9d859ef30>  
DEBUG:openai.agents:Tracing is disabled. Not creating span <agents.tracing.span_data.AgentSpanData object at 0x7cf9d859ef30>  

Running agent Agent_name (turn 1)  
DEBUG:openai.agents:Running agent Agent_name (turn 1)  

Tracing is disabled. Not creating span <agents.tracing.span_data.GenerationSpanData object at 0x7cf9d96229f0>  
DEBUG:openai.agents:Tracing is disabled. Not creating span <agents.tracing.span_data.GenerationSpanData object at 0x7cf9d96229f0>  

[
  {
    "content": "You are a helpful assistant",
    "role": "system"
  },
  {
    "role": "user",
    "content": "Write a haiku about beloved"
  }
]
Tools:
[]
Stream: False  
Tool choice: NOT_GIVEN  
Response format: NOT_GIVEN  
DEBUG:openai.agents:[
  {
    "content": "You are a helpful assistant",
    "role": "system"
  },
  {
    "role": "user",
    "content": "Write a haiku about beloved"
  }
]
Tools:
[]
Stream: False  
Tool choice: NOT_GIVEN  
Response format: NOT_GIVEN  

LLM resp:
{
  "content": "Heart beats soft and warm,\nLove's gentle light, a sweet peace,\nSoul finds its true home.\n",
  "refusal": null,
  "role": "assistant",
  "annotations": null,
  "audio": null,
  "function_call": null,
  "tool_calls": null
}
DEBUG:openai.agents:LLM resp:
{
  "content": "Heart beats soft and warm,\nLove's gentle light, a sweet peace,\nSoul finds its true home.\n",
  "refusal": null,
  "role": "assistant",
  "annotations": null,
  "audio": null,
  "function_call": null,
  "tool_calls": null
}

Resetting current trace  
DEBUG:openai.agents:Resetting current trace  

Heart beats soft and warm,  
Love's gentle light, a sweet peace,  
Soul finds its true home.  

RunResult:  
- Last agent: Agent(name="Agent_name", ...)  
- Final output (str):  
    Heart beats soft and warm,  
    Love's gentle light, a sweet peace,  
    Soul finds its true home.  
- 1 new item(s)  
- 1 raw response(s)  
- 0 input guardrail result(s)  
- 0 output guardrail result(s)  
(See `RunResult` for more details)

 ```
 ---

### **1. Tracing is disabled. Not creating trace Agent workflow**  
**Meaning:** Indicates that tracing (logging detailed execution steps for debugging/monitoring) is turned off, so no trace data is being recorded.  
**Use Case:** Useful in production where performance is prioritized over debugging logs.  

### **2. DEBUG:openai.agents:Tracing is disabled. Not creating trace Agent workflow**  
**Meaning:** Debug log confirming tracing is disabled (logged via the `openai.agents` module).  
**Use Case:** Helps developers verify tracing status during debugging.  

---

### **3. Setting current trace: no-op**  
**Meaning:** A "no-op" (no operation) trace is set, meaning no actual tracing occurs.  
**Use Case:** Ensures code runs without performance overhead from tracing in production.  

### **4. DEBUG:openai.agents:Setting current trace: no-op**  
**Meaning:** Debug log confirming the no-op trace setup.  
**Use Case:** Debugging to confirm tracing behavior.  

---

### **5. Tracing is disabled. Not creating span <agents.tracing.span_data.AgentSpanData ...>**  
**Meaning:** A "span" (a unit of work in tracing, like a function call) is skipped due to disabled tracing.  
**Use Case:** Avoids unnecessary overhead when detailed performance monitoring isn’t needed.  

### **6. DEBUG:openai.agents:Tracing is disabled. Not creating span ...**  
**Meaning:** Debug log confirming the span is not created.  
**Use Case:** Debugging to verify tracing behavior.  

---

### **7. Running agent Agent_name (turn 1)**  
**Meaning:** An AI agent (`Agent_name`) starts processing a task (e.g., turn 1 in a conversation).  
**Use Case:** Logging agent activity for auditing or debugging multi-turn interactions (e.g., chatbots).  

### **8. DEBUG:openai.agents:Running agent Agent_name (turn 1)**  
**Meaning:** Debug log confirming the agent’s execution.  
**Use Case:** Tracking agent execution flow during development.  

---

### **9. Tracing is disabled. Not creating span <agents.tracing.span_data.GenerationSpanData ...>**  
**Meaning:** A span for LLM (Large Language Model) text generation is skipped due to disabled tracing.  
**Use Case:** Improves performance when detailed generation logs aren’t needed.  

### **10. DEBUG:openai.agents:Tracing is disabled. Not creating span ...**  
**Meaning:** Debug log confirming the generation span is skipped.  
**Use Case:** Debugging LLM pipeline behavior.  

---

### **11-21. Input prompt (JSON) and parameters**  
```json
[
  {"content": "You are a helpful assistant", "role": "system"},
  {"role": "user", "content": "Write a haiku about beloved"}
]
Tools: []
Stream: False
Tool choice: NOT_GIVEN
Response format: NOT_GIVEN
```  
**Meaning:** The input to the LLM (system message + user request) and configuration (no tools, no streaming).  
**Use Case:**  
- **System message:** Defines the AI’s behavior (e.g., "helpful assistant").  
- **User message:** Task for the AI (e.g., writing a haiku).  
- **Tools:** Optional functions the AI can call (empty here).  
- **Stream: False:** The response is returned at once, not word-by-word.  

---

### **22-32. LLM Response (JSON)**  
```json
{
  "content": "Heart beats soft and warm,\nLove's gentle light, a sweet peace,\nSoul finds its true home.",
  "role": "assistant",
  ...
}
```  
**Meaning:** The AI’s response (a haiku) with metadata (no tool calls, no refusal, etc.).  
**Use Case:**  
- Extracting the generated text (`content`) for user output.  
- Checking `refusal` or `annotations` for moderation/guardrails.  

---

### **33. Resetting current trace**  
**Meaning:** Clears the no-op trace after the agent finishes.  
**Use Case:** Ensures clean state for subsequent operations.  

### **34. DEBUG:openai.agents:Resetting current trace**  
**Meaning:** Debug log confirming trace reset.  
**Use Case:** Debugging trace lifecycle issues.  

---

### **35-37. Haiku Output**  
```
Heart beats soft and warm,
Love's gentle light, a sweet peace,
Soul finds its true home.
```  
**Use Case:** Final output displayed to the user (e.g., in a chatbot).  

---

### **38-45. RunResult Summary**  
```plaintext
RunResult:
- Last agent: Agent(name="Agent_name", ...)
- Final output: [Haiku text]
- 1 new item(s) / 1 raw response(s)
```  
**Meaning:** Summary of the agent’s execution (output, responses, guardrails).  
**Use Case:**  
- Auditing agent performance.  
- Debugging (e.g., checking if guardrails were triggered).  

---

### **Practical Applications**  
1. **Chatbots:**  
   - System messages define behavior ("helpful assistant").  
   - User messages trigger responses (e.g., haiku generation).  
2. **Debugging/Logging:**  
   - `DEBUG` logs help track agent behavior.  
   - Tracing can be enabled in development for performance analysis.  
3. **Guardrails & Moderation:**  
   - Check `refusal` or `annotations` to filter harmful content.  
4. **Multi-Turn Conversations:**  
   - `turn 1` indicates a conversational agent (e.g., for follow-up questions).  

