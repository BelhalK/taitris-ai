import asyncio
import pdb

from taitriscore.logs import logger
from taitriscore.memory.memory import Memory
from taitriscore.roles import LeadGenerator


async def search():
    # store = FaissStore(DATA_PATH / 'example.json')
    # role = LeadGenerator(profile="LeadGenerator", store = store)

    role = LeadGenerator(profile="LeadGenerator")

    queries = [
        """I am preparing an influencers marketing campaign for Gardyn. Can you look on Google what they do?.
        Once you did so, please suggest some names of specific influencers or content creators who might be a good fit for the Gardyn campaign. We target Instagram. And influencers in the healthy food space with a moderate number of followers.
        """,
        "Is @freshfoods good to use?",
        "What content should you send to the influencer?",
    ]

    # queries = ['I am preparing an influencers marketing campaign for Gardyn. Can you look on Google what they do? Once you did so, please suggest some names of specific influencers or content creators who might be a good fit for the Gardyn campaign. We target Instagram. And influencers in the healthy food space with a moderate number of followers.']

    for query in queries:
        logger.info(f"User: {query}")
        result = await role.run(query)
        logger.info(result)


if __name__ == "__main__":
    asyncio.run(search())
