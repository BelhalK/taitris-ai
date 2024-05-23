from taitriscore.actions import Action
from taitriscore.config import CONFIG
from taitriscore.logs import logger
from taitriscore.utils.schema import Message

PLANNER_BASE_SYSTEM = """You are an AI super marketing campaign planner. Your sole purpose is to create a list of \
tasks to achieve the objective {objective}."""

CREATE_TASK = """### 
### Requirements
Depending on what is asked of you, you will either:

- Execute a task
- Create a new task
- Prioritize a list of unranked tasks

All of this is to complete the objective and design the perfect list of tasks to launch this influencer marketing campaign.
"""

class CreateTaskList(Action):
    """Action class to generate a list of tasks for a marketing campaign."""

    def __init__(self, objective, *args, **kwargs):
        self.objective = objective
        super().__init__(*args, **kwargs)

    async def run(
        self,
        topic: str,
        system_text: str = PLANNER_BASE_SYSTEM,
    ) -> str:
        prompt = CREATE_TASK.format(topic=topic)
        logger.debug(prompt)
        system_text = PLANNER_BASE_SYSTEM.format(objective=self.objective)
        self.llm.auto_max_tokens = True
        return await self._aask(prompt, [system_text])