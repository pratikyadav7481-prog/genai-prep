import asyncio
import sys
import httpx


async def summarize(text : str):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
               "Authorization": "Bearer {token}",
                "Content-Type": "application/json"  
            },
            json={
                "model": "gpt-3.5-turbo",
                "messages": [{"role": "system", "content":"You are helpful assistant that summarizes text concisely"},
                             {"role": "user", "content":f"Summarize this: \n\n{text}"} ]
            }
        )
        return response.json()["choices"][0]["message"]["content"]


async def main():
    # filename = sys.argv[1]

    with open("my_notes.txt", 'r') as f:
        text = f.read()

    print("Summarizing....")
    summary = await summarize(text)

    print(f"\nSummary: \n{summary}")

asyncio.run(main())