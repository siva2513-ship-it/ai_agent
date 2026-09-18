# AI Agent From Scratch

A hands-on project to learn how AI agents work by building them from the ground up.

## Goal

Learn the fundamentals of AI agents without depending on agent frameworks initially.

By the end of this project, I should be able to design and build different AI agents myself.

## Learning Path

- LLM fundamentals
- Local LLM with Ollama
- Python ↔ LLM communication
- Conversation state
- Structured outputs
- Tools
- Tool calling
- Agent loop
- Memory
- Planning and reasoning
- Error handling
- Git and GitHub integration
- Multi-agent systems
- README Agent
- Resume Agent

## Current Stack

- Python
- Ollama
- Qwen
- Git / GitHub

## Project Structure

```text
learning/
├── 01_llm/
├── 02_conversation/
├── 03_tools/
├── 04_tool_calling/
├── 05_agent_loop/
├── 06_memory/
└── ...

projects/
├── readme-agent/
└── resume-agent/


This is intentionally not a huge README yet. **We'll let our future README agent eventually maintain documentation too.** 😄

---

# 2. `.gitignore`

Use:

```gitignore
# Python
.venv/
__pycache__/
*.py[cod]

# Environment variables
.env
.env.*

# macOS
.DS_Store

# IDEs
.vscode/
.idea/

# Logs
*.log

# Generated files
*.pyc