import streamlit as st
import pandas as pd
import altair as alt
from datetime import date
from frontend import check_session

if not check_session():
    st.switch_page('frontend.py')

# Initialize session state
if 'habits' not in st.session_state:
    st.session_state.habits = pd.DataFrame(columns=['Date', 'Habit', 'Completed'])

def save_habit():
    today = date.today().strftime("%Y-%m-%d")
    new_habit = pd.DataFrame({
        'Date': [today],
        'Habit': [habit],
        'Completed': [completed]
    })
    st.session_state.habits = pd.concat([st.session_state.habits, new_habit], ignore_index=True)

st.title('Habit Tracker')

# Input for new habit
with st.form("habit_form"):
    habit = st.text_input("Enter a habit:")
    completed = st.checkbox("Completed")
    submitted = st.form_submit_button("Save")
    if submitted:
        save_habit()

# Display habits
if not st.session_state.habits.empty:
    st.subheader("Your Habits")
    st.dataframe(st.session_state.habits)

    # Visualize habits
    st.subheader("Habit Completion Chart")
    chart = alt.Chart(st.session_state.habits).mark_circle().encode(
        x='Date:T',
        y='Habit:N',
        color='Completed:N',
        size=alt.value(100)
    ).properties(
        width=600,
        height=400
    )
    st.altair_chart(chart)

# Option to clear all data
if st.button("Clear All Data"):
    st.session_state.habits = pd.DataFrame(columns=['Date', 'Habit', 'Completed'])
    st.success("All data cleared!")
