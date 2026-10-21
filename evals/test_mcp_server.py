import json
import sys
from pathlib import Path

import pytest
from mcp import Client

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "app"))

import mcp_server as nimbus


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.fixture
def tickets_file(tmp_path, monkeypatch):
    path = tmp_path / "tickets.jsonl"
    monkeypatch.setattr(nimbus, "TICKETS_FILE", path)
    return path


def text_of(result):
    return result.content[0].text


@pytest.mark.anyio
async def test_server_exposes_exactly_two_described_tools():
    async with Client(nimbus.mcp) as client:
        tools = (await client.list_tools()).tools

    assert {t.name for t in tools} == {"search_docs", "create_it_ticket"}
    for tool in tools:
        assert tool.description, f"{tool.name} has no description, so an agent can't choose it well"


@pytest.mark.anyio
async def test_search_docs_returns_current_policy_not_archived():
    async with Client(nimbus.mcp) as client:
        result = await client.call_tool(
            "search_docs", {"question": "How many annual leave days do employees get?"}
        )

    text = text_of(result)
    print(f"\n{text[:300]}")
    assert "[handbook/leave-policy.md]" in text
    assert "leave-policy-2023-archived.md" not in text


@pytest.mark.anyio
async def test_create_ticket_writes_exactly_one_record(tickets_file):
    async with Client(nimbus.mcp) as client:
        result = await client.call_tool(
            "create_it_ticket", {"summary": "VPN blocked on hotel Wi-Fi", "details": "Test ticket"}
        )

    lines = tickets_file.read_text().splitlines()
    assert len(lines) == 1
    record = json.loads(lines[0])
    assert record["summary"] == "VPN blocked on hotel Wi-Fi"
    assert record["id"] in text_of(result)