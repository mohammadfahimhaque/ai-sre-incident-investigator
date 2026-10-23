# AI SRE Incident Investigator

A Python command-line prototype for evidence-based incident investigation using
Amazon Bedrock, Strands Agents, and optional Bronto telemetry through MCP.

## What works in this repository

- An interactive investigation loop with a configurable Bedrock model.
- A latency comparison tool with deterministic severity thresholds and input validation.
- Optional Bronto MCP tools when a telemetry API key is configured.
- A Pydantic incident-report schema and offline unit tests.

This is an investigation assistant. It does not repair infrastructure or deploy
changes. MongoDB, GitHub issue publishing, and tracing modules are currently
placeholders and are not registered tools. The report schema is tested separately;
the interactive model output is text and is not automatically validated against it.
No live Bedrock or Bronto success is implied by the unit tests.

## Setup

Use Python 3.12. From a fresh clone:

```bash
python -m venv .venv
source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m pytest -q
```

Unit tests use mocks and synthetic values; they need no cloud credentials or paid
model calls. CI repeats installation, dependency consistency checks, and tests.
The requirements pin direct dependencies; they are not a complete transitive lock.

For an interactive investigation, copy `.env.example` to `.env`, choose a
`BEDROCK_MODEL_ID` available in your AWS region, and configure AWS credentials
through the normal AWS credential chain. Your account needs access to invoke that
model. Model calls can incur charges.

```bash
python -m src.agent.main
```

Enter an incident question; type `exit` or `quit` to stop. Without Bronto configured,
only the latency comparison tool is available, so the assistant cannot verify live
telemetry. To enable telemetry, set `BRONTO_API_KEY` and use the HTTPS
`BRONTO_MCP_URL` shown in `.env.example`. Check connectivity separately:

```bash
python -m scripts.check_bronto_mcp
```

## Example and limits

The synthetic comparison `analyze_latency("checkout-api", 120, 1800)` produces a
15x multiplier, a 1400% increase, and `critical` severity. Thresholds are 2x for
medium, 5x for high, and 10x for critical. These are illustrative rules, not an SLO
or a production alerting policy. A latency increase alone does not establish root
cause. The agent should cite telemetry and identify missing evidence.

Keep credentials in the ignored `.env` or AWS credential store. Never commit real
logs containing secrets or customer information. Review findings before using them
for operational decisions. The current prototype has no production authorization,
incident persistence, automated remediation, or end-to-end cloud validation.
