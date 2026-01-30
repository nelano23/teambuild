import os
import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("MINIMAX_API_KEY")
group_id = os.getenv("MINIMAX_GROUP_ID")

print(f"API Key exists: {bool(api_key)}")
print(f"Group ID exists: {bool(group_id)}")

# Correct endpoint for MiniMax
url = f"https://api.minimax.io/v1/text/chatcompletion_v2?GroupId={group_id}"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

# Try the M2 model
payload = {
    "model": "MiniMax-M2",  # Changed from abab6.5s-chat
    "messages": [
        {"role": "user", "content": "Say hello"}
    ]
}

response = requests.post(url, json=payload, headers=headers)
print(f"\nStatus Code: {response.status_code}")
print(f"Response: {response.text}")