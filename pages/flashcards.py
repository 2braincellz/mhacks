#from OCRget import * as OCRget
#from reading_image import * as reading_image
import streamlit as st
import os
import groq
from frontend import check_session

if not check_session():
    st.switch_page('frontend.py')
    
client = groq.Client(api_key=os.environ["GROQ_API_KEY"])

st.title("Flashcards")
 

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


def main():
    #text is a string
    #text = OCRget.detect_text()

    #clean up text
    #cleaned_text = reading_image.model(text)
    notes = """
The water cycle, also known as the hydrologic cycle, describes the continuous movement of water within the Earth and atmosphere.
It involves processes such as evaporation, condensation, precipitation, and runoff.
The sun drives the water cycle by heating water in oceans and on land, causing evaporation.
Water vapor rises into the atmosphere, cools, and forms clouds through condensation.
Precipitation occurs when water droplets in clouds become heavy enough to fall as rain or snow.
"""
    flashcards = create_flashcards(notes)
    print(flashcards)


if __name__ == '__main__':
    main()
