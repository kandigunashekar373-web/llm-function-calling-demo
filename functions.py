import ast
import operator

def schedule_meeting(title, date, time, attendees=None):
    return {
        "status": "mock_meeting_created",
        "title": title,
        "date": date,
        "time": time,
        "attendees": attendees or [],
        "note": "Demo only. No real calendar was changed."
    }

def draft_email(to, subject, message):
    return {
        "status": "draft_created",
        "to": to,
        "subject": subject,
        "message": message,
        "note": "Draft only. No email was sent."
    }

def get_weather(location):
    return {
        "status": "mock_weather",
        "location": location,
        "temperature_f": 72,
        "condition": "Partly cloudy",
        "note": "Demo data only."
    }

OPS = {
    ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul,
    ast.Div: operator.truediv, ast.Pow: operator.pow, ast.Mod: operator.mod,
    ast.USub: operator.neg, ast.UAdd: operator.pos
}

def _eval(node):
    if isinstance(node, ast.Expression):
        return _eval(node.body)
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return float(node.value)
    if isinstance(node, ast.BinOp) and type(node.op) in OPS:
        return OPS[type(node.op)](_eval(node.left), _eval(node.right))
    if isinstance(node, ast.UnaryOp) and type(node.op) in OPS:
        return OPS[type(node.op)](_eval(node.operand))
    raise ValueError("Unsupported expression")

def calculator(expression):
    try:
        result = _eval(ast.parse(expression, mode="eval"))
        return {"status": "completed", "expression": expression, "result": result}
    except Exception as exc:
        return {"status": "error", "expression": expression, "message": str(exc)}

FUNCTIONS = {
    "schedule_meeting": schedule_meeting,
    "draft_email": draft_email,
    "get_weather": get_weather,
    "calculator": calculator
}

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "schedule_meeting",
            "description": "Create a mock meeting after all details are known.",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "date": {"type": "string"},
                    "time": {"type": "string"},
                    "attendees": {"type": "array", "items": {"type": "string"}}
                },
                "required": ["title", "date", "time"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "draft_email",
            "description": "Create an email draft.",
            "parameters": {
                "type": "object",
                "properties": {
                    "to": {"type": "string"},
                    "subject": {"type": "string"},
                    "message": {"type": "string"}
                },
                "required": ["to", "subject", "message"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Return mock weather data.",
            "parameters": {
                "type": "object",
                "properties": {"location": {"type": "string"}},
                "required": ["location"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "Safely calculate a basic arithmetic expression.",
            "parameters": {
                "type": "object",
                "properties": {"expression": {"type": "string"}},
                "required": ["expression"],
                "additionalProperties": False
            }
        }
    }
]
