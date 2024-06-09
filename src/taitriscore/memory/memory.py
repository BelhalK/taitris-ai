from collections import defaultdict
from typing import Type

from taitriscore.actions import Action
from taitriscore.utils.schema import Message


class Memory:
    def __init__(self):
        """Initialize an empty storage list and an empty index dictionary"""
        self.storage: list[Message] = []
        self.index: dict[Type[Action], list[Message]] = defaultdict(list)

    def add(self, message):
        """Add a new message to storage, while updating the index"""
        if message in self.storage:
            return
        self.storage.append(message)
        if message.cause_by:
            self.index[message.cause_by].append(message)

    def add_batch(self, messages):
        for message in messages:
            self.add(message)

    def get_by_role(self, role):
        """Return all messages of a specified role"""
        return [message for message in self.storage if message.role == role]

    def get_by_content(self, content):
        """Return all messages containing a specified content"""
        return [message for message in self.storage if content in message.content]

    def delete(self, message):
        """Delete the specified message from storage, while updating the index"""
        self.storage.remove(message)
        if message.cause_by and message in self.index[message.cause_by]:
            self.index[message.cause_by].remove(message)

    def clear(self):
        """Clear storage and index"""
        self.storage = []
        self.index = defaultdict(list)

    def count(self):
        """Return the number of messages in storage"""
        return len(self.storage)

    def try_remember(self, keyword):
        """Try to recall all messages containing a specified keyword"""
        return [message for message in self.storage if keyword in message.content]

    def get(self, k=0):
        """Return the most recent k memories, return all when k=0"""
        return self.storage[-k:]

    def remember(self, observed, k=0):
        """remember the most recent k memories from observed Messages, return all when k=0"""
        already_observed = self.get(k)
        news: list[Message] = []
        for i in observed:
            if i in already_observed:
                continue
            news.append(i)
        return news

    def get_by_action(self, action):
        """Return all messages triggered by a specified Action"""
        return self.index[action]

    def get_by_actions(self, actions):
        """Return all messages triggered by specified Actions"""
        rsp = []
        for action in actions:
            if action not in self.index:
                continue
            rsp += self.index[action]
        return rsp
