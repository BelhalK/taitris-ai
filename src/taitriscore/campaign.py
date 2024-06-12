import pdb

from pydantic import BaseModel, Field

from taitriscore.config import CONFIG
from taitriscore.environment import Environment
from taitriscore.logs import logger
from taitriscore.roles import Role
from taitriscore.utils.schema import Message


class Campaign(BaseModel):
    environment: Environment = Field(default_factory=Environment)
    company: str = Field(default="")
    objective: str = Field(default="")

    def hire(self, roles):
        self.environment.add_roles(roles=roles)

    def set_quota_seeding(self, quota_seeding):
        """
        Sets the maximum number of products seeding in the campaign.

        Args:
            quota_seeding (int): The maximum number of seedings allowed in the campaign.

        Returns:
            None
        """
        CONFIG.max_quota_seeding = quota_seeding
        logger.info(f"Quota Seeding: {quota_seeding}.")

    def budget(self, budget):
        """
        Sets the maximum budget for the campaign.

        Args:
            budget (int): The maximum budget for the campaign.

        Returns:
            None

        Raises:
            None
        """
        CONFIG.max_budget = budget
        logger.info(f"Budget: ${budget}.")

    def _check_balance(self):
        """
        Checks the balance of the campaign by comparing the total number of products to be seeded with the maximum quota allowed for seeding.

        Raises:
            ValueError: If the total number of products to be seeded exceeds the maximum quota allowed for seeding.

        Returns:
            None
        """
        if CONFIG.total_seeding > CONFIG.max_quota_seeding:
            raise f"No More products to place -> Nb of Products placed: {CONFIG.total_seedings}"

    def start_campaign(self, objective):
        self.objective = objective

    async def run(self, n_round=3):
        while n_round > 0:
            n_round -= 1
            logger.debug(f"{n_round}")
            self._check_balance()
            await self.environment.run()
        return self.environment.history
