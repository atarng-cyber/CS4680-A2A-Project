# server/agent_card.py

AGENT_CARD = {
    "id": "echo-agent-v1",
    "name": "Echo Agent",
    "version": "1.0.0",
    "description": "A simple agent that echoes back any text it receives.",
    "url": "https://echo-a2a-agent-837585057784.us-central1.run.app",
    "contact": {
        "email": "andrewtarng01@gmail.com"
    },
    "capabilities": {
        "streaming": False,
        "pushNotifications": False
    },
    "defaultInputModes": ["text/plain"],
    "defaultOutputModes": ["text/plain"],
    "skills": [
        {
            "id": "echo",
            "name": "Echo",
            "description": "Returns the user message verbatim.",
            "inputModes": ["text/plain"],
            "outputModes": ["text/plain"]
        },
        {
            "id": "summarise",
            "name": "Summarise",
            "description": "Returns a brief summary of the input.",
            "inputModes": ["text/plain"],
            "outputModes": ["text/plain"]
        }
    ]
}


def validate_card(card: dict) -> bool:
    """Checks if all required A2A fields are present in the Agent Card."""
    required_keys = [
        "id", "name", "version", "description", "url",
        "capabilities", "skills"
    ]
    for key in required_keys:
        if key not in card:
            return False
    return True
