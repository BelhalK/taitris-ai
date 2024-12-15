from taitriscore.actions import SearchAndSummarize
from taitriscore.roles import Role
from taitriscore.tools import SearchEngineType


class LeadGenerator(Role):
    def __init__(
        self,
        name="Adam",
        profile="Lead generator. Influencers finder",
        desc="I am a lead generator for your influencers marketing campaign. My name is Adam. I"
        "will find several influencers profile on Instagram based on what I find using Google Search."
        " I will always give you names of influencers but if you don't like them I will find some more."
        "My answers will be given strictly in bullet points where each bullet point corresponds to"
        "the username of the influencer, a sentence describing their work and the number of followers they have.",
        store=None,
    ):
        super().__init__(name, profile, desc=desc)
        self._set_store(store)

    def _set_store(self, store):
        prompt = f"Find influencers for {self._setting.goal}"
        if store:
            action = SearchAndSummarize(
                prompt,
                engine=SearchEngineType.SERPAPI_GOOGLE,
                search_func=store.search
            )
        else:
            action = SearchAndSummarize(
                prompt,
                engine=SearchEngineType.SERPAPI_GOOGLE
            )
        self._init_actions([action])
