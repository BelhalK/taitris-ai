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

    async def run(self):
        for role in self.roles:
            todo = await role.run(self.memory)
            self.history.append(todo)
            if todo and "result" in todo:
                if isinstance(todo["result"], dict) and "choices" in todo["result"]:
                    content = todo["result"]["choices"][0]["message"]["content"]
                    logger.info(f"{role.__class__.__name__} response: {content}")
                else:
                    logger.info(f"{role.__class__.__name__} response: {todo['result']}")

    def get_roles(self):
        return self.roles

    def get_role(self, name):
        return self.roles.get(name, None)
