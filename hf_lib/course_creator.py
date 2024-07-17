import json
from hf_lib.client import HFClient
from hf_lib.messages import UserMessage
from hf_lib.search import ytsearch


class YouTubeCourseCreator:
    def __init__(self) -> None:
        self.schema = {
            "properties": {
                "search_queries": {"items": {"type": "string"}, "title": "Search Queries", "type": "array"},
                'subtopics': {"items": {"type": "string"}, "title": "Subtopics", "type": "array"},
            },
            "required": ['search_queries', 'subtopics'],
            "title": "Search Queries for Subtopics",
            "type": "object",
        }

        self.initial_prompt = '''
You are a expert YouTube Course Creator. 
Your job is to generate search queries that find user exactly the video they are looking for. 
You will be given a topic and you will have to generate a search query that will find the perfect YouTube video to learn from. 
The user tell you a topic they want to study and you bifurcate the topic into subtopics and generate a search query for each subtopic. 
You can understand the user and customise the output accordingly. 
You never Provide any additional commentary and strictly only provide the required response.
Think step by step always.
Bifurcate the main topic '{topic}' into {no_of_subtopics} subtopics that will make the main topic easier to learn. 
Generate ONE Youtube Search Query for each subtopic.
The output should be strictly in JSON format without any additional commentary. Please understand and use the following schema only: 

{schema}

DO NOT provide any additional commentary.
Think step by step and make sure the user can learn the main topic easily.'
'''

    def recommend(self, topic, no_of_subtopics):
        llm = HFClient(
            initial_message=UserMessage(content=self.initial_prompt.format(
                topic=topic, no_of_subtopics=no_of_subtopics, schema=self.schema)
            )
        )
        try:
            res = llm.conversation(output_parser=True)
            print(res['content'])
            queries = json.loads(res['content'])['search_queries']
            subtopics = json.loads(res['content'])['subtopics']
            print(queries, subtopics)
            course = {}
            for subtopic, query in zip(subtopics, queries):
                course[subtopic] = ytsearch(query)

            return course

        except Exception as e:
            print(e)
            llm.send_message(
                UserMessage(
                    f'The following error occured: {
                        e}. Please fix your response and try again.'
                )
            )
            # self.recommend(topic, subtopics)
