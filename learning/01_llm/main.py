from ollama import chat

messages=[]

while True:

    user_input = input("You: ")

    if user_input.lower() == "exit":
        print("Byee Byee Tataaa..")
        break

    messages.append({
        "role": "user",
        "content": user_input
    })

    response = chat(
        model="qwen3.5:4b",
        messages = messages
    )

    assistant_message = response.message.content

    messages.append({
        "role": "assistant",
        "content": assistant_message
    })

    print("Assistant: ",assistant_message)