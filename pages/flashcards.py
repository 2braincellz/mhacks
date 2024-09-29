#import OCRget as * OCRget
#import reading_image as * reading_image
import streamlit as st
import pandas as pd
import os
import groq
import random

client = groq.Client(api_key=os.environ["GROQ_API_KEY"])

st.title("Flashcards")
FLASHCARD_FILE = 'flashcards.csv'

# TODO: DISPLAYING FLASHCARDS
def load_flashcards_sets():
    if os.path.exists(FLASHCARD_FILE):
        return pd.read_csv(FLASHCARD_FILE, sep=';')
    return pd.DataFrame(columns=['Set Name', 'Question', 'Answer'])

def save_flashcards(df):
    df.to_csv(FLASHCARD_FILE, index=False, sep=';')

def create_flashcards(notes):
    prompt = f"""
    Given the following notes, create 5 flashcard-style question and answer pairs:

    {notes}

    Format each flashcard as:
    Q: [Question]
    A: [Answer]

    Ensure questions test key concepts and answers are concise.
    """

    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are an expert at creating educational flashcards to maximize retention."},
            {"role": "user", "content": prompt}
        ],
        model="llama3-70b-8192",
        temperature=0.5,
        max_tokens=500
    )

    return chat_completion.choices[0].message.content

def add_flashcards(set_name, question, answer):
    flashcards = load_flashcards_sets()
    new_flashcard = pd.DataFrame({'Set Name': [set_name], 'Question': question, 'Answer': answer})
    flashcards = pd.concat([flashcards, new_flashcard], ignore_index=True)
    save_flashcards(flashcards)

def get_unique_sets():
    flashcards = load_flashcards_sets()
    return sorted(flashcards['Set Name'].unique())

def next_card(length):
    st.session_state.current_card = random.randint(0, length - 1)
    st.session_state.show_answer = False

def flip_card():
    st.session_state.show_answer = not st.session_state.show_answer

def main():
    # text is a string
    # text = OCRget.detect_text()

    # clean up text
    # cleaned_text = reading_image.model(text)
    notes = """
    The water cycle, also known as the hydrologic cycle, describes the continuous movement of water within the Earth and atmosphere.
    It involves processes such as evaporation, condensation, precipitation, and runoff.
    The sun drives the water cycle by heating water in oceans and on land, causing evaporation.
    Water vapor rises into the atmosphere, cools, and forms clouds through condensation.
    Precipitation occurs when water droplets in clouds become heavy enough to fall as rain or snow.
    """
    tab1, tab2, tab3 = st.tabs(["Create", "View", "Study"])
    content = st.container()
    
    with tab1:
        set_name = st.text_input("Enter the set name")
        question = st.text_input("Enter question")
        answer = st.text_input("Enter answer")
        submitted = st.button("Save")
        if submitted:
            add_flashcards(set_name, question, answer)
        # todo - choose something from database
        # st.write("in progress")
    
    with tab2:
        flashcards = load_flashcards_sets()
        if not flashcards.empty:
            unique_flashcards = get_unique_sets()
            set_choice = st.selectbox("Choose a set: ", unique_flashcards, key="tab2")
            set_flashcards = flashcards[flashcards['Set Name'] == set_choice]
            st.dataframe(set_flashcards[['Question', 'Answer']])
        else:
            st.info("No flashcards available. Create some!")

    with tab3:
        # st.write("in progress")
        flashcards = load_flashcards_sets()
        if not flashcards.empty:
            set_choice = st.selectbox("Choose a set: ", get_unique_sets(), key="tab3")
            set_flashcards = flashcards[flashcards['Set Name'] == set_choice]
            if not set_flashcards.empty:
                questions = set_flashcards['Question'].values
                answers = set_flashcards['Answer'].values
                for i in range(len(questions)):
                    st.write(questions[i])
                    if st.button("Show Answer", key=f"button_{i}"):
                        st.subheader("Answer")
                        st.write(answers[i])
            else:
                st.info(f"No flashcards in the '{set_choice}' set. Add some flashcards to this set!")
        else:
            st.info("No flashcards available. Create some to start studying!")

if __name__ == '__main__':
    main()
