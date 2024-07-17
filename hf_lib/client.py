import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient
from typing import Union
from hf_lib.messages import Message, UserMessage, SystemMessage, AIMessage, OutputParser

MessageFormat = Union[Message, UserMessage, SystemMessage, AIMessage]


class HFClient:

    def __init__(self, hf_token: str = None, initial_message: Union[MessageFormat, None] = None, **model_kwargs):
        load_dotenv()
        self.__client = InferenceClient(
            "mistralai/Mixtral-8x7B-Instruct-v0.1",
            token=hf_token if hf_token else os.environ['HF_KEY'], **model_kwargs)

        self.messages = [initial_message] if initial_message else []
        self.prompt_templates = {}

    def send_message(self, message: MessageFormat):
        self.messages.append(message)

    def conversation(self, output_parser=None, **model_kwargs):

        response = self.__client.chat_completion(
            messages=self.messages,
            max_tokens=1000,
            **model_kwargs
        )
        self.messages.append(
            {
                'role': response.choices[0].message.role,
                'content': response.choices[0].message.content
            }
        )
        if output_parser:
            return OutputParser(response)
        return response

    def text_gen(self, prompt: MessageFormat, output_parser=None, **model_kwargs):

        response = self.__client.chat_completion(
            messages=[prompt],
            max_tokens=1000,
            **model_kwargs
        )
        if output_parser:
            return OutputParser(response)
        return response

    def add_prompt_template(self, name: str, template: Message):
        self.prompt_templates[name] = template
