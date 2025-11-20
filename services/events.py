from datetime import datetime
from sqlalchemy import between, select
from sqlalchemy.orm import Session, selectinload
from typing import List
from config import EventTypes, GuitarFocus, get_date
from model import Event, EventMetric, EventTag


def log_workout(
    session: Session,
    *,
    # distance_mi: float | None,
    # duration_min: float | None,
    dips: int | None,
    planks: int | None,
    pushups: int | None,
    pullups: int | None,
    rows: int | None,
    situps: int | None,
    squats: int | None,
    notes: str | None,
) -> Event:
    title = f"workout {get_date().strftime('%d-%m-%Y')}"
    event = Event(
        type=EventTypes.WORKOUT,
        title=title,
        raw_text=None,
        notes=notes,
    )
    session.add(event)
    session.flush()

    ## create and append metrics
    if dips:
        append_workout_metric(event, "dips", dips, "rep")
    if planks:
        append_workout_metric(event, "planks", planks, "sec")
    if pushups:
        append_workout_metric(event, "pushups", pushups, "rep")
    if pullups:
        append_workout_metric(event, "pullups", pullups, "rep")
    if rows:
        append_workout_metric(event, "rows", rows, "rep")
    if squats:
        append_workout_metric(event, "squats", squats, "rep")
    if situps:
        append_workout_metric(event, "situps", situps, "rep")

    session.commit()
    session.refresh(event)
    return event


def append_workout_metric(event: Event, name: str, value: int, unit: str):
    event.metrics.append(EventMetric(name=name, value=value, unit=unit))


def log_guitar(
    session: Session, name: GuitarFocus, value: float | None, notes: str | None
) -> Event:
    title = f"guitar {get_date().strftime('%d-%m-%Y')}"
    event = Event(
        type=EventTypes.GUITAR,
        title=title,
        raw_text=None,
        notes=notes,
    )
    session.add(event)
    session.flush()

    event.metrics.append(
        EventMetric(name=f"guitar_{name.value}", value=value, unit="min")
    )

    session.commit()
    session.refresh(event)
    return event


def log_activity(
    session: Session,
    name: str,
    value: float | None,
    notes: str | None,
) -> Event:
    title = f"{name} {get_date().strftime('%d-%m-%Y')}"
    event = Event(
        type=EventTypes.ACTIVITY,
        title=title,
        raw_text=None,
        notes=notes,
    )
    session.add(event)
    session.flush()

    event.metrics.append(EventMetric(name=name, value=value))

    session.commit()
    session.refresh(event)
    return event


def select_events_today(session: Session) -> list[Event]:
    today = get_date()
    start = datetime.combine(today, datetime.min.time())
    end = datetime.combine(today, datetime.max.time())
    stmt = (
        select(Event)
        .where(between(Event.timestamp, start, end))
        .options(
            selectinload(Event.metrics),
            selectinload(Event.event_tags).selectinload(EventTag.tag),
        )
        .order_by(Event.timestamp)
    )
    result = session.execute(stmt)
    events = list(result.scalars().all())
    return events
