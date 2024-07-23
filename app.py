import streamlit as st
from PIL import Image

from hf_lib.course_creator import YouTubeCourseCreator

st.set_page_config(
    page_title="YouTube Course Recommender",
    page_icon=Image.open('assets/favicon.png'),
    layout='wide',
    initial_sidebar_state='collapsed'
)

st.title('👋🏻Hello!')
query = st.text_input('Course Topic')
subtopics = st.number_input(
    'No. of subtopics', step=1, max_value=10, min_value=0)
create = st.button('Create Course')
if create:
    try:
        agent = YouTubeCourseCreator()
        st.session_state['User courses'] = {}
        st.session_state['User courses'][query] = agent.recommend(
            query, subtopics)
        st.json(st.session_state['User courses'][query])
    except Exception as e:
        st.exception(e)
