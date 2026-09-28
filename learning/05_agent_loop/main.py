from ollama import chat
from pydantic import BaseModel,ValidationError
from typing import Literal
import os
from pathlib import Path

class AgentDecision(BaseModel):
    action: Literal["read_file", "list_files", "finish"]
    path: str | None = None
    answer: str | None = None

WORKSPACE = Path.cwd().resolve()

def safe_path(path: str) -> Path:
    candidate = (WORKSPACE / path).resolve()

    if not candidate.is_relative_to(WORKSPACE):
        raise ValueError("Path is outside the workspace")

    return candidate

def read_file(path: str):
    try:
        file_path = safe_path(path)
    except ValueError as e:
        return f"Error: {e}"

    if not file_path.exists():
        return f"Error: path does not exist: {path}"

    if not file_path.is_file():
        return f"Error: path is not a file: {path}"

    with open(file_path, "r") as file:
        return file.read()

def list_files(path: str):
    try:
        directory = safe_path(path)
    except ValueError as e:
        return f"Error: {e}"

    if not directory.exists():
        return f"Error: path does not exist: {path}"

    if not directory.is_dir():
        return f"Error: path is not a directory: {path}"

    return [item.name for item in directory.iterdir()]

messages = []

messages = [
    {
        "role": "system",
        "content": (
            "You are an AI agent operating inside a workspace. "
            "All file paths must be relative to the workspace. "
            "Never use absolute paths. "
            "For example, use 'learning' instead of '/learning'."
        )
    }
]

user_input = input("You: ")

messages.append({
    "role": "user",
    "content": user_input
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
        "content": (
            f"Tool result:\n{result}\n\n"
            "The tool has already been executed. "
            "Use the result to decide your next action. "
            "If the user's request has been completed, choose finish."
        )
    })

else:
    print("Maximum steps reached.")
print("Agent Finished....")