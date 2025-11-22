from datetime import datetime, timezone, timedelta
from sqlalchemy import select
from typing import List
from sqlalchemy.orm import Session, selectinload

from config import EventTypes, GuitarFocus, TimeRange, get_date
from model import Event, EventMetric, EventTag

###################
##### LOGGING #####
###################


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


#####################
##### SELECTING #####
#####################


def get_range_bounds(
    days: int, tz: timezone = timezone.utc
) -> tuple[datetime, datetime]:
    """
    Return (start, end) such that:
    - end is end of today (23:59:59.999999)
    - start is midnight of (today - (days - 1))
    """
    now = datetime.now(tz)
    end = now.replace(hour=23, minute=59, second=59, microsecond=999999)

    start_date = (end - timedelta(days=days - 1)).date()
    start = datetime(
        year=start_date.year,
        month=start_date.month,
        day=start_date.day,
        tzinfo=tz,
    )

    return start, end


def select_events_between(
    session: Session,
    range: TimeRange,
) -> List[Event]:
    start, end = get_range_bounds(range)
    print(start)
    print(end)
    stmt = (
        select(Event)
        .where(Event.timestamp >= start, Event.timestamp < end)
        .options(
            selectinload(Event.metrics),
            selectinload(Event.event_tags).selectinload(EventTag.tag),
        )
    )
    return list(session.scalars(stmt).all())


def select_events_today(session: Session) -> List[Event]:
    events_today = select_events_between(session, TimeRange.TODAY)
    return events_today


def select_events_week(session: Session) -> List[Event]:
    events_week = select_events_between(session, TimeRange.WEEK)
    print(TimeRange.WEEK.value)
    print(events_week)
    return events_week
