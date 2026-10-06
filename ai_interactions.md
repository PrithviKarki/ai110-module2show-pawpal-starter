# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agent Workflow (SF7)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

I gave the AI Agent (Antigravity) a massive multi-step task: first, to wire up a bare-bones Streamlit `app.py` to our custom Object-Oriented backend (`pawpal_system.py`); second, to redesign the UI with a Pinterest-inspired aesthetic; and third, to debug a complex state-synchronization issue where tasks marked as "Done" were magically reverting themselves and appearing in the schedule.

**What did the agent do?**

The agent executed a series of autonomous changes across the codebase:
1. **Integration:** It rewrote `app.py` to parse form inputs, construct `Owner`, `Pet`, and `Task` objects, and pass them to the `Scheduler`.
2. **Redesign:** It replaced generic Streamlit tables with injected CSS and HTML, creating interactive, masonry-style "pin-cards".
3. **Debugging:** When I reported that the "Done" checkboxes were laggy and not removing tasks from the schedule, the agent autonomously tracked the bug down to two places. It fixed Streamlit's `st.session_state` binding in the UI to remove the lag, and it opened the backend file (`pawpal_system.py`) to rip out a line of code (`handle_recurring_tasks`) that was forcefully overriding my UI inputs.

**What did you have to verify or fix manually?**

I had to playtest the UI extensively to catch the state-desync bug in the first place, acting as QA for the agent. Once the agent deployed the fixes, I manually verified them by clicking checkboxes rapidly to ensure the UI didn't lag, and by checking the "⚠️ Skipped / Done" column to confirm that the backend was finally respecting the UI's completed tasks.

---

## Prompt Comparison (SF11)

> Compare two different prompts (or two different models) on the same task.

| | Option A | Option B |
|-|----------|----------|
| **Model / tool used** | Gemini 3.1 Pro (Generic Prompting) | Gemini 3.1 Pro (Detailed Constraints) |
| **Prompt** | "Write a python sorting function for pet care tasks based on priority." | "Write a Python `sort_tasks` method for a `Scheduler` class that takes a list of `Task` objects. Sort them primarily by `priority_score()` descending. If there is a tie, sort them chronologically by their `preferred_time` string (e.g. '08:00' before '09:00'), treating 'any' as the end of the day." |
| **Response summary** | Generated a very basic, generic sorting function using `sorted()` that assumed `Task` had a simple `priority` integer attribute. | Generated a highly specific lambda key using tuples to sort by `priority_score()` first, alongside a custom nested helper function to parse strings into integers for the tie-breaker. |
| **What was useful** | Provided a quick, readable reminder of how Python's `sorted(key=lambda x: ...)` function works syntax-wise. | The time-parsing helper function was incredibly clever and gave me the exact logic needed to convert "HH:MM" strings into sortable integers. |
| **Problems noticed** | The code was too abstract. It guessed the wrong attribute names and didn't include the tie-breaking time logic I actually needed, rendering it mostly useless. | Handled the core logic perfectly, though I did manually wrap the time parser in a `try/except ValueError` block just in case a user entered a malformed time string. |
| **Decision** | Rejected. | Accepted (with minor manual safety tweaks). |

**Which approach did you use in your final implementation and why?**

I used the detailed, constraint-based approach (Option B) for the final implementation. By explicitly feeding the AI the exact class context, identifying edge cases (like how to handle the word 'any'), and defining the tie-breaker rules upfront, it was able to generate complex, production-ready sorting logic. The generic prompt created too much technical debt and required rewriting the entire sorting algorithm manually just to fit the codebase.
