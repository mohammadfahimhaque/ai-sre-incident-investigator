from unittest.mock import Mock

import pytest

from src.agent import main


def test_missing_model_fails_before_network(monkeypatch):
    monkeypatch.setattr(main, "load_dotenv", lambda: None)
    monkeypatch.delenv("BEDROCK_MODEL_ID", raising=False)
    with pytest.raises(RuntimeError, match="BEDROCK_MODEL_ID"):
        main.create_agent()


@pytest.mark.parametrize("telemetry_enabled", [False, True])
def test_optional_telemetry_tool_is_not_none(monkeypatch, telemetry_enabled):
    monkeypatch.setattr(main, "load_dotenv", lambda: None)
    monkeypatch.setenv("BEDROCK_MODEL_ID", "test-model")
    monkeypatch.setattr(main, "BedrockModel", Mock())
    client = object() if telemetry_enabled else None
    monkeypatch.setattr(main, "create_bronto_mcp_client", lambda: client)
    factory = Mock()
    monkeypatch.setattr(main, "Agent", factory)
    main.create_agent()
    tools = factory.call_args.kwargs["tools"]
    assert tools == [main.analyze_latency] + ([client] if telemetry_enabled else [])
