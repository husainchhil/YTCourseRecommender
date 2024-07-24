import json
from streamlit_card import card
import streamlit as st
from PIL import Image

from hf_lib.course_creator import YouTubeCourseCreator

st.set_page_config(
    page_title="YouTube Course Recommender",
    page_icon=Image.open('assets/favicon.png'),
    layout='wide',
    initial_sidebar_state='collapsed'
)

st.session_state['User courses'] = {}


def display_video(course_dict):
    for key in courses_dict.keys():
        st.write(f'### {key}')
        for i, video in enumerate(courses_dict[key]['videos']):
            vid = video['snippet']
            res = card(
                title=vid['title'],
                text=vid['channelTitle'],
                image=vid['thumbnails']['standard']['url'],
                url=f"https://www.youtube.com/watch?v={video['id']}",
                key=f"{key}_{i}",
                styles={
                    'card': {
                        'width': '560px',
                        'height': '360px',
                    },
                }
            )

st.title('👋🏻Hello!')
query = st.text_input('Course Topic')
subtopics = st.number_input(
    'No. of subtopics', step=1, max_value=10, min_value=0)
create = st.button('Create Course')
if create:
    try:
        agent = YouTubeCourseCreator()
        st.session_state['User courses'][query] = agent.recommend(
            query, subtopics)
        courses_dict = st.session_state['User courses'][query]
        display_video(courses_dict)
    except Exception as e:
        st.exception(e)
