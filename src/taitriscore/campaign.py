import pdb
import asyncio

from pydantic import BaseModel, Field

from taitriscore.config import CONFIG
from taitriscore.environment import Environment
from taitriscore.logs import logger
from taitriscore.roles import Role
from taitriscore.roles.lead_generator import LeadGenerator
from taitriscore.utils.schema import Message


class Campaign(BaseModel):
    environment: Environment = Field(default_factory=Environment)
    company: str = Field(default="")
    objective: str = Field(default="")

    def __init__(self, **data):
        super().__init__(**data)
        self.environment = Environment()
        self.company = ""
        self.objective = ""

    def hire(self, roles):
        # Make sure we have an initial message in memory
        if not self.environment.memory.storage:
            initial_message = Message(
                content=f"Starting the campaign",
                role="system"
            )
            self.environment.memory.add(initial_message)
        
        # Add roles in sequence - Lead Generator first, then others
        lead_generator = None
        other_roles = []
        
        for role in roles:
            if isinstance(role, LeadGenerator):
                lead_generator = role
            else:
                other_roles.append(role)
        
        # Set goals and add roles in correct order
        if lead_generator:
            lead_generator._setting.goal = self.objective
            lead_generator.set_env(self.environment)  # Set environment for lead generator
            self.environment.add_roles([lead_generator])
        
        for role in other_roles:
            role._setting.goal = self.objective
            role.set_env(self.environment)  # Set environment for each role
            self.environment.add_roles([role])

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
        # Update existing roles with the objective
        for role in self.environment.roles:
            role._setting.goal = objective
        
        # Update the initial message with the objective
        initial_message = Message(
            content=f"Starting campaign with objective: {objective}",
            role="system"
        )
        self.environment.memory.add(initial_message)

    async def run(self, n_round=3):
        while n_round > 0:
            n_round -= 1
            logger.debug(f"{n_round}")
            self._check_balance()
            
            # Run lead generator first and ensure its message is stored
            for role in self.environment.roles:
                if isinstance(role, LeadGenerator):
                    lead_message = await role.run(self.environment.memory)
                    if lead_message:
                        logger.debug(f"Storing lead message - Role: {lead_message.role}, Type: {type(lead_message)}")
                        self.environment.memory.storage.append(lead_message)  # Add directly to storage
                    await asyncio.sleep(0.1)
            
            # Debug print memory contents
            logger.debug(f"Memory contents before OutreachSales:")
            for msg in self.environment.memory.storage:
                logger.debug(f"  - Message Role: {msg.role}, Type: {type(msg)}")
                if isinstance(msg.content, str) and "Lead Generator" in str(msg.role):
                    logger.debug(f"  - Content preview: {msg.content[:100]}")
            
            # Then run other roles with the updated memory
            for role in self.environment.roles:
                if not isinstance(role, LeadGenerator):
                    await role.run(self.environment.memory)

        return self.environment.history
