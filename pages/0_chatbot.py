import streamlit as st
from PIL import Image
import rag as rag_utils

IMAGE_ADDRESS = "https://cdn.shopify.com/s/files/1/0552/3269/2430/articles/learning-electronics-comprehensive-guide-for-beginners.webp?v=1702560862"
IMAGE_NAME = "uploaded_image.png"
QUERY = "Could you please provide more information about the following chip type {chip}"

# main web comps
# title
st.title("Circuit Analyzer")
# image
st.image(IMAGE_ADDRESS, caption = "Circuit Master")

# Upload image
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file:
    # open the image
    image = Image.open(uploaded_file)

    # display the image
    st.header("Uploaded Image")
    st.image(image, caption='Uploaded Image.', use_column_width=True)

    # save the image as a PNG file
    image.save(IMAGE_NAME)

    # analyse the image
    with st.spinner("Classifying the chip type......"):
        get_chip_type = rag_utils.call_vision_api(IMAGE_NAME)
        st.toast('Chip Classification Successful!', icon='✅')

    if not get_chip_type:
        st.error("Cannot Interpret the Image", icon = "❌")
        st.stop()

    # set the chip type
    st.subheader("Identified Chip Type: {}".format(get_chip_type))
    with st.spinner("Getting More Information"):
        get_info = rag_utils.generate_answer(QUERY.format(**{"chip":get_chip_type}))
        st.toast('Information Fetching Successful!', icon='✅')
        with st.sidebar:
            st.header("Chip Information")
            st.subheader("Uploaded Images")
            st.image(image, caption='Uploaded Image.', use_column_width=True)
            st.subheader("Chip Type")
            st.markdown(f"Chip Type: :red[{get_chip_type}]")
            st.subheader("More Information of the Chip")
            st.write(get_info)
