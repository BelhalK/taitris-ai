import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import asyncio
import fire

from taitriscore.memory.memory import Memory
from taitriscore.logs import logger
from taitriscore.roles import Planner


async def create_plan(objective: str):
    role = Planner(profile="Planner", objective = objective)
    final_list = await role.generate_tasks_list(objective)
    logger.info(final_list)
    

def main(objective):
    # Wrap the asyncio call in a synchronous function
    return asyncio.run(create_plan(objective))

if __name__ == "__main__":
    fire.Fire(main)
