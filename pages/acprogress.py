import streamlit as st
import pandas as pd
import plotly
from datetime import date
import os
from frontend import check_session

if not check_session():
    st.switch_page('frontend.py')

# File to store the progress data
PROGRESS_FILE = "academic_progress.csv"

@st.cache_data
def load_data():
    if os.path.exists(PROGRESS_FILE):
        return pd.read_csv(PROGRESS_FILE)
    return pd.DataFrame(columns=["Date", "Subject", "Hours", "Progress_Notes"])

@st.cache_data
def save_data(df):
    df.to_csv(PROGRESS_FILE, index=False)
def displaying_data(df):
    #TODO: Hours over a month

    #TODO: Subject hour breakdown
    st.line_chart(df['Hours'])
    
def main():

    st.title("Academic Progress Tracker")
    # Load existing data
    progress_data = load_data()

    # Display existing data
    if not progress_data.empty:
        st.subheader("Your Progress So Far")
        displaying_data(progress_data)
        st.dataframe(progress_data)

    # Input form for daily progress
    st.subheader("Log Today's Progress")
    
    # Get today's date
    today = date.today().strftime("%Y-%m-%d")
    
    # Check if an entry for today already exists
    if today in progress_data['Date'].values:
        st.warning("You've already made an entry for today. You can update it below.")

    subject = st.text_input("Subject")
    hours = st.number_input("Hours Spent", min_value=0.0, max_value=24.0, step=0.5)
    progress_notes = st.text_area("Progress Notes")

    if st.button("Save Progress"):
        new_entry = pd.DataFrame({
            "Date": [today],
            "Subject": [subject],
            "Hours": [hours],
            "Progress_Notes": [progress_notes]
        })

        # If entry for today exists, update it; otherwise, append new entry
        #if today in progress_data['Date'].values:
        #    progress_data.loc[progress_data['Date'] == today] = new_entry.values
        #else:
        progress_data = pd.concat([progress_data, new_entry], ignore_index=True)

        # Save the updated data
        save_data(progress_data)
        st.success("Progress saved successfully!")

        # Clear the cache to reflect the new data
        load_data.clear()
        
        # Refresh the displayed data
        st.rerun()

if __name__ == "__main__":
    main()

