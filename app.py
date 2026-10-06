import streamlit as st
import uuid
from pawpal_system import Owner, Pet, Task, Scheduler, Storage

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="wide")

st.markdown("""
<style>
    :root {
        --primary-color: #E60023;
        --bg-color: #F0F2F5;
        --card-bg: #FFFFFF;
        --text-color: #111111;
        --secondary-text: #767676;
    }
    .stApp { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; }
    .pin-card {
        background-color: var(--card-bg);
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 8px;
        box-shadow: 0 1px 4px rgba(0,0,0,0.08);
        transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
        border: 1px solid #eaeaea;
    }
    .pin-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 16px rgba(0,0,0,0.12);
    }
    .pin-card-done {
        opacity: 0.6;
    }
    .stButton>button {
        background-color: var(--primary-color) !important;
        color: white !important;
        border-radius: 24px !important;
        font-weight: bold !important;
        border: none !important;
        padding: 8px 20px !important;
        transition: background-color 0.2s;
        width: auto !important;
    }
    .stButton>button:hover {
        background-color: #ad081b !important;
        color: white !important;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --- State Initialization ---
if "tasks" not in st.session_state:
    st.session_state.tasks = []
if "pets" not in st.session_state:
    st.session_state.pets = {}
if "owner_name" not in st.session_state:
    st.session_state.owner_name = "Jordan"

# --- Header & Load ---
colA, colB = st.columns([8, 2])
with colA:
    st.markdown("<h1 style='color: #E60023; font-weight: 800; margin-bottom: 0px;'>🐾 PawPal+</h1>", unsafe_allow_html=True)
with colB:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("📂 Load Saved Data"):
        loaded_owner = Storage.load_owner("pawpal_data_streamlit.json")
        if loaded_owner:
            st.session_state.owner_name = loaded_owner.name
            st.session_state.tasks = []
            st.session_state.pets = {}
            for p in loaded_owner.pets:
                st.session_state.pets[p.name] = {
                    "species": p.species, "breed": p.breed, "age": p.age, "weight_kg": p.weight_kg
                }
                for t in p.tasks:
                    st.session_state.tasks.append({
                        "task_id": t.task_id, "title": t.title, "category": t.category,
                        "duration_minutes": t.duration_min, "priority": t.priority,
                        "preferred_time": t.preferred_time, "recurring": t.recurring,
                        "notes": t.notes, "completed": t.completed,
                        "pet_name": p.name, "species": p.species
                    })
        else:
            st.error("No saved data found.")

st.markdown("---")

# --- Profile ---
st.markdown("### 👤 Owner & Pet Profile")
st.session_state.owner_name = st.text_input("Owner Name", value=st.session_state.owner_name)

st.caption("Customize pet details. Change the pet name to add tasks for a different pet.")
pcol1, pcol2, pcol3, pcol4, pcol5 = st.columns(5)
with pcol1:
    pet_name = st.text_input("Pet Name", value="Mochi")
with pcol2:
    species = st.selectbox("Species", ["dog", "cat", "other"])
with pcol3:
    breed = st.text_input("Breed", value="")
with pcol4:
    age = st.number_input("Age (years)", min_value=0, value=0)
with pcol5:
    weight = st.number_input("Weight (kg)", min_value=0.0, value=0.0)

st.session_state.pets[pet_name] = {"species": species, "breed": breed, "age": age, "weight_kg": weight}

st.markdown("---")

# --- Tasks Form ---
st.markdown("### 📋 Care Tasks")
with st.container():
    tcol1, tcol2, tcol3, tcol4, tcol5 = st.columns([2, 1.5, 1.5, 1, 1])
    with tcol1:
        task_title = st.text_input("Task title", value="Morning walk", label_visibility="collapsed", placeholder="Task title")
    with tcol2:
        category = st.text_input("Category", value="Exercise", label_visibility="collapsed", placeholder="Category")
    with tcol3:
        preferred_time = st.text_input("Preferred Time", value="any", label_visibility="collapsed", placeholder="Preferred Time (e.g., 08:00)")
    with tcol4:
        duration = st.number_input("Duration (min)", min_value=1, max_value=240, value=20, label_visibility="collapsed")
    with tcol5:
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2, label_visibility="collapsed")

    with st.expander("Advanced Task Options"):
        adv1, adv2 = st.columns(2)
        with adv1:
            recurring = st.checkbox("Recurring Task (repeats daily)?", value=True)
        with adv2:
            notes = st.text_area("Notes", placeholder="Any special instructions...", height=68)

    if st.button("➕ Add Task"):
        st.session_state.tasks.append({
            "task_id": str(uuid.uuid4()), "title": task_title, "category": category,
            "duration_minutes": int(duration), "priority": priority, "preferred_time": preferred_time,
            "recurring": recurring, "notes": notes, "completed": False,
            "pet_name": pet_name, "species": species
        })

# --- Tasks Grid ---
if st.session_state.tasks:
    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2 = st.columns([8, 2])
    with c2:
        if st.button("🌅 Start New Day"):
            for t in st.session_state.tasks:
                if t.get("recurring", False):
                    t["completed"] = False
                    cb_key = f"done_{t['task_id']}"
                    if cb_key in st.session_state:
                        st.session_state[cb_key] = False
            st.rerun()

    cols = st.columns(4)
    for idx, t in enumerate(st.session_state.tasks):
        with cols[idx % 4]:
            cb_key = f"done_{t['task_id']}"
            if cb_key not in st.session_state:
                st.session_state[cb_key] = t.get("completed", False)
                
            t["completed"] = st.session_state[cb_key]
            
            done_class = "pin-card-done" if t["completed"] else ""
            notes_html = f"<p style='color: #767676; font-size: 13px; font-style: italic; margin-top: 8px;'>📝 {t['notes']}</p>" if t.get("notes") else ""
            st.markdown(f"""
            <div class="pin-card {done_class}">
                <h4 style="margin-top:0; color: #111;">{t['title']}</h4>
                <p style="color: #E60023; font-weight: bold; font-size: 13px; margin-bottom: 8px;">🐾 For: {t.get('pet_name', 'Unknown')}</p>
                <p style="color: #767676; font-size: 14px; margin-bottom: 4px;">⏱️ {t['duration_minutes']} min &nbsp;|&nbsp; ⚡ {t['priority']}</p>
                <p style="color: #767676; font-size: 14px; margin-bottom: 0;">⏰ {t['preferred_time']} &nbsp;|&nbsp; 🔄 {'Yes' if t.get('recurring') else 'No'}</p>
                {notes_html}
            </div>
            """, unsafe_allow_html=True)
            
            # Checkbox to mark complete
            st.checkbox("Done?", key=cb_key)

else:
    st.info("No tasks yet. Add one above to get started.")

st.markdown("---")

# --- Schedule Generation ---
st.markdown("### 🗓️ Build Schedule")
sched_col1, sched_col2, sched_col3 = st.columns(3)
with sched_col1:
    available_minutes = st.number_input("Available minutes", min_value=10, max_value=1440, value=120)
with sched_col2:
    start_time = st.text_input("Start time", value="08:00")
with sched_col3:
    strategy = st.selectbox("Strategy", ["priority", "smart_gaps"], index=1)

if st.button("✨ Generate Schedule", type="primary"):
    if not st.session_state.tasks:
        st.error("Please add at least one task before scheduling.")
    else:
        owner = Owner(name=st.session_state.owner_name, daily_minutes_available=available_minutes)
        
        pets_dict = {}
        for t_dict in st.session_state.tasks:
            p_name = t_dict.get("pet_name", pet_name)
            p_species = t_dict.get("species", species)
            
            if p_name not in pets_dict:
                p_info = st.session_state.pets.get(p_name, {})
                pets_dict[p_name] = Pet(
                    name=p_name, 
                    species=p_info.get("species", p_species),
                    breed=p_info.get("breed", ""),
                    age=p_info.get("age", 0),
                    weight_kg=p_info.get("weight_kg", 0.0)
                )
                
            task = Task(
                task_id=t_dict.get("task_id", str(uuid.uuid4())),
                title=t_dict["title"], category=t_dict.get("category", "general"),
                duration_min=t_dict["duration_minutes"], priority=t_dict["priority"],
                preferred_time=t_dict.get("preferred_time", "any"),
                recurring=t_dict.get("recurring", True), notes=t_dict.get("notes", "")
            )
            task.completed = t_dict.get("completed", False)
            task.pet_name = p_name
            pets_dict[p_name].add_task(task)
            
        for p in pets_dict.values():
            owner.add_pet(p)
        
        Storage.save_owner(owner, "pawpal_data_streamlit.json")
        
        scheduler = Scheduler(strategy=strategy, available_minutes=available_minutes, start_time=start_time)
        scheduler.build_plan(owner.list_pets())
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.success(f"Schedule generated successfully using '{strategy}' strategy!")
        
        conflicts = scheduler.detect_conflicts(scheduler.plan)
        if conflicts:
            for c in conflicts:
                st.error(c)
                
        col_plan, col_skip = st.columns([2, 1])
        with col_plan:
            st.markdown("### ✨ Your Plan")
            if scheduler.plan:
                for stask in scheduler.plan:
                    st.markdown(f"""
                    <div class="pin-card" style="border-left: 5px solid #E60023;">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <h3 style="margin: 0; color: #111;">{stask.task.title}</h3>
                            <span style="background-color: #ffe6e6; color: #E60023; padding: 4px 12px; border-radius: 12px; font-weight: bold; font-size: 14px;">
                                {stask.start_time} - {stask.end_time}
                            </span>
                        </div>
                        <p style="color: #E60023; font-weight: bold; font-size: 13px; margin: 8px 0 0 0;">🐾 For: {getattr(stask.task, 'pet_name', 'Unknown')}</p>
                        <p style="color: #767676; font-size: 14px; margin: 8px 0 0 0;">
                            ⏱️ {stask.task.duration_min} min &nbsp;&bull;&nbsp; ⚡ {stask.task.priority.capitalize()} &nbsp;&bull;&nbsp; 💡 {stask.reason}
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No tasks could be scheduled.")
                
        with col_skip:
            skipped_tasks = scheduler.skipped
            completed_tasks = [t for p in owner.list_pets() for t in p.tasks if t.completed]
            
            if skipped_tasks or completed_tasks:
                st.markdown("### ⚠️ Skipped / Done")
                
                # Render completed
                for s in completed_tasks:
                    st.markdown(f"""
                    <div class="pin-card" style="border-left: 5px solid #4CAF50; opacity: 0.8; padding: 16px;">
                        <h4 style="margin: 0; color: #555;">{s.title}</h4>
                        <p style="color: #4CAF50; font-weight: bold; font-size: 13px; margin: 4px 0 0 0;">🐾 For: {getattr(s, 'pet_name', 'Unknown')}</p>
                        <p style="color: #767676; font-size: 14px; margin: 4px 0 0 0;">
                            ✅ Already Completed &nbsp;&bull;&nbsp; ⏱️ {s.duration_min} min
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                # Render skipped due to time
                for s in skipped_tasks:
                    st.markdown(f"""
                    <div class="pin-card" style="border-left: 5px solid #767676; opacity: 0.8; padding: 16px;">
                        <h4 style="margin: 0; color: #555;">{s.title}</h4>
                        <p style="color: #E60023; font-weight: bold; font-size: 13px; margin: 4px 0 0 0;">🐾 For: {getattr(s, 'pet_name', 'Unknown')}</p>
                        <p style="color: #767676; font-size: 14px; margin: 4px 0 0 0;">
                            ⏳ Not enough time &nbsp;&bull;&nbsp; ⏱️ {s.duration_min} min
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
