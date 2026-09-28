from ollama import chat
from pydantic import BaseModel,ValidationError
from typing import Literal
import os

class AgentDecision(BaseModel):
    action : Literal["read_file","list_files","finish"]
    path : str | None = None

def read_file(path: str):

    if not os.path.exists(path):
        return f"Error: path does not exist: {path}"

    if not os.path.isfile(path):
        return f"Error: path is not a file: {path}"

    with open(path, "r") as file:
        return file.read()

def list_files(path: str):

    if not os.path.exists(path):
        return f"Error: path does not exist: {path}"

    if not os.path.isdir(path):
        return f"Error: path is not a directory: {path}"

    return os.listdir(path)

messages = []

user_input = input("You: ")

messages.append({
    "role":"user",
    "content":user_input
})

MAX_STEPS = 10

for step in range(MAX_STEPS):

    print(f"\n--- Step {step + 1} ---")

    response = chat(
        model="qwen3.5:4b",
        messages=messages,
        format=AgentDecision.model_json_schema()
    )

    content = response.message.content.strip()

    if not content:
        print("Qwen returned an empty response.")
        continue

    try:
        decision = AgentDecision.model_validate_json(content)

    except ValidationError as e:
        print("Qwen returned an invalid decision:")
        print(e)
        continue

    print("Decision:", decision)

    if decision.action == "finish":
        print("Agent Finished....")
        break

    if decision.action == "read_file":

        if decision.path is None:
            print("read_file requires a path.")
            continue

        result = read_file(decision.path)

    elif decision.action == "list_files":

        if decision.path is None:
            print("list_files requires a path.")
            continue

        result = list_files(decision.path)

    messages.append({
        "role": "assistant",
        "content": content
    })

    messages.append({
        "role": "user",
        "content": f"Tool result:\n{result}"
    })

else:
    print("Maximum steps reached.")
print("Agent Finished....")