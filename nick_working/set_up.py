import os
import os
from openai import OpenAI

# Function to read the API key from the file
def load_api_key(filepath):
    with open(filepath, 'r') as file:
        # Read the content and strip any whitespace/newline characters
        key = file.readline().strip()
        return key

keypath = 'API_key.txt'

# Load the API key
api_key = load_api_key(keypath)

# Set the API key as an environment variable
if api_key:
    os.environ['OPENAI_API_KEY'] = api_key
    print("API Key Loaded:", os.getenv('OPENAI_API_KEY'))
else:
    print("API Key not found.")


# Load the API key from the environment variable
client = OpenAI()

completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {
            "role": "user",
            "content": "Say Hello."
        }
    ]
)

print(completion.choices[0].message.content)