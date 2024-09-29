#import streamlit as st
import streamlit as st
from frontend import check_session, get_user_id, show_user_info
import base64
from frontend import supabase
from PIL import Image
from OCRget import readImage

if not check_session():
    st.switch_page('frontend.py')

st.set_page_config(page_title="journal")


if st.button("Start Scanning"):
    st.write("Scanning initiated...")

# uploaded_file = st.file_uploader("Upload your notes", type=["jpg", "png", "pdf"])
# if uploaded_file is not None:
#     st.success("File successfully uploaded!")



def save_image(image_file):

    user_id = get_user_id()

    name = image_file.name
    bytes_data = image_file.getvalue()
    base64_image = base64.b64encode(bytes_data).decode('utf-8')
    supabase.table('Image_files').insert({"user_id":user_id, "file_name" : name, "file" : base64_image}).execute()

    im = Image.open(image_file)
    im.save(f'{name}')

    im2 = Image.open(name)
    st.image(im2)



    readImage(name)
    st.write("Savedd!")


    st.download_button(label = "Download txt", file_name = 'rawtext.txt')





    

def upload_file():

    try:
        img_buffer = st.file_uploader("Upload an Image file", type = ['jpg', 'png'])
        if img_buffer:
            st.write(img_buffer.name)
            img = Image.open(img_buffer)
            st.image(img)
            return img_buffer

    except Exception as e:
        str.error("Unable to Upload file")
        st.write(e) 
        return


def tools():

    show_user_info()
    img= upload_file()

    if st.button("Save Image"):
        save_image(img)

    if st.button("See Past Images"):
        st.switch_page("pages/saved_images.py")

tools()
