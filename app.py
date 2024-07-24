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


def display_video(courses_dict):
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
                        'width': vid['thumbnails']['standard']['width'],
                        'height': vid['thumbnails']['standard']['height'],
                        'margin': '5px',
                    },
                }
            )
    st.download_button(
        label="Download",
        data=json.dumps(courses_dict),
        file_name=f"course_{query}.json",)


st.title('YouTube Course Recommender')
st.write('This app recommends a YouTube course based on the topic and number of subtopics you provide.')
cols = st.columns([4, 1])
with cols[0]:
    query = st.text_input(
        'Course Topic', placeholder='Enter the topic for the course', label_visibility='hidden')
with cols[1]:
    subtopics = st.number_input(
        'No. of subtopics', step=1, max_value=10, min_value=0, help='Enter the number of subtopics',)
create = st.button('Create Course')
if create:
    try:
        agent = YouTubeCourseCreator()
        st.session_state['User courses'][query] = agent.recommend(
            query, subtopics)
        courses_dict = st.session_state['User courses'][query]
        # with open('rm.json', encoding='utf-8') as f:
        #     courses_dict = json.load(f)
        display_video(courses_dict)
    except Exception as e:
        st.error(e, icon='⚠️')
