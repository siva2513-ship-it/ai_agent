from ollama import chat
from pydantic import BaseModel
from typing import Literal
import os

class AgentDecision(BaseModel):
    action: Literal["read_file","list_files"]
    path: str | None = None

def read_file(path: str):
    with open(path,'r') as file:
        return file.read()

def list_files():
    return os.listdir(".")

response = chat(
    model = "qwen3.5:4b",
    messages = [
        {
            "role": "user",
            "content" : "List the files in the current directory."
        }
    ],
    format=AgentDecision.model_json_schema()
)

decision = AgentDecision.model_validate_json(response.message.content)

if decision.action == "read_file":
    result = read_file(decision.path)

elif decision.action == "list_files":
    result = list_files()

final_response = chat(
    model="qwen3.5:4b",
    messages=[
        {
            "role":"user",
            "content":"List the files in the current directory."
        },
        {
            "role":"assistant",
            "content": response.message.content
        },
        {
            "role":"user",
            "content" : f"Tool result:\n{result}\nNow respond to the user"
        }
    ]
)

print(final_response.message.content)