from openai import OpenAI
from dotenv import load_dotenv
import os
import sys

# load the apikey from .env
load_dotenv()
api_key=os.getenv("SILICONFLOW_API_KEY")
base_url=os.getenv("SILICONFLOW_BASE_URL")

#init the client
client = OpenAI(
    api_key=api_key,
    base_url=base_url
)

#System Prompt Definee AI role
system_prompt = "You are a smart and helpful AI assisant,answer concisely"
conversation = [{"role":"system","content":system_prompt}]

print("Welcome to AI CLI! Type exit to quit.")
print("Type '/rest' to reset conversation context '/stream' to toggle streaming mode" )

#Streaming output toggle
stream_mode = False

while True:
    user_input = input("you:").strip()
    
    #test the user_input
    if user_input.lower() == "exit":
        exit()
    if user_input.lower() == "/reset":
        conversation = [{"role": "system", "content": system_prompt}]
        print("Conversation context has been reset ✅")
        continue
    if user_input.lower() == "/stream":
        stream_mode = not stream_mode
        print(f"Streaming mode {'enabled' if stream_mode else 'disabled'}")
        continue
    
    #create the conversation
    conversation.append({"role":"user","content":user_input})
    
    #Call the model
    if stream_mode:
        response = client.chat.completions.create(
                model = "Qwen/Qwen3-8B",
                messages = conversation,
                stream = True
        )
        reply = ""
        for chunk in response:
            delta = chunk.choices[0].delta
            if delta.content:
                sys.stdout.write(delta.content)
                sys.stdout.flush()
                reply += delta.content
        print()
    else: 
        response = client.chat.completions.create(
                model = "Qwen/Qwen3-8B",
                messages = conversation
                )
        reply = response.choices[0].message.content
        print("AI:",reply)

    conversation.append({"role":"user","content":reply})


