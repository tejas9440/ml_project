import streamlit as st
import pandas as pd

file_path = './popular.pkl'
data = pd.read_pickle(file_path)

# Display the data
st.title('Popular Data Viewer')
st.write(data)
st.write("ended")