import asyncio
import httpx
import os
import json
from dotenv import load_dotenv
from models import CallSummary

load_dotenv()
token = os.getenv("OPENAI_API_KEY")


async def summarize(text : str):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
               "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"  
            },
            json={
                "model": "gpt-3.5-turbo",
                "messages": [{"role": "system", "content":"""You are helpful assistant. Always response in this exact JSON format:
                                {
                                "key_points": ["point 1", "point 2"],
                              "sentiment": "positive/negative/neutral",
                              "action_items": ["action 1", "action 2"]
                              }
                              """},
                             {"role": "user", "content":f"Summarize this: \n\n{text}"} ]
            }
        )
        raw = response.json()["choices"][0]["message"]["content"]
        data = json.loads(raw)
        return CallSummary(**data)


async def main():
    # filename = sys.argv[1]

    with open("my_notes.txt", 'r') as f:
        text = f.read()

    print("Summarizing....")
    summary = await summarize(text)

    print(f"\Key Points: \n{summary.key_points}")
    print(f"\nSentiment: \n{summary.sentiment}")
    print(f"\nAction Items: \n{summary.action_items}")


asyncio.run(main())