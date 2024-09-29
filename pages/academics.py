import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_card import card
from st_clickable_images import clickable_images
from frontend import check_session

if not check_session():
    st.switch_page('frontend.py')
# Set page config
st.set_page_config(page_title="Academics", page_icon="🖊️", layout="wide")
 
def academics():
    st.subheader("Academics")
    #st.subheader(student_hub_structure['Academics']['Description'])
    col1,col2 = st.columns(2) 
    #for feature in student_hub_structure['Academics']['Features']:
    images = ["https://s3.amazonaws.com/pix.iemoji.com/images/emoji/apple/ios-12/256/left-pointing-magnifying-glass.png",
            "https://static.vecteezy.com/system/resources/previews/011/670/697/original/flash-card-flat-icon-free-vector.jpg",
            "https://cdn.vectorstock.com/i/500p/14/65/growth-progress-arrow-vector-49461465.jpg"
            ]
    #content = [document_scanner,
     #flashcards(),
    #    "Progress Tracker"] 
    #clicked = clickable_images(
     #       images,
     #       titles=[f"Image {i+1}" for i in range(len(images))],
     #       div_style={"display": "flex", "justify-content": "space-evenly", "flex-wrap": "wrap"},
     #       img_style={"margin": "5px", "height": "200px"}
     #   )
    #if clicked > -1:
    #    content[clicked]()
    #else:
    #    st.markdown("**Click an image to view its content!")
    #uploaded_file = st.file_uploader("Upload your notes", type=["jpg", "png", "pdf"])
    #if uploaded_file is not None:
    #    st.success("File successfully uploaded!")
    #    if st.button("Start Scanning"):
    #        st.write("Scanning initiated...")


academics() 
st.markdown("---")
st.markdown("GAAT: Greatest App of All Time")
