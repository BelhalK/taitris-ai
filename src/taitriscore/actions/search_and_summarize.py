from taitriscore.actions import Action
from taitriscore.config import CONFIG
from taitriscore.logs import logger
from taitriscore.tools.search_engine import SearchEngine
from taitriscore.utils.schema import Message

SEARCH_AND_SUMMARIZE_PROMPT = """
### Reference Information
{CONTEXT}

### Dialogue History
{QUERY_HISTORY}
{QUERY}

### Current Question
{QUERY}

### Current Reply: Based on the information, please write the reply to the Question
"""

SEARCH_AND_SUMMARIZE_LEADGEN_SYSTEM = """## Requirements
1. Please summarize the latest dialogue based on the reference information (secondary) and dialogue history (primary). Do not include text that is irrelevant to the conversation.
- The context is for reference only. If it is irrelevant to the user's search request history, please reduce its reference and usage.
2. If there are citable links in the context, annotate them in the main text in the format [main text](citation link). If there are none in the context, do not write links.
3. The reply should be graceful, clear, non-repetitive, smoothly written, and of moderate length, in Simplified English.

# Example
## Reference Information
...

## Dialogue History
user: I am preparing an influencers marketing campaign for Gardyn. Can you look on Google what they do?
Leadgenerator: Of course! Using Google, I found that Gardyn is a company that specializes in creating personalized gardening kits for homeowners. They offer a variety of kits that include everything needed to grow a specific type of plant, such as herbs, vegetables, or flowers.
user: please suggest some names of specific influencers or content creators who might be a good fit for the Gardyn campaign. We target Instagram. And influencers in the healthy food space with a moderate number of followers.
> Leadgenerator: ..

## Ideal Answer
Of course! Here are some suggestions for influencers or content creators in the healthy food space who may be a good fit for your Gardyn campaign on Instagram:
1. @EatYourVeggies - This account has a moderate number of followers and focuses on promoting healthy eating habits through fun and creative recipes.
2. @FreshFoodFrenzy - This account showcases delicious and nutritious recipes that cater to a variety of dietary needs and preferences.
3. @NourishedLife - This account provides healthy living tips and inspiration, including recipes, workouts, and mindfulness practices.
"""

SEARCH_AND_SUMMARIZE_LEADGEN_SYSTEM_EN_US = SEARCH_AND_SUMMARIZE_LEADGEN_SYSTEM.format(
    LANG="en-us"
)


class SearchAndSummarize(Action):
    def __init__(self, name="", context=None, llm=None, engine=None, search_func=None):
        self.config = CONFIG
        self.engine = engine
        self.search_engine = SearchEngine(self.engine, run_func=search_func)
        self.result = ""
        super().__init__(name, context, llm)

    async def run(self, context, system_text=SEARCH_AND_SUMMARIZE_LEADGEN_SYSTEM_EN_US):
        no_serpapi = (
            not self.config.serpapi_api_key
            or "YOUR_API_KEY" == self.config.serpapi_api_key
        )

        if no_serpapi and no_google and no_serper:
            logger.warning(
                "Configure one of SERPAPI_API_KEY, SERPER_API_KEY, GOOGLE_API_KEY to unlock full feature"
            )
            return ""
        query = context[-1].content
        # logger.debug(query)

        rsp = await self.search_engine.run(query)
        self.result = rsp
        if not rsp:
            logger.error("empty rsp...")
            return ""
        # logger.info(rsp)

        system_prompt = [system_text]
        prompt = SEARCH_AND_SUMMARIZE_PROMPT.format(
            # PREFIX = self.prefix,
            ROLE=self.profile,
            CONTEXT=rsp,
            QUERY_HISTORY="\n".join([str(i) for i in context[:-1]]),
            QUERY=str(context[-1]),
        )
        result = await self._aask(prompt, system_prompt)
        logger.debug(prompt)
        logger.debug(result)
        return result
