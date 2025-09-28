from openai import OpenAI

# create client, it will automatically use the API key from environment
client = OpenAI()

# send a chat message
response = client.chat.completions.create(
    model="gpt-4o-mini",  # cheaper + good for beginners
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello! Tell me a short joke."}
    ]
)

# print the reply
print(response.choices[0].message.content)
