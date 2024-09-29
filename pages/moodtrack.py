import streamlit as st
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date
import os
from home import check_session

if not check_session():
    st.switch_page('home.py')

# File to store the mood data
MOOD_FILE = "mood_tracker.csv"

@st.cache_data
def load_data():
    if os.path.exists(MOOD_FILE):
        return pd.read_csv(MOOD_FILE)
    return pd.DataFrame(columns=["Date", "Mood", "Notes"])

def save_data(df):
    df.to_csv(MOOD_FILE, index=False)

def create_mood_chart(df):
    # Convert 'Date' to datetime and sort
    df['Date'] = pd.to_datetime(df['Date'])
    df_sorted = df.sort_values('Date')
    
    # Create the Plotly chart
    fig = px.line(df_sorted, x='Date', y='Mood',
                  title='Mood Tracker Over Time',
                  labels={'Mood': 'Mood (1-5)', 'Date': 'Date'},
                  markers=True)
    
    # Customize the layout
    fig.update_layout(yaxis_range=[1, 5])
    fig.update_traces(textposition='top center')
    
    return fig

def main():
    st.title("Mood Tracker")

    # Load existing data
    mood_data = load_data()

    # Display existing data
    if not mood_data.empty:
        st.subheader("Your Mood History")
        st.dataframe(mood_data)

        # Create and display the mood chart
        mood_chart = create_mood_chart(mood_data)
        st.plotly_chart(mood_chart)

    # Input form for daily mood
    st.subheader("Log Today's Mood")
    
    # Get today's date
    today = date.today().strftime("%Y-%m-%d")
    
    # Check if an entry for today already exists
    today_entry = mood_data[mood_data['Date'] == today]
    if not today_entry.empty:
        st.warning("You've already made an entry for today. You can update it below.")
        mood = st.slider("Mood (1 = Very Low, 5 = Very High)", 1, 5, int(today_entry['Mood'].values[0]))
        notes = st.text_area("Notes", value=today_entry['Notes'].values[0])
    else:
        mood = st.slider("Mood (1 = Very Low, 5 = Very High)", 1, 5)
        notes = st.text_area("Notes")

    if st.button("Save Mood"):
        new_entry = pd.DataFrame({
            "Date": [today],
            "Mood": [mood],
            "Notes": [notes]
        })

        # If entry for today exists, update it; otherwise, append new entry
        if not today_entry.empty:
            mood_data.loc[mood_data['Date'] == today] = new_entry.values
        else:
            mood_data = pd.concat([mood_data, new_entry], ignore_index=True)

        # Save the updated data
        save_data(mood_data)
        st.success("Mood saved successfully!")

        # Clear the cache to reflect the new data
        load_data.clear()
        
        # Rerun the app to show updated data
        st.rerun()

if __name__ == "__main__":
    main()

