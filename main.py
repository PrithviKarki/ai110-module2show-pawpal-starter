from pawpal_system import Owner, Pet, Task, Scheduler

def main():
    print("🐾 Welcome to PawPal+ CLI Demo 🐾\n")

    # 1. Create Owner
    owner = Owner(name="Alex", email="alex@example.com", daily_minutes_available=60)
    print(f"Created Owner: {owner.name} with {owner.daily_minutes_available} mins available today.")

    # 2. Create Pets (2)
    dog = Pet(name="Biscuit", species="Dog", breed="Golden Retriever", age=5)
    cat = Pet(name="Mochi", species="Cat", breed="Siamese", age=3)
    
    owner.add_pet(dog)
    owner.add_pet(cat)
    print(f"Added Pets: {dog.name} ({dog.species}) and {cat.name} ({cat.species})\n")

    # 3. Create Tasks (3+)
    task1 = Task(task_id="t1", title="Morning walk", duration_min=30, priority="high", preferred_time="08:00")
    task2 = Task(task_id="t2", title="Feed Breakfast", duration_min=10, priority="high", preferred_time="08:30")
    task3 = Task(task_id="t3", title="Playtime", duration_min=20, priority="medium", preferred_time="any")
    task4 = Task(task_id="t4", title="Brush fur", duration_min=15, priority="low", preferred_time="09:00")
    
    # Intentionally cause a conflict with another task (Morning walk overlaps with Give medication)
    task5 = Task(task_id="t5", title="Give medication", duration_min=5, priority="high", preferred_time="08:25")
    
    dog.add_task(task1)
    dog.add_task(task2)
    dog.add_task(task3)
    
    cat.add_task(task4)
    cat.add_task(task5)

    print("Tasks added across all pets:")
    for p in owner.pets:
        print(f"- {p.name}'s tasks:")
        for t in p.tasks:
            print(f"    - {t.title} ({t.duration_min}m, priority: {t.priority}, time: {t.preferred_time})")
    
    # 4. Use Scheduler
    print("\nInitializing Scheduler...")
    scheduler = Scheduler(strategy="priority", available_minutes=owner.daily_minutes_available, start_time="08:00")
    
    print("\n--- Generating Schedule (Executing Algorithms) ---")
    plan = scheduler.build_plan(owner.pets)
    
    # 5. Output
    print(scheduler.explain())

if __name__ == "__main__":
    main()

