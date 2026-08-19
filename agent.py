import json
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

PRICES = {"shoes": 799, "hat": 399, "bag": 1420, "shorts": 1299, "pants": 1699}


def get_price(item):
    print(f"🔧 tool called: get_price({item})")
    
    # Handle singular/plural variations (e.g., "shoe" vs "shoes")
    item_clean = item.lower().strip()
    if item_clean not in PRICES and item_clean.endswith('s'):
        item_clean = item_clean[:-1]
    elif item_clean not in PRICES and not item_clean.endswith('s'):
        item_clean = item_clean + 's'

    if item_clean in PRICES:
        return f"₹{PRICES[item_clean]}"
    
    # Return a clear message so the model knows it's out of stock / not sold
    return f"Sorry, '{item}' is not available in our shop inventory."


tools = [{
    "type": "function",
    "function": {
        "name": "get_price",
        "description": "Get the price of a shop item from the inventory database.",
        "parameters": {
            "type": "object",
            "properties": {"item": {"type": "string", "description": "the item name"}},
            "required": ["item"],
        },
    },
}]


def agent(user_message):
    # Added System Prompt to keep the model on-track when items are missing
    messages = [
        {
            "role": "system", 
            "content": (
                "You are a shop assistant. Use the `get_price` tool to look up prices. "
                "If the tool returns that an item is not available or not found, explicitly "
                "inform the user that the item is out of stock or not sold in the shop."
            )
        },
        {"role": "user", "content": user_message}
    ]
    
    max_turns = 5
    turn_count = 0

    while turn_count < max_turns:
        response = client.chat.completions.create(
            model="openai/gpt-oss-120b", 
            messages=messages, 
            tools=tools, 
            tool_choice="auto"
        )
        msg = response.choices[0].message

        # Exit loop when the model gives a final answer
        if not msg.tool_calls:
            return msg.content

        messages.append(msg)

        for call in msg.tool_calls:
            args = json.loads(call.function.arguments)
            result = get_price(args.get("item", ""))
            
            messages.append({
                "role": "tool",
                "tool_call_id": call.id,
                "content": str(result),
            })

        turn_count += 1

    return "Agent reached maximum tool-call limit."


if __name__ == "__main__":
    print(agent("Is laptop available?"))