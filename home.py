import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
import streamlit as st
from PIL import Image, ImageDraw, ImageGrab
import numpy as np
from supabase import create_client, Client

def init_connection():
    url = st.secrets['SUPABASE_URL']
    key = st.secrets['SUPABASE_KEY']
    return create_client(url, key)

supabase = init_connection()

def sign_in(email, password):
    try:
        session = supabase.auth.sign_in_with_password({"email" : email, "password" : password})
        st.session_state['supabase_session'] = session
        st.success("Signed in successfully")
        return session
    except Exception as e:
        st.write(f"Authentication failed {e}")

def sign_up(email, password): # ! FIX SIGNUP
    user = supabase.auth.sign_up({"email":"hual.Alexander@gmail.com","password":password})



def check_session():
    if 'supabase_session' in st.session_state:
            return True
    else:
        return False
    
def show_user_info():
     session = st.session_state['supabase_session']
     st.write(f'Hello 👋')

def get_user_id():
    session = st.session_state['supabase_session']
    return session.user.user_metadata['sub']


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

    with col1:
        create_card("Smart Scanning", "Digitize your notes with OCR", "📷")
    with col2:
        create_card("Flashcard Creator", "Create digital flashcards from physical notes", "🗂️")  

def main_components():

    if not check_session():

        with st.form(key = 'login_form'):
            email = st.text_input("Email")
            password = st.text_input("Password", type = "password")
            submit_button = st.form_submit_button(label = "Sign In")
            sign_up_button = st.form_submit_button(label = "Sign up")

        if submit_button:
            session = sign_in(email, password)
            if session:
                st.success("You can now visit any page!")
            else:
                st.error("Sign in failed")
        
        if sign_up_button:
            session = sign_up(email, password)
            if session:
                st.success("You made an account!")
            else:
                st.error("Sign up failed")
                
    st.title("Student Hub")    

    st.subheader("Your one-stop solution for bridging digital and physical learning")
    menu = ["home","Academics","Personal"]
    choice = st.sidebar.selectbox("What do you need today?",menu)
    if choice == "home":
        st.write("Welcome to the Student Hub!")
    elif choice == "Academics":
        academics()



if __name__ == "__main__":
    main_components()
