# GitHub Issue Assistant — Approval-Gated Agent

An approval-gated AI agent built on [TrueForge](https://github.com/truefoundry/trueforge), submitted for the WeMakeDevs Agent Harness Hackathon (TrueForge track).

## What it does

The agent drafts a GitHub issue (title + body) from a plain-English prompt, shows the draft to the user, and pauses for explicit human approval before actually creating the issue on GitHub. No issue is created without a human clicking approve.

## How the approval gate works

TrueForge's harness enforces the pause at the tool-call level via the agent manifest:

```json
"require_approval_for_tools": ["issue_write"]
```

This means the GitHub `issue_write` tool cannot execute until a human explicitly approves the pending call — it's enforced by the harness, not just requested in the prompt.

## Setup

1. Run TrueForge locally: `npx @truefoundry/trueforge`
2. Connect a model provider (this project uses OpenRouter / Gemini) in Settings → Providers
3. Connect the GitHub connector in Settings → Connectors using a GitHub Personal Access Token (`repo` scope)
4. Load `agent/manifest.json` as the agent's manifest (via the API: `PUT /api/v1/agents/<id>`)
5. Chat with the agent, describe the issue you want, approve the draft when prompted

## Qodo Code Review Evidence

<!-- Add link to the reviewed PR here once merged -->

## Demo

<!-- Add demo video link here -->
