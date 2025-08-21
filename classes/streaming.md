### 🔁 What is Streaming?

In **normal (non-streaming) mode**, you call:

```python
res = Runner.run_sync(agent, "What is AI?")
```

And you get back the **full response** after the model finishes generating everything.

But in **streaming mode**, the response is sent to you in **small parts (events)** as the model generates them — almost like **live typing**.

---

### 🧩 What are "Response Events"?

When streaming is enabled, you **subscribe to events** from the runner using `Runner.stream` or `Runner.run` (async).

These events are instances of various classes, for example:

| Event Class           | What It Represents              |
| --------------------- | ------------------------------- |
| `TextBlockStartEvent` | Start of the model's text block |
| `TextBlockDeltaEvent` | New piece (delta) of text       |
| `TextBlockEndEvent`   | Completion of the response      |
| `ToolCallEvent`       | A tool is about to be used      |
| `ToolResultEvent`     | Tool has responded              |
| `RunStepStartEvent`   | A step of the agent has started |
| `RunStepEndEvent`     | A step of the agent has ended   |

These events come **one by one** — like:

```plaintext
TextBlockStartEvent
TextBlockDeltaEvent: "The"
TextBlockDeltaEvent: " weather"
TextBlockDeltaEvent: " in"
TextBlockDeltaEvent: " Lahore"
...
TextBlockEndEvent
```

This allows your UI (like Chainlit or a custom CLI) to **display output live, word-by-word or sentence-by-sentence**, without waiting for the full answer.

---

### 🧪 Sample Streaming Code Snippet

```python
async for event in Runner.run(agent, "Tell me a story", stream=True):
    if isinstance(event, TextBlockDeltaEvent):
        print(event.delta, end="")
```

This would print:

```
Once upon a time in a land far away...
```

**Live** — as the model generates it!

---

### ⚙️ Behind the scenes

* The SDK uses **async generators** or internal event loops to deliver these.
* You can plug them into custom UIs, CLI interfaces, or use them in `Chainlit` for a streaming chat.

---

### 📌 Summary

| Feature            | Non-Streaming                     | Streaming                           |
| ------------------ | --------------------------------- | ----------------------------------- |
| Delivery           | Full response at once             | Piece-by-piece events               |
| Speed              | Waits till full response is ready | Starts showing response immediately |
| Use cases          | Background processing             | Live chats, voice-over generation   |
| Response structure | `RunOutput` object                | Sequence of `Event` objects         |

---

## ✅ Part 1: What is `event` and why do we use `isinstance(event, ...)`

### 🔹 What is `event`?

When you write:

```python
async for event in Runner.run(agent, "your input", stream=True):
```

Each `event` is an **object** (a Python class instance) that represents **something that happened** during the agent's processing.

That "something" could be:

* A tool is called
* A part of the model’s reply is generated
* The model started or ended a block of text
* etc.

---

### 🔹 Why do we use `isinstance(event, TextBlockDeltaEvent)`?

`isinstance()` checks the **type** of object `event` is.

```python
if isinstance(event, TextBlockDeltaEvent):
```

This means:

> “If this event is a small piece of the model's text response, then show it.”

We use it because:

* Not all events are `TextBlockDeltaEvent`
* Some are tool events, or signal start/end of blocks
* You want to **react only to the specific kind** of event you care about

---

Returns True if obj is an instance (object) of the class ClassName (or a subclass of it), else returns False.
```
isinstance(obj, ClassName)
```
---


