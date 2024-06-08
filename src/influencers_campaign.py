import asyncio
import pdb

import fire

from taitriscore.campaign import Campaign
from taitriscore.logs import logger
from taitriscore.roles import LeadGenerator, Negotiator, OutreachSales


async def influencers_campaign(
    company: str,
    objective: str,
    n_round: int = 5,
    quota_seeding: int = 3,
    budget: float = 3.0,
    negotiate: bool = False,
):

    campaign = Campaign()

    logger.info("Hiring Lead Generator and Outreach Sales person.")
    campaign.hire([LeadGenerator(), OutreachSales()])

    if negotiate:
        logger.info("Hiring a Negotiator.")
        campaign.hire([Negotiator()])

    campaign.start_campaign(objective)
    campaign.set_quota_seeding(quota_seeding)

    await campaign.run(n_round=n_round)


def main(
    company: str,
    objective: str,
    n_round: int = 5,
    quota_seeding: int = 3,
    budget: float = 3.0,
    negotiate: bool = False,
):
    asyncio.run(
        influencers_campaign(
            company, objective, n_round, quota_seeding, budget, negotiate
        )
    )


if __name__ == "__main__":
    fire.Fire(main)

# python influencers_campaign.py --company Gardyn --objective test --quota_seeding 10 --budget 1000 --negotiate True
