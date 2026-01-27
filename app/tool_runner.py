from app.tools import (
    tool_get_last_emails,
    tool_send_email
)

TOOL_REGISTRY = {
    "get_last_emails": tool_get_last_emails,
    "send_email": tool_send_email
}

def run_tool(tool_name: str, arguments: dict):
    if tool_name not in TOOL_REGISTRY:
        return {
            "success": False,
            "error": f"Tool '{tool_name}' no registrada"
        }

    try:
        result = TOOL_REGISTRY[tool_name](**arguments)
        return {
            "success": True,
            "tool": tool_name,
            "result": result
        }
    except Exception as e:
        return {
            "success": False,
            "tool": tool_name,
            "error": str(e)
        }