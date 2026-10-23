import math

from strands import tool


@tool
def analyze_latency(
    service: str,
    baseline_ms: float,
    current_ms: float,
) -> dict:
    """
    Compare a service's current latency against its healthy baseline.

    Args:
        service: Name of the service being investigated.
        baseline_ms: Normal healthy latency in milliseconds.
        current_ms: Current observed latency in milliseconds.

    Returns:
        Structured latency analysis.
    """

    if not service.strip():
        raise ValueError("service must not be blank")
    if not math.isfinite(baseline_ms) or baseline_ms <= 0:
        raise ValueError("baseline_ms must be finite and greater than zero")
    if not math.isfinite(current_ms) or current_ms < 0:
        raise ValueError("current_ms must be finite and nonnegative")

    ratio = current_ms / baseline_ms
    increase_percent = ((current_ms - baseline_ms) / baseline_ms) * 100
    if not math.isfinite(ratio) or not math.isfinite(increase_percent):
        raise ValueError("latency comparison exceeds the supported numeric range")

    if ratio >= 10:
        severity = "critical"
    elif ratio >= 5:
        severity = "high"
    elif ratio >= 2:
        severity = "medium"
    else:
        severity = "low"

    return {
        "service": service,
        "baseline_ms": baseline_ms,
        "current_ms": current_ms,
        "latency_multiplier": round(ratio, 2),
        "increase_percent": round(increase_percent, 2),
        "severity": severity,
    }
