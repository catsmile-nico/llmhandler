# TODO: This file.. needs a better name or folder

import json
from dotenv import load_dotenv

from dataclasses import dataclass, field
from typing import TypedDict, List, Optional, Literal

import openai
from openai.openai_object import OpenAIObject

ROLES = Literal["system", "user", "function", "assistant"]

class FunctionCallDict(TypedDict):
    name: str
    arguments: dict

class MessageDict(TypedDict):
    role: ROLES
    content: Optional[str]
    name: Optional[str]
    function_call: Optional[FunctionCallDict]

@dataclass
class Message:
    role: ROLES
    content: str

    def raw(self) -> MessageDict:
        return {"role": self.role, "content": self.content}
    
@dataclass
class MessageDB:
    messages: List = field(default_factory=list)

    def add(self, msg: MessageDict):
        self.messages.append(msg)

    def dump(self) -> List:
        return self.messages
    
    # TODO: add dump human readable
    
    def raw(self) -> List:
        # Create a new list without the 'usage' key in each message
        return [{k: v for k, v in msg.items() if k != 'usage'} for msg in self.messages]

def create_chat_completion(
    messages: List[MessageDict]
    ,**kwargs
) -> OpenAIObject:

    """Calls chat completion from OpenAI API

    Args:
        messages: List of messages to send to the API
        kwargs: Other OpenAI API chat completion arguments
    Returns:
        OpenAIObject: Response from the API

    """
    return openai.ChatCompletion.create(
        messages=messages,
        **kwargs,
    )

def chat(
        message_history: MessageDB
        , model: str="gpt-3.5-turbo-0613"
        , functions: List=[]
        , callables: List=[]
        , persist: bool=True):
    
    # TODO: there's got to be a more elegant way for this
    if len(functions)>0:
        response = create_chat_completion(messages=message_history.raw(),model=model,functions=functions)
    else:
        response = create_chat_completion(messages=message_history.raw(),model=model)

    # Save response
    message = MessageDict(response.choices[0].message)
    message["usage"] = response.usage
    message_history.add(message)

    # Print response or execute function_call
    # TODO: a better way to limit it from indefinitely calling function_call
    if message.get("function_call") and persist:
        
        # TODO: there's got to be a more elegant way for this
        function = FunctionCallDict(message.get("function_call"))

        print("Assistant is calling function:", function)

        fuction_to_call = callables[function["name"]]
        # TODO: Add safety check that arguments have the right datatype
        function_response = fuction_to_call( # updated this method
                                **json.loads(function["arguments"])
                            )
        
        message_history.add(MessageDict({"role":"function","name":function["name"],"content":function_response}))

        chat(message_history=message_history, model=model, persist=False)

    else:
        print("Assistant response:", message.get("content"))


# region Fake chat
    # message = {"role":"assistant","content":"idk"}
    # message = {
    #     "role": "assistant",
    #     "content": None,
    #     "function_call": {
    #       "name": "timezone_difference",
    #       "arguments": "{\n  \"location_1\": \"Asia/Singapore\",\n  \"location_2\": \"Asia/Tokyo\"\n}"
    #     }
    # }
    # message["usage"] = {
    #     "prompt_tokens": 65,
    #     "completion_tokens": 19,
    #     "total_tokens": 84
    # }
# endregion

# region JSON Examples

    # Initial Message
    # {
    #     'role': 'system', 
    #     'content': "you are an expert in telling time"
    # }
    # {
    #     'role': 'user', 
    #     'content': "What's the time difference between Singapore and Tokyo"
    # }

    # Function Call Response
    # {
    #     "role": "assistant",
    #     "content": null,
    #     "function_call": {
    #         "name": "calculate_time_difference",
    #         "arguments": "{\n  \"location_1\": \"Asia/Singapore\",\n  \"location_2\": \"Asia/Tokyo\"\n}"
    # }

    # Function Call Message
    # {
    #     'role': 'function', 
    #     'name': 'calculate_time_difference', 
    #     'content': '1 hours, 0 minutes after'
    # }

    # Assistant Response
    # {
    #     "role": "assistant", 
    #     "content": "The time difference between Singapore and Tokyo is 1 hour, with Tokyo being ahead of Singapore."
    # }

    # Usage
    # {
    #     "prompt_tokens": 65,
    #     "completion_tokens": 19,
    #     "total_tokens": 84
    # }

# endregion