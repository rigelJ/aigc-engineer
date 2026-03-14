import os
import json
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI
from concurrent.futures import ThreadPoolExecutor


#load the env
load_dotenv()

api_key = os.getenv("SILICONFLOW_API_KEY")
base_url = os.getenv("SILICONFLOW_BASE_URL")

#create openai client
client = OpenAI(
    api_key=api_key,
    base_url=base_url
)

#Set the SystemPrompt
System_prompt = "You are a helpful AI assistant,You can use tools if necessary."
conversation = [{"role":"system","content":System_prompt}]

#--------------------
#  TOOLs
#--------------------

#Set the function
def get_current_time():
    return str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

def multiply(a,b):
    return a*b 

#def get_weather(city):
   # return f"The weather in {city} is sunny"    


#Set the tools
tools = [
    {
        "type":"function",
        "function":{
            "name":"get_current_time",
            "description":"Get current time",
            "parameters": {}
        }
    },
    {
        "type":"function",
        "function": {
            "name":"multiply",
            "description":"Multiply two numbers",
            "parameters":{
                "a": {"type":"number"},
                "b": {"type":"number"}
            }
        }
    }
]

#def a function to handle tool calls 
def call_tool(tool):
    name = tool.function.name
    args = json.loads(tool.function.arguments)

    if name =="get_current_time":
        return get_current_time()
    elif name == "multiply":
        return multiply(args["a"],args["b"])   
    
#def a loop to handle user_input
def handle_input(user_input):

    global conversation

    conversation.append({"role":"user","content":user_input})

    try:
        response = client.chat.completions.create(
            model = "Qwen/Qwen3-8B",
            messages = conversation,
            tools = tools
        )
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        message = "An unexpected error occurred. Please try again later."

    message = response.choices[0].message

    if message.tool_calls:
        
        with ThreadPoolExecutor() as executor:
            
            futures = []
            for tool in message.tool_calls:
                futures.append(executor.submit(call_tool,tool))
            
            results = [future.result() for future in futures]

            for result in results:
                conversation.append({"role":"tool","content":result})
            
            return results

    else:
        result =[]
        result.append(message.content)
        conversation.append({"role":"assistant","content":message.content})
        return result
    


#print the welcome title
print("Welcome to AI CLI! Type exit to quit.")
print("Type '/rest' to reset conversation context , /exit to exit." )

#Recycle start
while True:
    user_input = input("You:").strip()

    #check if exit
    if user_input.lower() == "/exit":
        exit()

    #check if /reset    
    elif user_input.lower() == "/reset":
        conversation = [{"role":"system","content":System_prompt}]
        continue

    results = handle_input(user_input)

    for result in results:
        print(f"Result:{result}")