import asyncio
from agents import Agent, Runner

billing_agent = Agent(name="Billing_agent")
refund_agent = Agent(name="Refund_agent")

triage_agent = Agent(name="Triage_agent", handoffs=[billing_agent,refund_agent])

async def main():
    res = await Runner.run(triage_agent, """I want to refund my order of id=12345 which is T-shirt""", )

    print(res.final_output)
    print(res.last_agent.name)

if __name__== "__main__":
    asyncio.run(main())



    