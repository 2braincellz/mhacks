import streamlit as st
import pandas as pd
from datetime import datetime, date
from home import check_session

if not check_session():
    st.switch_page('home.py')

# Initialize tasks DataFrame in session state
if 'tasks' not in st.session_state:
    st.session_state.tasks = pd.DataFrame(columns=['Task', 'Due Date', 'Days Until Due'])

def add_task(task, due_date):
    new_task = pd.DataFrame({'Task': [task], 'Due Date': [due_date]})
    st.session_state.tasks = pd.concat([st.session_state.tasks, new_task], ignore_index=True)

def calculate_days_until_due():
    today = pd.to_datetime(date.today()) 
    st.session_state.tasks['Due Date'] = pd.to_datetime(st.session_state.tasks['Due Date'])
    #st.session_state.tasks['Due Date'] = st.session_state.tasks['Due Date'].dt.date
    st.session_state.tasks['Days Until Due'] = (st.session_state.tasks['Due Date'] - today).dt.days
def main():
    st.title("Task Tracker")

    # Input form for new task
    with st.form("new_task_form"):
        task_description = st.text_input("Task Description")
        due_date = st.date_input("Due Date")
        submit_button = st.form_submit_button("Add Task")

        if submit_button and task_description:
            add_task(task_description, due_date)
            st.success("Task added successfully!")

    # Calculate days until due for all tasks
    if not st.session_state.tasks.empty:
        calculate_days_until_due()

    # Display tasks
    if not st.session_state.tasks.empty:
        st.subheader("Your Tasks")
        # Sort tasks by due date
        sorted_tasks = st.session_state.tasks.sort_values('Due Date')
        # Display tasks with custom formatting
        for _, task in sorted_tasks.iterrows():
            days_until_due = task['Days Until Due']
            if days_until_due < 0:
                status = "🔴 Overdue"
            elif days_until_due == 0:
                status = "🟠 Due Today"
            else:
                status = "🟢 Upcoming"
            
            st.markdown(f"**{task['Task']}**")
            st.markdown(f"Due Date: {task['Due Date']} | Days Until Due: {days_until_due} | Status: {status}")
            st.markdown("---")

    # Option to clear all tasks
    if st.button("Clear All Tasks"):
        st.session_state.tasks = pd.DataFrame(columns=['Task', 'Due Date', 'Days Until Due'])
        st.success("All tasks cleared!")

if __name__ == "__main__":
    main()
st.markdown("---")
# st.markdown("GAAT: Greatest App of All Time")
