from src.tools.telemetry import analyze_latency


def test_latency_analysis():
    result = analyze_latency(
        service="checkout-api",
        baseline_ms=120,
        current_ms=1800,
    )

    assert result["service"] == "checkout-api"
    assert result["baseline_ms"] == 120
    assert result["current_ms"] == 1800
    assert result["latency_multiplier"] == 15.0
    assert result["increase_percent"] == 1400.0
    assert result["severity"] == "critical"
