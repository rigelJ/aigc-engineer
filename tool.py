from dotenv import load_dotenv
from openai import OpenAI
from datetime import datetime
import os 
import sys

#load the api key
load_dotenv()
api_key=os.getenv("SILICONFLOW_API_KEY")
base_url=os.getenv("SILICONFLOW_BASE_URL")
                   


#set up the client
client = OpenAI(
    api_key = api_key,
    base_url = base_url
)


#Define the fuction calling 
def get_time():
    return datetime.now().strftime("%H:%M:%S")
#print(get_time())


#Define tools
tools =[
    {
        "type":"function",
        "function":{
            "name":"get_time",
            "description":"Get current time",
            "parameters":{
                "type":"object",
                "properties":{},
                "required":[]
            }
        }
    }
]

#Define AI Role
system_prompt = "You are a smart and helpful AI assisant,answer concisely"
conversation = [{"role":"system","content":system_prompt}]

#Set welcome 
print("Welcome to AI CLI! Type exit to quit.")
print("Type '/rest' to reset conversation context,'exit' to exit ." )

#Start cricle
while True:
    user_input = input("you:").strip()

    #/exit
    if user_input.lower == "exit":
        exit()
    #/reset 
    if user_input.lower == "/reset":
        conversation = [{"role":"system","content":system_prompt}]
        continue

    #create conversation
    conversation.append({"role":"user","content":user_input})
    
    #get response
    response = client.chat.completions.create(
           model = "Qwen/Qwen3-8B",
           messages = conversation,
           tools = tools
    )

    message = response.choices[0].message

    if message.tool_calls:
        tool_call = message.tool_calls[0]

        if tool_call.function.name == "get_time":
            result = get_time()
        
        print("Tool result:",result)
    
    else:
        print(message.content)
        conversation.append({"role":"user","content":message.content})







