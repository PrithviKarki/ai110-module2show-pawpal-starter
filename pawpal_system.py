"""PawPal+ core classes.

Skeleton generated from diagrams/uml.mmd. Attributes are wired up in the
constructors; every method body is still a stub for you to implement.
"""

from __future__ import annotations
import json


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
        scores = {"high": 3, "medium": 2, "low": 1}
        return scores.get(self.priority.lower(), 0)

    def mark_complete(self) -> None:
        """Mark this task as done for the day."""
        self.completed = True

    def reset(self) -> None:
        """Clear the completed flag (e.g. at the start of a new day)."""
        self.completed = False

    def fits_in(self, minutes_left: int) -> bool:
        """Return True if this task can still fit in the remaining time budget."""
        return self.duration_min <= minutes_left

    def __str__(self) -> str:
        """Return a readable one-line summary of the task."""
        status = "[x]" if self.completed else "[ ]"
        return f"{status} {self.title} ({self.duration_min} min, priority: {self.priority})"

    def to_dict(self) -> dict:
        return {
            "task_id": self.task_id,
            "title": self.title,
            "category": self.category,
            "duration_min": self.duration_min,
            "priority": self.priority,
            "preferred_time": self.preferred_time,
            "recurring": self.recurring,
            "completed": self.completed,
            "notes": self.notes
        }

    @classmethod
    def from_dict(cls, data: dict) -> Task:
        t = cls(
            task_id=data["task_id"],
            title=data["title"],
            category=data.get("category", "general"),
            duration_min=data.get("duration_min", 15),
            priority=data.get("priority", "medium"),
            preferred_time=data.get("preferred_time", "any"),
            recurring=data.get("recurring", True),
            notes=data.get("notes", "")
        )
        t.completed = data.get("completed", False)
        return t


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

    def __str__(self) -> str:
        """Return a readable line like '08:00-08:30  Morning walk (reason)'."""
        return f"{self.start_time}-{self.end_time}  {self.task.title} ({self.reason})"


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
        self.tasks.append(task)

    def remove_task(self, task_id: str) -> bool:
        """Remove a task by id. Return True if something was removed."""
        original_count = len(self.tasks)
        self.tasks = [t for t in self.tasks if t.task_id != task_id]
        return len(self.tasks) < original_count

    def get_tasks(self, only_due: bool = False) -> list[Task]:
        """Return this pet's tasks; if only_due, skip the completed ones."""
        if only_due:
            return [t for t in self.tasks if not t.completed]
        return self.tasks

    def is_senior(self) -> bool:
        """Return True if the pet counts as senior for its species."""
        species_lower = self.species.lower()
        if species_lower == "dog":
            return self.age >= 7
        elif species_lower == "cat":
            return self.age >= 10
        return self.age >= 8

    def daily_activity_need(self) -> int:
        """Return the recommended minutes of activity per day for this pet."""
        if self.is_senior():
            return 30
        return 60

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "species": self.species,
            "breed": self.breed,
            "age": self.age,
            "weight_kg": self.weight_kg,
            "tasks": [t.to_dict() for t in self.tasks]
        }

    @classmethod
    def from_dict(cls, data: dict) -> Pet:
        p = cls(
            name=data["name"],
            species=data["species"],
            breed=data.get("breed", ""),
            age=data.get("age", 0),
            weight_kg=data.get("weight_kg", 0.0)
        )
        if "tasks" in data:
            for t_data in data["tasks"]:
                p.add_task(Task.from_dict(t_data))
        return p


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
        self.pets.append(pet)

    def remove_pet(self, pet_name: str) -> bool:
        """Remove a pet by name. Return True if something was removed."""
        original_count = len(self.pets)
        self.pets = [p for p in self.pets if p.name != pet_name]
        return len(self.pets) < original_count

    def get_pet(self, pet_name: str) -> Pet:
        """Return the pet with this name."""
        for p in self.pets:
            if p.name == pet_name:
                return p
        raise ValueError(f"Pet {pet_name} not found.")

    def list_pets(self) -> list[Pet]:
        """Return all of this owner's pets."""
        return self.pets

    def total_daily_task_load(self) -> int:
        """Return the total minutes of tasks across all pets."""
        return sum(t.duration_min for p in self.pets for t in p.tasks if not t.completed)

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "email": self.email,
            "daily_minutes_available": self.daily_minutes_available,
            "preferred_times": self.preferred_times,
            "pets": [p.to_dict() for p in self.pets]
        }

    @classmethod
    def from_dict(cls, data: dict) -> Owner:
        o = cls(
            name=data["name"],
            email=data.get("email", ""),
            daily_minutes_available=data.get("daily_minutes_available", 60),
            preferred_times=data.get("preferred_times", [])
        )
        if "pets" in data:
            for p_data in data["pets"]:
                o.add_pet(Pet.from_dict(p_data))
        return o


class Storage:
    """Handles Data Persistence Layer for saving and loading Owners (with their pets and tasks)."""
    
    @staticmethod
    def save_owner(owner: Owner, filename: str = "pawpal_data.json") -> None:
        with open(filename, "w") as f:
            json.dump(owner.to_dict(), f, indent=4)

    @staticmethod
    def load_owner(filename: str = "pawpal_data.json") -> Owner | None:
        try:
            with open(filename, "r") as f:
                data = json.load(f)
                return Owner.from_dict(data)
        except (FileNotFoundError, json.JSONDecodeError):
            return None


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

    def build_plan(self, pets: Pet | list[Pet], minutes: int | None = None) -> list[ScheduledTask]:
        """Pick and time the tasks that fit the budget; fill self.plan and self.skipped."""
        self.clear()
        budget = minutes if minutes is not None else self.available_minutes
        
        if isinstance(pets, Pet):
            pets = [pets]
            
            
        all_tasks = []
        for p in pets:
            # get_tasks with only_due=True acts as an initial filter for completion
            all_tasks.extend(p.get_tasks(only_due=True))
            
        # Algorithm 2: Filtering tasks
        viable_tasks = self.filter_tasks(all_tasks, budget)
            
        # Algorithm 1: Sorting tasks by due time/priority
        ordered_tasks = self.sort_tasks(viable_tasks)
        
        tasks_to_schedule = []
        for task in ordered_tasks:
            if task.fits_in(budget):
                tasks_to_schedule.append(task)
                budget -= task.duration_min
            else:
                self.skipped.append(task)
                
        self.plan = self.assign_times(tasks_to_schedule)
        return self.plan

    def sort_tasks(self, tasks: list[Task]) -> list[Task]:
        """Algorithm 1: Order tasks according to priority AND due time (preferred time)."""
        def time_score(t: Task) -> int:
            if t.preferred_time.lower() == "any":
                return 9999
            try:
                h, m = map(int, t.preferred_time.split(':'))
                return h * 60 + m
            except ValueError:
                return 9999

        # Sort primarily by priority score (descending), then by due time (ascending)
        return sorted(tasks, key=lambda t: (-t.priority_score(), time_score(t)))

    def filter_tasks(self, tasks: list[Task], max_duration: int) -> list[Task]:
        """Algorithm 2: Filter out tasks that are completely unfeasible within the time budget."""
        return [t for t in tasks if t.duration_min <= max_duration]

    def detect_conflicts(self, scheduled: list[ScheduledTask]) -> list[str]:
        """Algorithm 3: Detect any scheduling conflicts (overlapping times) across the multi-pet schedule."""
        conflicts = []
        
        def to_minutes(time_str: str) -> int:
            h, m = map(int, time_str.split(':'))
            return h * 60 + m
            
        # Ensure chronological order to easily find overlapping items
        scheduled_sorted = sorted(scheduled, key=lambda st: to_minutes(st.start_time))
        
        for i in range(len(scheduled_sorted) - 1):
            curr_task = scheduled_sorted[i]
            next_task = scheduled_sorted[i+1]
            
            # If the current task ends strictly after the next one begins, it's a conflict
            if to_minutes(curr_task.end_time) > to_minutes(next_task.start_time):
                conflicts.append(
                    f"Conflict: '{curr_task.task.title}' overlaps with '{next_task.task.title}'"
                )
        return conflicts

    def handle_recurring_tasks(self, pets: list[Pet]) -> None:
        """Algorithm 4: Scan across multiple pets to handle recurring tasks, resetting their status."""
        for pet in pets:
            for task in pet.tasks:
                if task.recurring and task.completed:
                    task.reset()

    def assign_times(self, tasks: list[Task]) -> list[ScheduledTask]:
        """Lay ordered tasks out. If strategy is 'smart_gaps', use advanced Next Available Slot algorithm."""
        scheduled = []
        
        try:
            h, m = map(int, self.start_time.split(':'))
        except ValueError:
            h, m = 8, 0
            
        day_start_minutes = h * 60 + m
        
        if self.strategy == "smart_gaps":
            # Advanced Algorithmic Capability: Next Available Slot
            anchored_tasks = []
            floating_tasks = []
            for t in tasks:
                if t.preferred_time.lower() != "any":
                    try:
                        ph, pm = map(int, t.preferred_time.split(':'))
                        start_min = ph * 60 + pm
                        end_min = start_min + t.duration_min
                        anchored_tasks.append((t, start_min, end_min))
                    except ValueError:
                        floating_tasks.append(t)
                else:
                    floating_tasks.append(t)
            
            def to_time_str(mins):
                return f"{mins // 60:02d}:{mins % 60:02d}"

            for t, s_min, e_min in anchored_tasks:
                scheduled.append(ScheduledTask(t, to_time_str(s_min), to_time_str(e_min), "smart_gaps: anchored"))

            for t in floating_tasks:
                current_check = day_start_minutes
                while True:
                    overlap = False
                    for st in scheduled:
                        st_s = int(st.start_time.split(':')[0])*60 + int(st.start_time.split(':')[1])
                        st_e = int(st.end_time.split(':')[0])*60 + int(st.end_time.split(':')[1])
                        
                        if max(current_check, st_s) < min(current_check + t.duration_min, st_e):
                            current_check = st_e
                            overlap = True
                            break
                    
                    if not overlap:
                        s_min = current_check
                        e_min = current_check + t.duration_min
                        scheduled.append(ScheduledTask(t, to_time_str(s_min), to_time_str(e_min), "smart_gaps: gap-filled"))
                        break
        else:
            current_time_minutes = day_start_minutes
            for task in tasks:
                pref_time_minutes = None
                if task.preferred_time.lower() != "any":
                    try:
                        ph, pm = map(int, task.preferred_time.split(':'))
                        pref_time_minutes = ph * 60 + pm
                    except ValueError:
                        pass
                
                if pref_time_minutes is not None:
                    current_time_minutes = pref_time_minutes
                    
                start_h = current_time_minutes // 60
                start_m = current_time_minutes % 60
                
                current_time_minutes += task.duration_min
                
                end_h = current_time_minutes // 60
                end_m = current_time_minutes % 60
                
                start_str = f"{start_h:02d}:{start_m:02d}"
                end_str = f"{end_h:02d}:{end_m:02d}"
                
                scheduled.append(ScheduledTask(task, start_str, end_str, f"strategy: {self.strategy}"))
                
        # Chronological sort for final presentation
        scheduled.sort(key=lambda st: int(st.start_time.split(':')[0])*60 + int(st.start_time.split(':')[1]))
        return scheduled

    def explain(self) -> str:
        """Return a human-readable explanation of the plan and what was skipped."""
        lines = [f"Plan Explanation (Strategy: {self.strategy})"]
        
        conflicts = self.detect_conflicts(self.plan)
        if conflicts:
            lines.append("WARNING - Scheduling Conflicts Detected:")
            for c in conflicts:
                lines.append(f" ! {c}")
                
        lines.append(f"Scheduled tasks: {len(self.plan)}")
        for st in self.plan:
            lines.append(f" - {st}")
            
        lines.append(f"Skipped tasks: {len(self.skipped)}")
        if self.skipped:
            lines.append("Skipped due to time constraints:")
            for s in self.skipped:
                lines.append(f" - {s.title} ({s.duration_min} min)")
        return "\n".join(lines)

    def clear(self) -> None:
        """Reset the plan and skipped lists."""
        self.plan = []
        self.skipped = []

