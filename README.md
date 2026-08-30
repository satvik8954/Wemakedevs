# Data Watchdog — Two-Gate Approval Agent

An agent built on [TrueForge](https://github.com/truefoundry/trueforge) for the WeMakeDevs Agent Harness Hackathon, combining a SQL analytics check and a GitHub issue filer into one workflow with real branching judgment — not a fixed pipeline.

## What it does

Data Watchdog checks a SQLite database (Chinook music store) for underperforming categories, decides — using a stated threshold rule — whether a finding is actually worth flagging, and only files a GitHub issue when it is. Every sensitive action (running SQL, creating a GitHub issue) pauses for explicit human approval.

**Flow:**
1. Agent proposes a SQL query → **pauses for approval** → runs it
2. Agent analyzes the result against a stated rule (flag if more than 30% below the category average)
3. If it meets the threshold: agent drafts a GitHub issue with the finding as evidence → **pauses for approval** → creates it
4. If it doesn't meet the threshold: agent reports the finding in chat and stops — no second approval, no issue created

This branching is real, not scripted: asking about a low-revenue genre produces a flagged issue; asking about a high-revenue genre produces a "not worth flagging" conclusion with no further action.

## Architecture

- **Model:** Gemini (via OpenRouter)
- **SQL tool:** a custom local MCP server (`sql_server.py`, built with the Python `mcp` SDK) exposing `run_sql` and `list_schema` over a Chinook SQLite database
- **GitHub tool:** TrueForge's built-in GitHub MCP connector, using `issue_write`
- **Approval gates:** configured via the agent manifest's `require_approval_for_tools`, covering both `run_sql` and `issue_write` — enforced by the harness itself, not just prompted

## Setup

1. Run TrueForge locally: `npx @truefoundry/trueforge`
2. Connect a model provider (OpenRouter / Gemini) in Settings → Providers
3. Connect GitHub in Settings → Connectors using a GitHub PAT (`repo` scope)
4. Run the local SQL MCP server: `python3 sql_server.py` (needs `chinook.db` in the same directory)
5. Register it in Settings → Connectors as a custom MCP server pointing to `http://127.0.0.1:8000/mcp`
6. Load the agent manifest (see below) via `PUT /api/v1/agents/<id>`

## Qodo Code Review Evidence

Qodo reviewed [PR #1](https://github.com/satvik8954/Wemakedevs/pull/1) and reported no bugs, rule violations, or requirement gaps.

## Demo

<!-- Add demo video link here -->
https://youtu.be/0yOMzkJwzNY?si=eY-mBEoRbNSZJ0ss
