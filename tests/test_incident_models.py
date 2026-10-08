from src.incidents.models import IncidentReport


def test_incident_report_model():
    report = IncidentReport(
        service="checkout-api",
        severity="critical",
        summary="Checkout latency increased significantly.",
        evidence=[
            "Baseline latency: 120 ms",
            "Current latency: 1800 ms",
        ],
        root_cause="Database query regression",
        impact="Checkout requests are significantly slower.",
        recommended_actions=[
            "Inspect slow database queries",
            "Compare query plans against healthy baseline",
        ],
        confidence="high",
    )

    assert report.service == "checkout-api"
    assert report.severity == "critical"
    assert len(report.evidence) == 2
    assert report.confidence == "high"
