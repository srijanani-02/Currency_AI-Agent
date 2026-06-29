import os
import json
import requests
import streamlit as st

from dotenv import load_dotenv

from tools import convert_currency
from memory import load_memory, save_memory
from prompts import SYSTEM_PROMPT

load_dotenv()

# Works locally (.env) and on Streamlit Cloud (Secrets)
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY") or st.secrets["OPENROUTER_API_KEY"]

MODEL = "openrouter/auto"

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

# ===========================
# Available Tools
# ===========================

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "convert_currency",
            "description": "Convert an amount from one currency to another.",
            "parameters": {
                "type": "object",
                "properties": {
                    "amount": {
                        "type": "number",
                        "description": "Amount to convert"
                    },
                    "from_currency": {
                        "type": "string",
                        "description": "Source currency code (e.g. USD, INR, EUR)"
                    },
                    "to_currency": {
                        "type": "string",
                        "description": "Target currency code (e.g. INR, USD, JPY)"
                    }
                },
                "required": [
                    "amount",
                    "from_currency",
                    "to_currency"
                ]
            }
        }
    }
]

# ===========================
# Tool Mapping
# ===========================

TOOL_FUNCTIONS = {
    "convert_currency": convert_currency
}


# ===========================
# Call OpenRouter
# ===========================

def call_llm(messages):

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL,
        "messages": messages,
        "tools": TOOLS
    }

    response = requests.post(
        OPENROUTER_URL,
        headers=headers,
        json=payload
    )

    if response.status_code != 200:
        print(response.json())
        raise Exception(response.json())

    return response.json()


# ===========================
# Execute Tool
# ===========================

def run_tool(tool_call):

    tool_name = tool_call["function"]["name"]

    tool_args = json.loads(
        tool_call["function"]["arguments"]
    )

    if tool_name in TOOL_FUNCTIONS:

        result = TOOL_FUNCTIONS[tool_name](**tool_args)

        return str(result)

    return "Tool not found."


# ===========================
# Agent Loop
# ===========================

def agent_loop(user_input):

    memory = load_memory()

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ]

    messages.extend(memory)

    messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    for _ in range(5):

        response = call_llm(messages)

        message = response["choices"][0]["message"]

        messages.append(message)

        if message.get("tool_calls"):

            for tool_call in message["tool_calls"]:

                tool_result = run_tool(tool_call)

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call["id"],
                    "name": tool_call["function"]["name"],
                    "content": tool_result
                })

        else:

            answer = message.get(
                "content",
                "No response."
            )

            save_memory(messages[1:])

            return answer

    return "Maximum steps reached."


# ===========================
# Run from Terminal
# ===========================

if __name__ == "__main__":

    print("💱 Currency Converter Agent Started\n")

    while True:

        user = input("You : ")

        if user.lower() == "exit":
            print("Goodbye!")
            break

        try:

            reply = agent_loop(user)

            print("\nAgent :", reply)
            print()

        except Exception as e:

            print(e)