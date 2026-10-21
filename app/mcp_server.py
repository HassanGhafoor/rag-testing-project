import json
from datetime import datetime
from pathlib import Path

import requests
from mcp.server.mcpserver import MCPServer

API = "http://127.0.0.1:8000"
TICKETS_FILE = Path(__file__).resolve().parent.parent / "tickets.jsonl"

mcp = MCPServer("nimbus")


@mcp.tool()
def search_docs(question: str) -> str:
    """Search Nimbus Logistics company documents (HR handbook and IT guides).
    Use this for any question about Nimbus policies, benefits, leave, travel, laptops or VPN.
    Returns the most relevant document sections with their source file."""
    response = requests.post(f"{API}/retrieve", json={"question": question, "k": 3}, timeout=30)
    response.raise_for_status()
    hits = response.json()["hits"]
    return "\n\n---\n\n".join(f"[{h['source']}]\n{h['text']}" for h in hits)


@mcp.tool()
def create_it_ticket(summary: str, details: str) -> str:
    """Create an IT Helpdesk ticket for a Nimbus employee.
    Only use this when the user explicitly asks to raise a ticket,
    or when the documents say to raise one and the user agrees."""
    ticket_id = f"IT-{datetime.now():%Y%m%d%H%M%S}"
    record = {"id": ticket_id, "summary": summary, "details": details}
    with TICKETS_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")
    return f"Ticket {ticket_id} created (mock). Summary: {summary}"


if __name__ == "__main__":
    mcp.run()