from __future__ import annotations

from dataclasses import dataclass, field

from pydantic import BaseModel
from typing_extensions import Type, TypedDict

from taitriscore.logs import logger

# TypedDict for raw message structure
class RawMessage(TypedDict):
    content: str
    role: str

# Dataclass for representing a message
@dataclass
class Message:
    content: str
    instruct_content: BaseModel = field(default=None)
    role: str = field(default="user")  # Roles can be system, user, or assistant
    cause_by: Type["Action"] = field(default="")
    sent_from: str = field(default="")
    send_to: str = field(default="")

    def __str__(self):
        return f"{self.role}: {self.content}"

    def __repr__(self):
        return self.__str__()

    def to_dict(self):
        """
        Converts the Message instance to a dictionary.
        """
        return {"role": self.role, "content": self.content}

# Subclass of Message specifically for user messages
@dataclass
class UserMessage(Message):
    def __init__(self, content: str):
        super().__init__(content, role="user")

# Subclass of Message specifically for system messages
@dataclass
class SystemMessage(Message):
    def __init__(self, content: str):
        super().__init__(content, role="system")

# Subclass of Message specifically for assistant (AI) messages
@dataclass
class AIMessage(Message):
    def __init__(self, content: str):
        super().__init__(content, role="assistant")

if __name__ == "__main__":
    test_content = "test_message"
    msgs = [
        UserMessage(test_content),
        SystemMessage(test_content),
        AIMessage(test_content),
        Message(test_content, role="QA"),  # Example message with a custom role
    ]
    logger.info(msgs)  # Logs the list of message instances