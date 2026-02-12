import os
from dotenv import load_dotenv
from openai import OpenAI

# Load .env file
load_dotenv()

print("OPENAI_API_KEY present:", bool(os.getenv("OPENAI_API_KEY")))

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://models.inference.ai.azure.com"
)

try:
    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {"role": "user", "content": "Say 'token works' if you can read this."}
        ],
        temperature=0
    )

    print("✅ Token test successful!")
    print("Model response:")
    print(response.choices[0].message.content)

except Exception as e:
    print("❌ Token test failed:")
    print(type(e).__name__, e)