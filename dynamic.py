from project import model
from agents import Agent, Runner, RunContextWrapper
from dataclasses import dataclass

@dataclass
class User:
    name: str
    phone: int
    current_conversation: list[str]
    memory: str = ""  # initialize memory to avoid attribute errors

    def get_memory(self):
        return f"User {self.name} has a phone number {self.phone}"

    def update_memory(self, memory: str):
        self.memory = memory

    def update_conversation(self, message: str):
        self.current_conversation.append(message)

@dataclass
class UserContext:
    user: User
    is_admin: bool

def get_system_prompt(ctx: RunContextWrapper, start_agent: Agent[User]):
    print("\nContext: ", ctx.context)
    print("\nAgent: ", start_agent)

    # Update memory and conversation before returning
    ctx.context.update_memory(f"User {ctx.context.name} has a phone number {ctx.context.phone}")
    ctx.context.update_conversation(f"User {ctx.context.name} just started a conversation.")

    return "You are a helpful assistant."

# Create the agent
agent = Agent(
    name="Haiku Agent",
    model=model,
    instructions=get_system_prompt
)

# Create user instance
user_1 = User(
    name="Ali Zaid",
    phone=1234,
    current_conversation=[]
)

# Run the agent
res = Runner.run_sync(agent, "Hi", context=user_1)
print(res.final_output)


print([user_1.get_memory()])
print([user_1.current_conversation])


