from typing import List, Set, Type

from pydantic import BaseModel, Field

from taitriscore.actions import Action
from taitriscore.utils.schema import Message


class Memory(BaseModel):
    storage: List[Message] = Field(default_factory=list)

    def add(self, message: Message):
        self.storage.append(message)

    def get(self) -> List[Message]:
        return self.storage

    def get_by_actions(self, actions: Set[Type[Action]]) -> List[Message]:
        if not actions:
            return []
        return [i for i in self.storage if i.cause_by in actions]

    def remember(self, messages: List[Message]) -> List[Message]:
        news = []
        for message in messages:
            if message not in self.storage:
                self.add(message)
                news.append(message)
        return news
