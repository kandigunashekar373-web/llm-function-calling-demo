import json
from collections import defaultdict
from openai import OpenAI

from app.config import OPENAI_API_KEY, OPENAI_MODEL
from app.functions import FUNCTIONS, TOOLS
from app.prompts import SYSTEM_PROMPT

class FunctionCallingAssistant:
    def __init__(self):
        if not OPENAI_API_KEY:
            raise RuntimeError("OPENAI_API_KEY is missing.")
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.sessions = defaultdict(list)

    def chat(self, session_id, user_message):
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            *self.sessions[session_id],
            {"role": "user", "content": user_message}
        ]

        first = self.client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=messages,
            tools=TOOLS,
            tool_choice="auto",
            temperature=0.2
        )

        msg = first.choices[0].message
        tool_events = []

        if msg.tool_calls:
            messages.append(msg.model_dump(exclude_none=True))
            for call in msg.tool_calls:
                name = call.function.name
                args = json.loads(call.function.arguments)
                result = FUNCTIONS[name](**args)
                tool_events.append({"tool": name, "arguments": args, "result": result})
                messages.append({
                    "role": "tool",
                    "tool_call_id": call.id,
                    "content": json.dumps(result)
                })

            final = self.client.chat.completions.create(
                model=OPENAI_MODEL,
                messages=messages,
                temperature=0.2
            )
            text = final.choices[0].message.content or ""
        else:
            text = msg.content or ""

        self.sessions[session_id].extend([
            {"role": "user", "content": user_message},
            {"role": "assistant", "content": text}
        ])

        return {"session_id": session_id, "response": text, "tools_used": tool_events}
