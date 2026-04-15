# client/demo.py
from client import A2AClient

if __name__ == "__main__":
    with A2AClient("https://echo-a2a-agent-837585057784.us-central1.run.app") as client:
        card = client.fetch_agent_card()
        print(f"Agent Name: {card['name']}")
        print("Skills:", [skill['name'] for skill in client.get_skills()])
        
        response = client.send_task("Hello from the client!")
        result = client.extract_text(response)
        print(f"Echo Response: {result}")
        
        response_sum = client.send_task("!summarise This is a really long text that needs shortening.")
        result_sum = client.extract_text(response_sum)
        print(f"Summarise Response: {result_sum}")