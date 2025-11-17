from enum import Enum


# --------------------
# Shared enums / helpers
# --------------------
class EventTypes(Enum):
    GUITAR = "guitar"
    HARMONICA = "harmonica"
    NOTE = "note"
    STUDY = "study"
    WORKOUT = "workout"


class TimeRange(str, Enum):
    today = "today"
    week = "week"
    month = "month"


class GuitarFocus(Enum):
    COURSE = "course"
    SCALE = "scale"
    SONG = "song"
    WRITING = "writing"
    THEORY = "theory"


sqlite_engine_uri = "sqlite:///forgelog.sqlite"
