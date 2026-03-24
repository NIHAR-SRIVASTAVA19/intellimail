import os

from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI

from src.agent.system_prompt import system_prompt
from src.tools.current_date import current_datetime
from src.tools.read_mail import get_inbox, get_mail_body
from src.tools.send_mail import send_mail
from langgraph.checkpoint.memory import InMemorySaver

openai_model=ChatOpenAI(
    base_url="https://api.sarvam.ai/v1/",
    api_key=os.getenv("SARVAM_API_KEY"),
    model="sarvam-105b"
)

checkpointer = InMemorySaver()
thread_config = {"configurable": {"thread_id": "1"}}
mail_agent=create_agent(
    model=openai_model,
    system_prompt=system_prompt,
    tools=[send_mail,current_datetime,get_inbox,get_mail_body],
    checkpointer=checkpointer
)

