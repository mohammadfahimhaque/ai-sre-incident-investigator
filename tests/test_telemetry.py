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


import pytest


@pytest.mark.parametrize("baseline,current,severity", [
    (100, 0, "low"), (100, 199, "low"), (100, 200, "medium"),
    (100, 500, "high"), (100, 1000, "critical"),
])
def test_severity_boundaries(baseline, current, severity):
    assert analyze_latency("checkout", baseline, current)["severity"] == severity


@pytest.mark.parametrize("baseline,current", [
    (0, 100), (-1, 100), (float("nan"), 100), (float("inf"), 100),
    (100, -1), (100, float("nan")), (100, float("inf")),
    (1e-300, 1e300),
])
def test_invalid_measurements_are_rejected(baseline, current):
    with pytest.raises(ValueError):
        analyze_latency("checkout", baseline, current)


def test_blank_service_is_rejected():
    with pytest.raises(ValueError, match="service"):
        analyze_latency("  ", 100, 200)
