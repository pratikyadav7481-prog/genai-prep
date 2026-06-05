import asyncio
from models import CallSummary
import json
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

    

model = ChatOpenAI(model="gpt-5-nano")
promt = ChatPromptTemplate.from_template("""You are helpful assistant. Always response in this exact JSON format:
                                {{
                                "key_points": ["point 1", "point 2"],
                              "sentiment": "positive/negative/neutral",
                              "action_items": ["action 1", "action 2"]
                              }}
                              Text: {text}""")

chain = promt | model | StrOutputParser()



# response = chain.invoke(text)
# print(response)

async def summarize(text: str):
    response = await chain.ainvoke(text)
    data = json.loads(response)
    return CallSummary(**data)



async def main():
    with open("../my_notes.txt", 'r') as f:
        text = f.read()
    
    response = await summarize(text)

    print("Key Points: ", response.key_points)
    print("Sentiments: ", response.sentiment)
    print("Actions: ", response.action_items)

asyncio.run(main())