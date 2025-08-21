# 🧬 Agent Cloning: Create Agent Variants
## 🎯 What is Agent Cloning?
Think of Agent Cloning like copying a recipe and making small changes. You have a base recipe (your original agent), and you can create variations by changing specific ingredients (instructions, settings, tools) while keeping the rest the same.

# 🧒 Simple Analogy: The Recipe Book
Imagine you have a base cake recipe:

Original Recipe: Vanilla cake with basic frosting
Clone 1: Same recipe but with chocolate frosting
Clone 2: Same recipe but with strawberry filling
Clone 3: Same recipe but with different baking temperature

```
from project import model
from agents import Agent, Runner,ModelSettings

base_agent = Agent(name="Base Assistant",model=model,model_settings=ModelSettings(temperature=0.7),
                   instructions="You`re helpful assistant.")

creative_agent=base_agent.clone( model=model,model_settings=ModelSettings(temperature=0.3),)
res= Runner.run_sync(creative_agent, "How`re you?", max_turns=2)
print(res.final_output)

```