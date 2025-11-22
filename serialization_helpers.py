import json
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from typing import Iterable, Optional

from model import Event, EventMetric, Tag
from services import events

# --- serialization helpers ---


def event_metric_to_dict(m: EventMetric) -> dict:
    return {
        "id": m.id,
        "event_id": m.event_id,
        "name": m.name,
        "value": m.value,
        "unit": m.unit,
        "created_at": m.created_at.isoformat() if m.created_at else None,
    }


def tag_to_dict(t: Tag) -> dict:
    return {
        "id": t.id,
        "name": t.name,
        "color": t.color,
        "created_at": t.created_at.isoformat() if t.created_at else None,
    }


def event_to_dict(e: Event) -> dict:
    return {
        "id": e.id,
        "timestamp": e.timestamp.isoformat() if e.timestamp else None,
        "type": e.type.value if hasattr(e.type, "value") else str(e.type),
        "title": e.title,
        "raw_text": e.raw_text,
        "notes": e.notes,
        "created_at": e.created_at.isoformat() if e.created_at else None,
        "metrics": [event_metric_to_dict(m) for m in e.metrics],
        "tags": [tag_to_dict(et.tag) for et in e.event_tags if et.tag],
    }


# --- GENERAL formatter ---


def format_events_as_json(
    events: Iterable[Event],
    *,
    label: Optional[str] = None,
) -> str:
    """
    Format an iterable of Event objects (with relationships loaded)
    into a JSON string that is easy for LLMs to consume.
    """
    events_list = list(events)

    payload = {
        "schema_version": 1,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "label": label,  # e.g. "today", "this_week", "custom_range"
        "event_count": len(events_list),
        "events": [event_to_dict(e) for e in events_list],
    }

    return json.dumps(payload, indent=2, ensure_ascii=False)


def format_events_today_as_json(session: Session) -> str:
    today_events = events.select_events_today(session)
    return format_events_as_json(today_events, label="today")


def format_events_week_as_json(session: Session) -> str:
    today_events = events.select_events_week(session)
    return format_events_as_json(today_events, label="today")


# def format_events_today_as_json(session: Session) -> str:
#     """
#     Returns a JSON string with a simple, LLM-friendly schema:
#     {
#       "schema_version": 1,
#       "generated_at": "...",
#       "events": [ {event1...}, {event2...}, ... ]
#     }
#     """
#     today_events = events.select_events_today(session)
#     payload = {
#         "schema_version": 1,
#         "generated_at": datetime.now(timezone.utc).isoformat(),
#         "events": [event_to_dict(e) for e in today_events],
#     }
#     return json.dumps(payload, indent=2, ensure_ascii=False)
