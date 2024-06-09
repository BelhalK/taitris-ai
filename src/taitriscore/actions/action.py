from abc import ABC, abstractmethod
from typing import Optional

from taitriscore.llm import LLM
from taitriscore.logs import logger

class Action(ABC):
    """Abstract base class for actions."""

    def __init__(self, name: str = "", context: Optional[dict] = None, llm: Optional[LLM] = None):
        """
        Initialize an Action instance.

        Args:
            name (str): The name of the action.
            context (Optional[dict]): Optional context for the action.
            llm (Optional[LLM]): An instance of the LLM class. If None, a new LLM instance is created.
        """
        self.name: str = name
        self.context: Optional[dict] = context
        self.llm: LLM = llm if llm is not None else LLM()
        self.prefix: str = ""
        self.profile: str = ""
        self.desc: str = ""
        self.content: str = ""
        self.instruct_content: Optional[str] = None

    def __str__(self) -> str:
        """Return the class name as the string representation of the instance."""
        return self.__class__.__name__

    def __repr__(self) -> str:
        """Return the string representation of the instance."""
        return self.__str__()

    async def _aask(self, prompt: str, system_msgs: Optional[list] = None) -> str:
        """
        Asynchronously ask the LLM with the given prompt and system messages.

        Args:
            prompt (str): The prompt to ask.
            system_msgs (Optional[list]): Optional list of system messages. The prefix is appended to this list.

        Returns:
            str: The response from the LLM.
        """
        if system_msgs is None:
            system_msgs = []
        system_msgs.append(self.prefix)
        return await self.llm.aask(prompt, system_msgs)

    @abstractmethod
    async def run(self, *args, **kwargs):
        """Abstract method to be implemented in subclasses to execute the action."""
        raise NotImplementedError("The run method should be implemented in a subclass.")