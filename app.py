import streamlit as st
import json
import os

# Set Streamlit page config
st.set_page_config(page_title="Agile Mastery for C.O.M Professionals", layout="wide")

# Constants
COURSE_TITLE = "Agile Mastery for C.O.M Professionals"
DATA_DIR = "data"
MODULES_FILE = os.path.join(DATA_DIR, "modules.json")

# Initialize session state
if "points" not in st.session_state:
    st.session_state.points = 0
if "completed" not in st.session_state:
    st.session_state.completed = []
if "badges" not in st.session_state:
    st.session_state.badges = []
if "current_module" not in st.session_state:
    st.session_state.current_module = 0

# Load module definitions
@st.cache_data
def load_modules():
    if not os.path.exists(MODULES_FILE):
        st.error("Modules data file not found. Please upload modules.json to the 'data' folder.")
        return []
    with open(MODULES_FILE, "r") as f:
        return json.load(f)

modules = load_modules()
if not modules:
    st.stop()

# Sidebar navigation & progress
st.sidebar.title(COURSE_TITLE)
st.sidebar.markdown("### Progress & Rewards")
st.sidebar.write(f"**Points:** {st.session_state.points}")
st.sidebar.write("**Badges:**")
for badge in st.session_state.badges:
    st.sidebar.write(f"- {badge}")
st.sidebar.markdown("---")

module_names = [m["title"] for m in modules]
selected = st.sidebar.radio("Select Module", module_names, index=st.session_state.current_module)
st.session_state.current_module = module_names.index(selected)
current = modules[st.session_state.current_module]

# Main content
st.header(current['title'])
st.write(current.get('description', ''))

# Video
if current.get('video_url'):
    st.video(current['video_url'])

# Reading / instructions
for section in current.get('sections', []):
    if section['type'] == 'text':
        st.markdown(section['content'])

# Quiz
if current.get('quiz'):
    st.subheader("Quiz")
    answers = {}
    for i, q in enumerate(current['quiz']):
        answers[i] = st.radio(q['question'], q['options'], key=f"q{st.session_state.current_module}_{i}")
    if st.button("Submit Quiz", key=f"submit_{st.session_state.current_module}"):
        score = 0
        for i, q in enumerate(current['quiz']):
            if answers[i] == q['answer']:
                score += 1
        pts = score * 10
        st.session_state.points += pts
        st.success(f"You scored {score}/{len(current['quiz'])} and earned {pts} points!")
        if current['title'] not in st.session_state.completed:
            st.session_state.completed.append(current['title'])
        badge = current.get('badge')
        if badge and badge not in st.session_state.badges:
            st.session_state.badges.append(badge)
            st.balloons()
            st.success(f"Badge earned: {badge}")

# Navigation
st.markdown("---")
col1, col2 = st.columns(2)
if col1.button("<< Previous Module"):
    if st.session_state.current_module > 0:
        st.session_state.current_module -= 1
        st.experimental_rerun()
if col2.button("Next Module >>"):
    if st.session_state.current_module < len(modules) - 1:
        st.session_state.current_module += 1
        st.experimental_rerun()
