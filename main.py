from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from hf_lib.course_creator import YouTubeCourseCreator

app = FastAPI()


class Topic(BaseModel):
    topic: str
    no_of_subtopics: int


@app.post("/create_course/")
def create_course(topic: Topic):
    try:
        agent = YouTubeCourseCreator()
        return agent.recommend(topic.topic, topic.no_of_subtopics)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
