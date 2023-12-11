import requests
import os
from dotenv import load_dotenv

load_dotenv()
CRYPTOPANIC_API_KEY = os.getenv("CRYPTOPANIC_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = "gpt-3.5-turbo"

# Fetch latest feeds from CryptoPanic
url = f"https://cryptopanic.com/api/v1/posts/?auth_token={CRYPTOPANIC_API_KEY}&public=true&filter=hot"
response = requests.get(url)
feeds = response.json()['results']


concatenated_feeds = ""
for i, feed in enumerate(feeds):
    concatenated_feeds += f"{i+1}. {feed['title']} // "

concatenated_feeds = concatenated_feeds[:-3]  # Remove the last "// "

if response.status_code == 200:
    feeds = response.json()['results']
    # Set up OpenAI API request
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {OPENAI_API_KEY}',
    }
    data = {
        'model': OPENAI_MODEL,
        'temperature': 0.7,
        'messages': [
            {
                "role": "user",
                "content": ''
            },
        ]
    }
    data['messages'][0]['content'] = f"Categorize each feed from the following cryptopanic news feeds as \"negative\", \"neutral\" or \"positive\", then return them as csv with columns [number,feed,Category]. Use RFC 4180 spec to handle commas and double quotes. The feeds are the following => '{concatenated_feeds}'"
    response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=data)
    if response.status_code == 200:
        result = response.json()
        sentiment = result['choices'][0]['message']['content'].strip()
        print(sentiment)
    else:
        print(f"Error fetching sentiment analysis: {response.text}")
else:
    print("Error fetching feeds.")