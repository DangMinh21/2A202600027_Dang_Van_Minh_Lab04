import os 
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini")

print(llm.invoke("Xin chào, Hôm nay thời tiết Hà Nội thế nào?").content)