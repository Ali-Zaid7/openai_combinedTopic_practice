from project import model
from agents import Agent, Runner, enable_verbose_stdout_logging,RunContextWrapper,function_tool

# Optional: see LLM + tool logs
enable_verbose_stdout_logging()

# Dynamic control: only allow tool for "premium" users
async def is_weather_enabled(ctx: RunContextWrapper, agent: Agent):
    if ctx.context.get("user_type", "basic") == "basic":
        return False
    return True

@function_tool(is_enabled=is_weather_enabled)
def get_weather(city: str) -> str:
    return f"The weather in {city} is sunny"

# Create agent
agent = Agent(name="Haiku Agent",tools=[get_weather],model=model,instructions="Help users based on their subscription tier.")

# 👇 Simulate different user types
for user_type in ["basic", "premium"]:
    print(f"\n🧪 Running as user_type={user_type}")
    result = Runner.run_sync(agent,"What is the weather in Berlin?",context={"user_type": user_type},max_turns=2)
    print("📤 Final output:", result.final_output)
