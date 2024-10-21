import os
from openai import OpenAI


keypath = 'API_key.txt'
# Function to read the API key from the file
def load_api_key(filepath):
    with open(filepath, 'r') as file:
        # Read the content and strip any whitespace/newline characters
        key = file.readline().strip()
        return key


# Load the API key
api_key = load_api_key(keypath)

# Set the API key as an environment variable
if api_key:
    os.environ['OPENAI_API_KEY'] = api_key
    print("API Key Loaded:", os.getenv('OPENAI_API_KEY'))
else:
    print("API Key not found.")

#r'C:\Users\NickS\Documents\GitHub\LLMs-top-student\speech-transcription\transcription.txt'
transcription_file = file_path_here
# read in text from trancription
with open(transcription_file, 'r') as file:
    # Read the contents of the file
    transcription = file.read()
# Load the API key from the environment variable
client = OpenAI()

messages=[
        {"role": "system", "content": "You are an attentive tutor with expertise in academic matters. You are given a transcription from a lecture and expected to answer questions from a student."},
        {"role": "user", "content": transcription},
        {"role": "user", "content": "Summarize the most valuable concepts introduced in the transcription (at most 10 words)."}
    ]

completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=messages
)

print(completion.choices[0].message.content)