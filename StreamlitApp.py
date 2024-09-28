
import streamlit as st
from PIL import Image
import numpy as np

def main():

    img_file_buffer = st.camera_input("Take a photo")

    if img_file_buffer is not None:

        img = Image.open(img_file_buffer)

        img_array = np.array(img)

        st.write(type(img_array))
        st.write(img_array.shape)


if __name__ == "__main__":
    main()