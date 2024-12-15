import asyncio
import pdb
from typing import List

from pydantic import BaseModel, Field

from taitriscore.memory import Memory
from taitriscore.roles import Role
from taitriscore.utils.schema import Message
from taitriscore.logs import logger


class Environment(BaseModel):
    roles: List[Role] = Field(default_factory=list)
    memory: Memory = Field(default_factory=Memory)
    history: List = Field(default_factory=list)

    class Config:
        arbitrary_types_allowed = True

    def add_roles(self, roles):
        self.roles.extend(roles)

    def publish_message(self, message: Message):
        """Add a message to the environment's memory"""
        self.memory.add(message)
        self.history.append(message)

    async def run(self):
        for role in self.roles:
            todo = await role.run(self.memory)
            self.history.append(todo)
            if todo and hasattr(todo, 'content'):
                if isinstance(todo.content, dict) and 'choices' in todo.content:
                    # Extract just the message content from OpenAI response
                    content = todo.content['choices'][0]['message']['content']
                    logger.info(f"{role.__class__.__name__} response: {content}")
                else:
                    # For lead generator, only show the findings once
                    if isinstance(todo.content, str):
                        if '🔍 Lead Generator Findings:' in todo.content:
                            # Only show the findings, skip the response
                            continue
                        logger.info(f"{role.__class__.__name__} response: {todo.content}")

    def get_roles(self):
        return self.roles

    def get_role(self, name):
        return self.roles.get(name, None)
