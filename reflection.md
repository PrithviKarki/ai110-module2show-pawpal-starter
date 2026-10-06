# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?
**Answer:**
The initial design was structured around Object-Oriented Programming (OOP) to cleanly separate data and logic. I included the following core classes:
- **Owner**: Manages the user's available time and a list of their pets.
- **Pet**: Holds pet details (species, age, etc.) and acts as a container for a list of `Task` objects.
- **Task**: Represents individual care activities (title, duration, priority, preferred time).
- **ScheduledTask**: A wrapper for a `Task` that assigns it a specific start and end time.
- **Scheduler**: The core engine that takes an Owner's pets and available time, and processes the tasks using specific algorithms.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.
**Answer:**
Yes. Initially, the project started with managing tasks for just one pet. As the project grew, the design evolved to handle multiple pets simultaneously. We updated the `Scheduler.build_plan` method to accept a list of pets and extract all their tasks into a single pool. We also introduced a `Storage` class to serialize these objects into JSON, allowing data persistence between UI sessions.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?
**Answer:**
The scheduler evaluates `available_minutes` (the time budget), `priority` (high/medium/low mapped to scores), `preferred_time` (anchoring tasks to specific times), and `duration_min`. The time budget is the hardest constraint (Algorithm 2 strictly drops tasks that exceed the remaining time). Among tasks that fit, Priority is the most important factor, followed by preferred time slots, ensuring the most critical care happens first.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?
**Answer:**
In the advanced `smart_gaps` strategy, the tradeoff is that anchored tasks (those with a strict `preferred_time`) are placed on the timeline first, and floating tasks are squeezed into the gaps. A tradeoff here is that a low-priority anchored task might consume a time slot that blocks a higher-priority floating task from being scheduled. This is a reasonable tradeoff because time-sensitive tasks (like administering medication exactly at 08:00) are usually non-negotiable, whereas general tasks (like brushing) are flexible.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?
**Answer:**
I used an Agentic AI assistant as a pair programmer to build the OOP backend, implement complex algorithms (sorting, filtering, gap filling), and construct a Pinterest-styled Streamlit UI. The most helpful prompts were highly specific about constraints and goals—for example, explicitly asking to "Wire up app.py to the backend to render custom schedule output" and defining specific UI aesthetics ("create a minimalistic yet aesthetic design inspired by the UI of Pinterest").

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?
**Answer:**
There was a subtle bug where the AI placed the `handle_recurring_tasks()` logic *inside* the `build_plan()` backend method. This meant whenever I clicked "Done" on a task in the UI and regenerated the schedule, the backend aggressively overrode the UI, resetting the recurring task back to "incomplete" and scheduling it again! I verified this by noticing the UI bug (done tasks kept showing up) and evaluating the backend trace. I instructed the AI to remove that automated reset from the backend and let the UI's "Start New Day" button handle resetting checkboxes instead.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?
**Answer:**
I built a `pytest` suite (`tests/test_pawpal.py`) to test state changes (`task_completion`), time-budget constraints (`filtering_behavior`), prioritization algorithms (`sorting_correctness`), and overlap scenarios (`conflict_detection`). These tests were critical to ensure the backend logic was rock-solid before hooking it up to a dynamic UI, guaranteeing that the scheduler would never assign 90 minutes of tasks if the user only had 60 minutes.

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?
**Answer:**
I am highly confident in the core scheduler since the Pytest suite passes and the interactive Streamlit UI successfully handles the end-to-end flow. If I had more time, I would test edge cases involving tasks that span past midnight, or highly congested schedules where multiple anchored tasks overlap and require advanced collision resolution.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
**Answer:**
I am extremely satisfied with the final Streamlit UI integration. The customized Pinterest-inspired masonry grid, the clear red/green visual badging for scheduled versus completed tasks, and the multi-pet tagging `🐾 For: Mochi (dog)` made the underlying backend OOP logic feel like a real, polished consumer application.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?
**Answer:**
I would redesign the time handling to use native Python `datetime` objects rather than parsing string times like "08:00". This would make it much easier to handle true calendar scheduling, time zones, duration math, and midnight rollovers natively without custom string parsing.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
**Answer:**
Working with AI requires strict oversight of state management. The AI is incredibly fast at generating complex algorithms, but combining a stateless UI framework (Streamlit) with persistent backend data structures can easily lead to synchronization bugs (like the recurring task reset loop). It taught me the importance of clearly separating UI widget state from backend object states.