from urllib import response
import streamlit as st
import requests
from find_your_inner_gamer.gcp import get_data_from_gcp

url = 'https://find-your-inner-gamer-7oqykbx6lq-ew.a.run.app/predict'

@st.cache
def get_select_box_data():
    return get_data_from_gcp()

df = get_select_box_data()

game = st.selectbox('Select your favourite game', df['name'])

params = {
    'game': game
}

if st.button('Find Similar'):
    response = requests.get(url, params)
    pred = response.json()
    st.write(pred)
