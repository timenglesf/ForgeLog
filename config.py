from enum import Enum
from datetime import datetime, timezone


# --------------------
# Shared enums / helpers
# --------------------
class EventTypes(Enum):
    ACTIVITY = "activity"
    GUITAR = "guitar"
    HARMONICA = "harmonica"
    NOTE = "note"
    STUDY = "study"
    WORKOUT = "workout"


class TimeRange(int, Enum):
    TODAY = 1
    WEEK = 7
    MONTH = 30
    YEAR = 365


class TimeRangeStr(str, Enum):
    today = "today"
    week = "week"
    month = "month"
    year = "year"


class GuitarFocus(Enum):
    COURSE = "course"
    SCALE = "scale"
    SONG = "song"
    WRITING = "writing"
    THEORY = "theory"


sqlite_engine_uri = "sqlite:///forgelog.sqlite"


def get_date() -> datetime:
    return datetime.now(timezone.utc)
