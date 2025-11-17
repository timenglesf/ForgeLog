"""
Main CLI entrypoint for your local AI life tracker.

Commands (high-level):

    ai log workout ...
    ai log study ...
    ai log guitar ...
    ai log note ...

    ai today
    ai analyze week
    ai blog week
    ai goals add ...
    ai goals status

For now, everything is just stubbed out with Typer.
You can wire in DB + LLM logic step by step.
"""

from typing import Optional
import typer
from sqlalchemy.orm import Session
import time

from config import TimeRange
import config
import db
from model import Base
from services import events


# Root Typer app
app = typer.Typer(help="Local AI life tracker (workout, study, guitar, journaling).")

# Sub-apps
log_app = typer.Typer(
    help="Log events: workouts, study sessions, guitar practice, notes."
)
analyze_app = typer.Typer(help="Analyze your data over different time ranges.")
blog_app = typer.Typer(help="Generate markdown blog posts from your logs.")
goals_app = typer.Typer(help="Create and inspect goals.")


# Attach sub-apps to main app
app.add_typer(log_app, name="log")
app.add_typer(analyze_app, name="analyze")
app.add_typer(blog_app, name="blog")
app.add_typer(goals_app, name="goals")


# --------------------
# log subcommands
# --------------------


@log_app.command("workout")
def log_workout(
    distance_km: Optional[float] = typer.Option(
        None, "--distance-km", "-d", help="Distance in kilometers."
    ),
    duration_min: Optional[float] = typer.Option(
        None, "--duration-min", "-t", help="Duration in minutes."
    ),
    dips: Optional[int] = typer.Option(
        None, "--dips", help="Number of dips(optional)."
    ),
    pushups: Optional[int] = typer.Option(
        None, "--pushups", help="Number of pushups (optional)."
    ),
    pullups: Optional[int] = typer.Option(
        None, "--pullups", help="Number of pullups (optional)."
    ),
    rows: Optional[int] = typer.Option(
        None, "--rows", help="Number of rows (optional)."
    ),
    squats: Optional[int] = typer.Option(
        None, "--squats", help="Number of squats (optional)."
    ),
    notes: Optional[str] = typer.Option(
        None, "--notes", "-n", help="Optional notes about the workout."
    ),
):
    """
    Log a workout (run, PT, etc.).
    """
    with Session(db.get_engine()) as session:
        event = events.log_workout(
            session,
            dips=dips,
            pushups=pushups,
            pullups=pullups,
            rows=rows,
            squats=squats,
            notes=notes,
        )

        typer.echo(f"Logged Workout Event:\n{event.title} with id {event.id}")

    typer.echo("Logging workout:")
    typer.echo(f"  distance_km={distance_km}")
    typer.echo(f"  duration_min={duration_min}")
    typer.echo(f"  dips={dips}")
    typer.echo(f"  pushups={pushups}")
    typer.echo(f"  pullups={pullups}")
    typer.echo(f"  rows={rows}")
    typer.echo(f"  squats={squats}")
    typer.echo(f"  notes={notes}")


@log_app.command("study")
def log_study(
    minutes: float = typer.Option(
        ..., "--minutes", "-m", help="Study duration in minutes."
    ),
    topic: Optional[str] = typer.Option(
        None, "--topic", "-t", help="Topic or subject studied."
    ),
    notes: Optional[str] = typer.Option(
        None, "--notes", "-n", help="Extra notes about the study session."
    ),
):
    """
    Log a study session.
    """
    typer.echo("Logging study session:")
    typer.echo(f"  minutes={minutes}")
    typer.echo(f"  topic={topic}")
    typer.echo(f"  notes={notes}")


@log_app.command("guitar")
def log_guitar(
    record_session: bool = typer.Option(
        False,
        "--session",
        "-s",
        help="Start a practice session. Records the number of minutes practicing until a key is pressed.",
    ),
    minutes: Optional[float] = typer.Option(
        None, "--minutes", "-m", help="Practice duration in minutes"
    ),
    focus: Optional[config.GuitarFocus] = typer.Option(
        None, "--focus", "-f", help="Focus area: course, scale, song, theory, writing"
    ),
    notes: Optional[str] = typer.Option(
        None, "--notes", "-n", help="Extra notes about practice"
    ),
):
    """
    Log a guitar practice session.
    """
    if record_session:
        typer.echo("🎸 Starting practice session…")
        typer.echo("Press ENTER to end the session.")
        start = time.time()
        input()  # wait for user
        end = time.time()
        minutes = round((end - start) / 60, 2)
        add_note = typer.prompt("Yould you like to add a note? (Y/N)")
        if add_note.lower() == "y":
            notes = typer.prompt("Note")
            typer.echo(f"Notes: {notes}")
        typer.echo(f"⏱ Session length: {minutes} minutes")

    # If user didn't use --session and didn't supply minutes → error
    if minutes is None:
        raise typer.BadParameter("You must provide --minutes or use --session.")
    if focus and focus in config.GuitarFocus:
        with Session(db.get_engine()) as session:
            event = events.log_guitar(
                session=session, name=focus, value=minutes, notes=notes
            )
        typer.echo(f"Logged Guitar Event:\n{event.title} with id {event.id}")

    typer.echo("Logging guitar practice:")
    typer.echo(f"  minutes={minutes}")
    typer.echo(f"  focus={focus}")
    typer.echo(f"  notes={notes}")


# --------------
# today command
# --------------


@app.command("today")
def show_today(
    detailed: bool = typer.Option(
        False,
        "detailed" "-d",
        help="Show full details/notes for each event.",
    )
):
    """
    Show all events logged today.
    """
    # TODO: fetch events from DB for today's date and print them nicely.
    typer.echo(f"Showing today's events (detailed={detailed})")
    typer.echo("TODO: implement DB query and rendering.")


# --------------------
# analyze subcommands
# --------------------


@analyze_app.command("range")
def analyze_range(
    range: TimeRange = typer.Argument(TimeRange.week, help="Time range to analyze."),
):
    """
    Analyze your data for a given time range (today, week, month).
    """
    # TODO: query DB, aggregate metrics, optionally call LLM for summary.
    typer.echo(f"Analyzing range: {range.value}")
    typer.echo("TODO: implement analytics + optional LLM summary.")


# --------------------
# blog subcommands
# --------------------


@blog_app.command("generate")
def blog_generate(
    range: TimeRange = typer.Argument(
        TimeRange.week, help="Time range for the blog post."
    ),
    output: Optional[str] = typer.Option(
        None,
        "--output",
        "-o",
        help="Optional path to write markdown output to a file.",
    ),
):
    """
    Generate a markdown blog post from your logs for a given time range.
    """
    typer.echo(f"Generating blog post for range: {range.value}")
    typer.echo(f"Output file: {output}")
    # TODO:
    # 1. Fetch events for range.
    # 2. Build prompt & call local LLM.
    # 3. Print markdown and/or save to file.


# --------------------
# goals subcommands
# --------------------


@goals_app.command("add")
def goals_add(
    name: str = typer.Argument(..., help="Short name for the goal."),
    metric_name: str = typer.Option(
        ...,
        "--metric",
        "-m",
        help="Metric name (e.g. distance_km, study_minutes, guitar_minutes).",
    ),
    target_value: float = typer.Option(
        ...,
        "--target",
        "-t",
        help="Numeric target for the goal (e.g. 10.0 for 10 km).",
    ),
    period: str = typer.Option(
        "weekly",
        "--period",
        "-p",
        help="Goal period: daily, weekly, or monthly.",
    ),
):
    """
    Add a new goal.
    """
    typer.echo("Adding goal:")
    typer.echo(f"  name={name}")
    typer.echo(f"  metric_name={metric_name}")
    typer.echo(f"  target_value={target_value}")
    typer.echo(f"  period={period}")
    # TODO: insert Goal into DB.


@goals_app.command("status")
def goals_status():
    """
    Show current goals and (eventually) progress for each.
    """
    typer.echo("Showing goal status.")
    # TODO:
    # 1. Fetch goals from DB.
    # 2. Compute progress from EventMetric.
    # 3. Print in a readable table.


# --------------------
# entrypoint
# --------------------


def main():
    Base.metadata.create_all(db.get_engine())
    app()


if __name__ == "__main__":
    main()
