import openai

class Prompter:
    def __init__(self):
        self.messages = []
        self.client = openai.OpenAI(api_key=openai.api_key)

        # prompt lock. block if processing
        self.prompting = False
        
        # whether 
        self.pending = True

    # content is the last batch of the transcript.
    def append(self, content):
        while self.prompting:
            pass 
        content = "If a highlight worth calling attention is in this, state it in < 10 words. else, strictly say 'N': " + content
        self.messages.append({"role": "user", "content": content})

    def ask(self, content):
        while self.prompting:
            pass 
        self.messages.append({"role":"user", "content": content})

    def prompt(self):
        self.prompting = True
        completion = self.client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=self.messages
        )
        assistant_response = completion.choices[0].message.content
        self.messages.append({"role": "assistant", "content": assistant_response})
        self.prompting = False
        return assistant_response
    