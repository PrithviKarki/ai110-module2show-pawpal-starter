"""PawPal+ core classes.

Skeleton generated from diagrams/uml.mmd. Attributes are wired up in the
constructors; every method body is still a stub for you to implement.
"""

from __future__ import annotations


class Task:
    """One thing that needs to happen for a pet (walk, feeding, meds, ...)."""

    def __init__(
        self,
        task_id: str,
        title: str,
        category: str = "general",
        duration_min: int = 15,
        priority: str = "medium",
        preferred_time: str = "any",
        recurring: bool = True,
        notes: str = "",
    ) -> None:
        self.task_id = task_id
        self.title = title
        self.category = category
        self.duration_min = duration_min
        self.priority = priority
        self.preferred_time = preferred_time
        self.recurring = recurring
        self.completed = False
        self.notes = notes

    def priority_score(self) -> int:
        """Return the priority as a number so tasks can be sorted (high = biggest)."""
        raise NotImplementedError

    def mark_complete(self) -> None:
        """Mark this task as done for the day."""
        raise NotImplementedError

    def reset(self) -> None:
        """Clear the completed flag (e.g. at the start of a new day)."""
        raise NotImplementedError

    def fits_in(self, minutes_left: int) -> bool:
        """Return True if this task can still fit in the remaining time budget."""
        raise NotImplementedError

    def __str__(self) -> str:
        """Return a readable one-line summary of the task."""
        raise NotImplementedError


class ScheduledTask:
    """A Task placed at a specific time in a plan, with the reason it was chosen."""

    def __init__(
        self,
        task: Task,
        start_time: str,
        end_time: str,
        reason: str = "",
    ) -> None:
        self.task = task
        self.start_time = start_time
        self.end_time = end_time
        self.reason = reason


class Pet:
    """A pet and the care tasks it needs."""

    def __init__(
        self,
        name: str,
        species: str,
        breed: str = "",
        age: int = 0,
        weight_kg: float = 0.0,
    ) -> None:
        self.name = name
        self.species = species
        self.breed = breed
        self.age = age
        self.weight_kg = weight_kg
        self.tasks: list[Task] = []

    def add_task(self, task: Task) -> None:
        """Attach a care task to this pet."""
        raise NotImplementedError

    def remove_task(self, task_id: str) -> bool:
        """Remove a task by id. Return True if something was removed."""
        raise NotImplementedError

    def get_tasks(self, only_due: bool = False) -> list[Task]:
        """Return this pet's tasks; if only_due, skip the completed ones."""
        raise NotImplementedError

    def is_senior(self) -> bool:
        """Return True if the pet counts as senior for its species."""
        raise NotImplementedError

    def daily_activity_need(self) -> int:
        """Return the recommended minutes of activity per day for this pet."""
        raise NotImplementedError


class Owner:
    """The person planning care, their pets, and their time constraints."""

    def __init__(
        self,
        name: str,
        email: str = "",
        daily_minutes_available: int = 60,
        preferred_times: list[str] | None = None,
    ) -> None:
        self.name = name
        self.email = email
        self.daily_minutes_available = daily_minutes_available
        self.preferred_times = preferred_times if preferred_times is not None else []
        self.pets: list[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner."""
        raise NotImplementedError

    def remove_pet(self, pet_name: str) -> bool:
        """Remove a pet by name. Return True if something was removed."""
        raise NotImplementedError

    def get_pet(self, pet_name: str) -> Pet:
        """Return the pet with this name."""
        raise NotImplementedError

    def list_pets(self) -> list[Pet]:
        """Return all of this owner's pets."""
        raise NotImplementedError

    def total_daily_task_load(self) -> int:
        """Return the total minutes of tasks across all pets."""
        raise NotImplementedError


class Scheduler:
    """Turns a pet's tasks into a time-ordered daily plan."""

    def __init__(
        self,
        strategy: str = "priority",
        available_minutes: int = 60,
        start_time: str = "08:00",
    ) -> None:
        self.strategy = strategy
        self.available_minutes = available_minutes
        self.start_time = start_time
        self.plan: list[ScheduledTask] = []
        self.skipped: list[Task] = []

    def build_plan(self, pet: Pet, minutes: int | None = None) -> list[ScheduledTask]:
        """Pick and time the tasks that fit the budget; fill self.plan and self.skipped."""
        raise NotImplementedError

    def sort_tasks(self, tasks: list[Task]) -> list[Task]:
        """Order tasks according to self.strategy (priority, duration, ...)."""
        raise NotImplementedError

    def assign_times(self, tasks: list[Task]) -> list[ScheduledTask]:
        """Lay ordered tasks out back-to-back starting at self.start_time."""
        raise NotImplementedError

    def explain(self) -> str:
        """Return a human-readable explanation of the plan and what was skipped."""
        raise NotImplementedError

    def clear(self) -> None:
        """Reset the plan and skipped lists."""
        raise NotImplementedError
