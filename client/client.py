# client/client.py
import httpx, uuid
from typing import Any, Optional

class A2AClient:
    """Minimal A2A-compliant client."""
    def __init__(self, agent_url: str):
        self.agent_url = agent_url.rstrip('/')
        self._card = None
        self._http = httpx.Client(timeout=30)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        """Close the underlying HTTP client."""
        self._http.close()

    # ── 1. Discovery ─────────────────────────────────────────────────
    def fetch_agent_card(self) -> dict:
        """Fetch and cache the Agent Card."""
        if self._card is None:
            url = f'{self.agent_url}/.well-known/agent.json'
            print(f"[LOG] Fetching Agent Card: GET {url}")
            resp = self._http.get(url)
            resp.raise_for_status()
            self._card = resp.json()
        return self._card

    def get_skills(self) -> list:
        """Returns the skills list from the cached Agent Card."""
        card = self.fetch_agent_card()
        return card.get('skills', [])

    # ── 2. Request Construction ──────────────────────────────────────
    def _build_task(self, text: str, task_id: Optional[str] = None, session_id: Optional[str] = None) -> dict:
        """Build a conformant A2A task payload."""
        return {
            'id': task_id or str(uuid.uuid4()),
            'sessionId': session_id,
            'message': {
                'role': 'user',
                'parts': [{'type': 'text', 'text': text}]
            }
        }

    # ── 3. Send & Parse ──────────────────────────────────────────────
    def send_task(self, text: str, **kwargs) -> dict:
        """Send a task and return the parsed response."""
        self.fetch_agent_card()
        payload = self._build_task(text, **kwargs)
        url = f'{self.agent_url}/tasks/send'
        
        print(f"[LOG] Sending Task: POST {url} | Payload ID: {payload['id']}")
        resp = self._http.post(url, json=payload)
        resp.raise_for_status()
        
        data = resp.json()
        if data.get('status', {}).get('state') != 'completed':
            raise RuntimeError(f"Task failed or incomplete. Status: {data.get('status')}")
            
        return data

    # ── 4. Helper: extract result text ───────────────────────────────
    @staticmethod
    def extract_text(response: dict) -> str:
        """Pull the first text part from artifacts, or url if it's a file."""
        artifacts = response.get('artifacts', [])
        for artifact in artifacts:
            for part in artifact.get('parts', []):
                if part.get('type') == 'text':
                    return part['text']
                elif part.get('type') == 'file':
                    return part.get('url', '')
        return ''