
def create_tool(name, description, **kwargs):
    return {
        "name": name,
        "description": description,
        "parameters": {
            "type": "object",
            "properties": kwargs,
            "required": list(kwargs.keys())
        }
    }