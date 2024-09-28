import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
import streamlit as st
from PIL import Image, ImageDraw, ImageGrab
import numpy as np


def take_photo():
    img_file_buffer = st.camera_input("Take a photo")


    if img_file_buffer is not None:
        img = Image.open(img_file_buffer)
        # img = img.convert('RBGA')
        # rectangles = [
        #     ((10, 10), (50, 50)),  # rectangle 1
        #     ((100, 100), (150, 150)),  # rectangle 2
        #     ((200, 200), (250, 250))  # rectangle 3
        # ]

        # draw = ImageDraw.Draw(img)


        # for rect in rectangles:
        #     x1, y1 = rect[0]
        #     w, h = rect[1]
        #     draw.rectangle((x1, y1, x1+w, y1+h), outline='red', width=2)

        # print(type(img))

        st.image(img)

        img_array = np.array(img)

        st.write(type(img_array))
        st.write(img_array.shape)
        img.save("im.jpg")

def create_card(title, description, icon):
    card_html = f"""
    <div style="padding: 20px; border-radius: 10px; background-color: #f0f2f6; margin-bottom: 20px;">
        <h3>{title} {icon}</h3>
        <p>{description}</p>
    </div>
    """
    return components.html(card_html, height=150)
def academics():
    col1, col2 = st.columns(2)

    st.title("Time to lock in buddy")
    with col1:
        create_card("Smart Scanning", "Digitize your notes with OCR", "📷")
    with col2:
        create_card("Flashcard Creator", "Create digital flashcards from physical notes", "🗂️")  

def personal():
    st.title("Ommmm")
def main_components():
    st.title("Student Hub")    

    st.subheader("Your one-stop solution for bridging digital and physical learning")
    menu = ["Home","Academics","Personal"]
    choice = st.sidebar.selectbox("What do you need today?",menu)
    if choice == "Home":
        st.write("Welcome to the Student Hub!")
    elif choice == "Academics":
        academics()
    else:
        personal()



if __name__ == "__main__":
    main_components()
