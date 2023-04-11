import streamlit as st
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np

st.set_page_config(page_title='Plot Digitizer', page_icon=':pencil2:')

st.title('Plot Digitizer')

uploaded_file = st.file_uploader('Upload an image of the plot', type=['jpg', 'jpeg', 'png'])
if uploaded_file is not None:
    # Convert uploaded file to PIL Image
    img = Image.open(uploaded_file)

    # Display uploaded image
    st.subheader('Uploaded Image')
    st.image(img, caption='Uploaded Image', use_column_width=True)

    # Allow user to specify the axis limits
    x_min, x_max = st.slider('X-Axis Limits', 0, img.width, (0, img.width))
    y_min, y_max = st.slider('Y-Axis Limits', 0, img.height, (0, img.height))

    # Extract the data from the selected region of the image
    img_data = np.array(img.crop((x_min, y_min, x_max, y_max)).convert('L'))

    # Display the extracted data
    st.subheader('Extracted Data')
    fig, ax = plt.subplots()
    ax.imshow(img_data, cmap='gray')
    st.pyplot(fig)

    # Allow user to download the extracted data as a CSV file
    st.subheader('Download CSV')
    if st.button('Download CSV'):
        data = []
        for i in range(img_data.shape[1]):
            row = [float(img_data[j][i]) for j in range(img_data.shape[0])]
            data.append(row)
        np.savetxt('data.csv', np.array(data), delimiter=',')
        st.download_button(label='Download', data='data.csv', file_name='data.csv', mime='text/csv')
