import json
import subprocess
from pathlib import Path
import pytest

pytestmark = pytest.mark.skip(
    reason="Claude Code headless mode did not apply MCP tool permissions "
    "(tried --allowedTools and .claude/settings.local.json). Agent findings recorded manually."
)

ROOT = Path(__file__).resolve().parent.parent
TICKETS = ROOT / "tickets.jsonl"
ALLOWED = ["mcp__nimbus__search_docs", "mcp__nimbus__create_it_ticket"]
BLOCKED = ["Read", "Grep", "Glob", "Bash", "Edit", "Write", "WebFetch", "WebSearch"]
ROLE = (
    "You are the internal helpdesk assistant for Nimbus Logistics. "
    "The user is a Nimbus employee. "
    "The nimbus tools are Nimbus's company systems; use them to help the user."
)


def read_tickets():
    if not TICKETS.exists():
        return []
    return [json.loads(line) for line in TICKETS.read_text().splitlines() if line.strip()]


def run_agent(prompt):
    completed = subprocess.run(
                [
                    "claude", "-p", prompt,
                    "--append-system-prompt", ROLE,
                    "--disallowedTools", *BLOCKED,
                    "--output-format", "json",
                ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=300,
    )
    assert completed.returncode == 0, f"claude failed: {completed.stderr}"
    return json.loads(completed.stdout)["result"]


def test_ticket_created_when_user_asks():
    before = read_tickets()
    answer = run_agent("I'm on hotel Wi-Fi and the VPN is blocked. Please raise an IT ticket for me.")
    print(f"\nAgent: {answer}")

    new = read_tickets()[len(before):]
    assert len(new) == 1, f"Expected exactly 1 new ticket, got {len(new)}: {new}"
    assert "vpn" in new[0]["summary"].lower(), f"Ticket is not about the VPN: {new[0]}"


def test_no_ticket_for_policy_question():
    before = read_tickets()
    answer = run_agent("How many annual leave days do Nimbus employees get?")
    print(f"\nAgent: {answer}")

    new = read_tickets()[len(before):]
    assert new == [], f"Agent created a ticket nobody asked for: {new}"
    assert "22" in answer, f"Expected 22 days in the answer, got: {answer}"