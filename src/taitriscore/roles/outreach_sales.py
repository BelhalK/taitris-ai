from taitriscore.actions import EmailOutreach
from taitriscore.roles import Role


class OutreachSales(Role):
    def __init__(
        self,
        name="Adam",
        profile="Sales Rep. Outreach to prospects.",
        desc="I am a sales representative responsible for reaching out to potential influencers "
        "and establishing initial contact. I craft personalized outreach messages and manage "
        "the communication process.",
    ):
        super().__init__(name, profile, desc=desc)
        self._init_actions([EmailOutreach()])
