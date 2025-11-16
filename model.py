from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, Enum, ForeignKey, String, Text, Boolean, Date, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from config import EventTypes


class Base(DeclarativeBase):
    pass


class Event(Base):
    __tablename__ = "event"
    id: Mapped[int] = mapped_column(primary_key=True)
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    type: Mapped[EventTypes] = mapped_column(
        Enum(EventTypes, name="event_type"),
        nullable=False,
    )
    title: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    raw_text: Mapped[Optional[str]] = mapped_column(Text(), nullable=True)
    notes: Mapped[Optional[str]] = mapped_column(Text(), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    metrics: Mapped[list["EventMetric"]] = relationship(
        back_populates="event", cascade="all, delete-orphan"
    )
    event_tags: Mapped[list["EventTag"]] = relationship(
        back_populates="event",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return (
            f"Event(id={self.id!r}, "
            f"timestamp={self.timestamp!r}, "
            f"type={self.type!r}, "
            f"title={self.title!r})"
        )


class EventMetric(Base):
    __tablename__ = "event_metric"
    id: Mapped[int] = mapped_column(primary_key=True)
    event_id: Mapped[int] = mapped_column(
        ForeignKey("event.id"), nullable=False, index=True
    )
    event: Mapped["Event"] = relationship(back_populates="metrics")

    name: Mapped[str] = mapped_column(String(25), nullable=False)
    value: Mapped[float] = mapped_column(nullable=False)
    unit: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )


class Tag(Base):
    __tablename__ = "tag"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    color: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    # association objects
    event_tags: Mapped[list["EventTag"]] = relationship(
        back_populates="tag",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"Tag(id={self.id!r}, name={self.name!r})"


class EventTag(Base):
    """
    Association between Event and Tag.
    One row = one tag attached to one event.
    """

    __tablename__ = "event_tag"

    event_id: Mapped[int] = mapped_column(
        ForeignKey("event.id"),
        primary_key=True,
    )
    tag_id: Mapped[int] = mapped_column(
        ForeignKey("tag.id"),
        primary_key=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    event: Mapped["Event"] = relationship(back_populates="event_tags")
    tag: Mapped["Tag"] = relationship(back_populates="event_tags")

    def __repr__(self) -> str:
        return f"EventTag(event_id={self.event_id!r}, tag_id={self.tag_id!r})"


class Goal(Base):
    __tablename__ = "goal"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text(), nullable=True)

    # e.g. "distance_km", "study_minutes", "guitar_minutes"
    metric_name: Mapped[str] = mapped_column(String(50), nullable=False)

    # daily / weekly / monthly – stored as text for now
    period: Mapped[str] = mapped_column(String(20), nullable=False)

    # numeric target, interpreted based on metric_name
    target_value: Mapped[float] = mapped_column(nullable=False)

    # Whether we should consider this goal in calculations/feedback
    is_active: Mapped[bool] = mapped_column(
        Boolean(),
        nullable=False,
        server_default="1",
    )

    start_date: Mapped[Optional[datetime]] = mapped_column(Date(), nullable=True)
    end_date: Mapped[Optional[datetime]] = mapped_column(Date(), nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    def __repr__(self) -> str:
        return (
            f"Goal(id={self.id!r}, name={self.name!r}, "
            f"metric_name={self.metric_name!r}, period={self.period!r}, "
            f"target_value={self.target_value!r}, is_active={self.is_active!r})"
        )
