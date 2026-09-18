from ollama import chat
from pydantic import BaseModel
from typing import Literal

class AgentDecision(BaseModel):
    action: Literal["read_file", "list_files"]
    path: str | None = None

response = chat(
    model="qwen3.5:4b",
    messages=[
        {
            "role": "user",
            "content": "I want to inspect the file pom.xml. Decide what action should be taken"
        }
    ],
    format=AgentDecision.model_json_schema()
)

decision = AgentDecision.model_validate_json(response.message.content)

print(decision.action, decision.path)