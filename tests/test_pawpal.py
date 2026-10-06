import pytest
import sys
import os

# Add parent directory to path so we can import pawpal_system
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pawpal_system import Task, Pet, Owner, Scheduler, ScheduledTask

def test_task_completion():
    """Test that a task correctly updates its completion status."""
    task = Task(task_id="t1", title="Walk", duration_min=30, priority="high")
    assert task.completed is False
    
    task.mark_complete()
    assert task.completed is True
    
    task.reset()
    assert task.completed is False

def test_filtering_behavior():
    """Test that the scheduler correctly filters out tasks that exceed the time budget."""
    task1 = Task(task_id="t1", title="Quick Walk", duration_min=15)
    task2 = Task(task_id="t2", title="Long Hike", duration_min=120)
    
    scheduler = Scheduler(available_minutes=60)
    
    # max_duration is set to 60. The 120-minute task should be filtered out.
    filtered_tasks = scheduler.filter_tasks([task1, task2], max_duration=60)
    
    assert len(filtered_tasks) == 1
    assert filtered_tasks[0].task_id == "t1"

def test_sorting_correctness():
    """Test that the scheduler correctly sorts tasks by priority and then by preferred_time."""
    # Medium priority, no preferred time
    task1 = Task(task_id="t1", title="Play", duration_min=20, priority="medium", preferred_time="any")
    
    # High priority, no preferred time
    task2 = Task(task_id="t2", title="Feed", duration_min=10, priority="high", preferred_time="any")
    
    # High priority, early preferred time
    task3 = Task(task_id="t3", title="Meds", duration_min=5, priority="high", preferred_time="08:00")
    
    scheduler = Scheduler()
    sorted_tasks = scheduler.sort_tasks([task1, task2, task3])
    
    # Expected order: task3 (high priority, 08:00), task2 (high priority, any), task1 (medium priority)
    assert sorted_tasks[0].task_id == "t3"
    assert sorted_tasks[1].task_id == "t2"
    assert sorted_tasks[2].task_id == "t1"

def test_conflict_detection():
    """Test that the scheduler correctly detects time overlaps."""
    task1 = Task("t1", "Morning walk", duration_min=30)
    task2 = Task("t2", "Give medication", duration_min=5)
    
    # Create overlapping scheduled tasks
    st1 = ScheduledTask(task1, start_time="08:00", end_time="08:30")
    st2 = ScheduledTask(task2, start_time="08:25", end_time="08:30")
    
    scheduler = Scheduler()
    conflicts = scheduler.detect_conflicts([st1, st2])
    
    assert len(conflicts) == 1
    assert "overlaps" in conflicts[0]
