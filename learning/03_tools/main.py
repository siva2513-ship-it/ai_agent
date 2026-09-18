from pydantic import BaseModel
from typing import Literal
import os

class AgentDecision(BaseModel):
    action: Literal["read_file","list_files"]
    path : str |None = None

def read_file(path: str):
    with open(path,'r') as file:
        return file.read()

def list_files():
    return os.listdir(".")

decision = AgentDecision(
    action = "list_files"
)

if decision.action =="read_file":
    result = read_file(decision.path)

elif decision.action == "list_files":
    result = list_files()

print(result)