from __future__ import annotations

from dataclasses import dataclass
from statistics import mean


@dataclass(frozen=True)
class ScrollEvent:
    dwell_seconds: float
    interaction_count: int
    manual_skip: bool = False


@dataclass(frozen=True)
class SessionSummary:
    events: int
    average_dwell_seconds: float
    interaction_rate: float
    fatigue_risk: float
    recommendation: str


def summarize_session(events: list[ScrollEvent]) -> SessionSummary:
    if not events:
        return SessionSummary(0, 0.0, 0.0, 0.0, "NO_SESSION")

    dwell = [max(0.0, event.dwell_seconds) for event in events]
    interactions = [max(0, event.interaction_count) for event in events]
    skips = sum(1 for event in events if event.manual_skip)
    fatigue = round(min(1.0, (skips / len(events)) + _low_dwell_penalty(dwell)), 4)
    interaction_rate = round(sum(interactions) / len(events), 4)
    avg_dwell = round(mean(dwell), 2)

    if fatigue >= 0.7:
        recommendation = "SLOW_DOWN"
    elif interaction_rate >= 1.5 and avg_dwell >= 8:
        recommendation = "CONTINUE"
    else:
        recommendation = "REFINE_FEED"

    return SessionSummary(len(events), avg_dwell, interaction_rate, fatigue, recommendation)


def _low_dwell_penalty(dwell: list[float]) -> float:
    low = sum(1 for value in dwell if value < 3)
    return (low / len(dwell)) * 0.4

