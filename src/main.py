

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage

# ✅ LOAD ENV FIRST
load_dotenv("./.env")

# ✅ THEN import agent
from src.agent.agent import mail_agent, thread_config


def call_agent():
    while True:
        user_input = input("User --> ")

        response = mail_agent.invoke(
            {"messages": [HumanMessage(content=user_input)]},
            config=thread_config# ← LangChain object
        )

        msg=response["messages"][-1]
        tool=response["messages"][-2]
        if tool.type =="tool":
            print(f"tool-->{tool.name}")
        print(f"AI--> {msg.content}")



if __name__ == "__main__":
    call_agent()