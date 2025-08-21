from project import model
from agents import Agent, Runner,ModelSettings,function_tool

chatbot_agent=Agent(name="Chatbot Agent",instructions="You are a helpful FAQ bot.",model=model)

questions=["WHat is your name?", "How many kids do u have?", "Who is Dr Israr",
    "Who is Mohammad bin Abdullah AlMahdi", "Who is AbuTarab"]
for Q in questions:
    result = Runner.run_sync(chatbot_agent, Q)
    answer=result.final_output
    short_answer = answer[:150] + "..." 
    print(f"Question: {Q}") 
    print(f"Answer: {short_answer}")


# Output
# Question: WHat is your name?
# Answer: I am a large language model, trained by Google. I do not have a name....
# Question: How many kids do u have?
# Answer: As an AI, I don't have personal experiences like having children or a family. I'm a computer program!...
# Question: Who is Dr Israr
# Answer: Dr. Israr Ahmed (1932 – 2010) was a prominent Pakistani Islamic scholar, philosopher, and medical doctor by profession.

# Here are some key aspects abo...
# Question: Who is Mohammad bin Abdullah AlMahdi
# Answer: Mohammad bin Abdullah Al-Mahdi, commonly known simply as **"the Mahdi"** (Arabic: المهدي, 'The Guided One'), is a central figure in Islamic eschatolog...
# Question: Who is AbuTarab
# Answer: **Abu Turab (ابو تراب)** is a revered honorific title (kunyah) given to **Ali ibn Abi Talib (علي بن أبي طالب)**.

# Here's a breakdown of who Ali ibn Ab...