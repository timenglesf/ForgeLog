from datetime import datetime
from sqlalchemy.orm import Session
from config import EventTypes, GuitarFocus
from model import Event, EventMetric


def log_workout(
    session: Session,
    *,
    # distance_mi: float | None,
    # duration_min: float | None,
    dips: int | None,
    pushups: int | None,
    pullups: int | None,
    rows: int | None,
    squats: int | None,
    notes: str | None,
) -> Event:
    title = f"workout {datetime.now().strftime('%d-%m-%Y')}"
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
        append_workout_metric(event, "dips", dips, "reps")
    if pushups:
        append_workout_metric(event, "pushups", pushups, "reps")
    if pullups:
        append_workout_metric(event, "pullups", pullups, "reps")
    if rows:
        append_workout_metric(event, "rows", rows, "reps")
    if squats:
        append_workout_metric(event, "squats", squats, "reps")

    session.commit()
    session.refresh(event)
    return event


def append_workout_metric(event: Event, name: str, value: int, unit: str):
    event.metrics.append(EventMetric(name=name, value=value, unit=unit))


def log_guitar(
    session: Session, name: GuitarFocus, value: float | None, notes: str | None
) -> Event:
    title = f"guitar {datetime.now().strftime('%d-%m-%Y')}"
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
