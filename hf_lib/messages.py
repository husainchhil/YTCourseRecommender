from pydantic import BaseModel
from huggingface_hub import ChatCompletionOutput


class Message(BaseModel):
    """
    ### Create a message

    Args:
        role (str): The role of the message
        content (str): The content of the message

    Returns:
        dict: The message
    """
    def __new__(cls, role: str, content: str):
        """
        Create a new message
        """
        return {
            'role': role,
            'content': content
        }


class UserMessage(Message):
    """
    ### Create a user message

    Args:
        content (str): The content of the message

    Returns:
        dict: The user message
    """
    def __new__(cls, content: str):
        """
        Create a new user message
        """
        return {
            'role': 'user',
            'content': content
        }


class SystemMessage(BaseModel):
    """
    ### Create a system message

    Args:
        content (str): The content of the message

    Returns:
        dict: The system message
    """
    def __new__(cls, content: str):
        """
        Create a new system message
        """
        return {
            'role': 'system',
            'content': content
        }


class AIMessage(BaseModel):
    """
    ### Create a assistant message

    Args:
        content (str): The content of the message

    Returns:
        dict: The assistant message
    """
    def __new__(cls, content: str):
        """
        Create a new assistant message
        """
        return {
            'role': 'assistant',
            'content': content
        }


def OutputParser(response: ChatCompletionOutput):
    """
    ### Parse the output

    Args:
        response (ChatCompletionResponse): The response from the model

    Returns:
        dict: The parsed output
    """
    return {
        'role': response.choices[0].message.role,
        'content': response.choices[0].message.content
    }
