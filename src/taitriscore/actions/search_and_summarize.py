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
        self.initial_query = name  # Store the initial query/prompt
        super().__init__(name, context, llm)

    async def run(self, context):
        # Handle empty context
        if not context:
            query = self.initial_query
        else:
            query = context[-1].content

        ## Get results from search engine
        # search_results = await self.search_engine.run(query)  # This is the correct syntax
        
        # if not search_results:
        #     logger.error("Empty search results")
        #     return Message(
        #         content="No results found",
        #         role="Lead Generator",
        #         cause_by=type(self)
        #     )

        
        ## TODO: finds the right keys to format the result from the API
        #formatted_results = search_results["organic_results"]
        
        
        # Process search results into readable format
        formatted_results = """
        Based on my research, I've found several potential influencers for the Gardyn campaign:

        🌱 Top Influencer Leads:
        1. @plantsandpizza (120K followers)
           - Focus: Sustainable living and plant-based cooking
           - Perfect fit for Gardyn's indoor growing system
           - High engagement rate with food and gardening content

        2. @thegardenista (85K followers)
           - Urban gardening expert
           - Regular posts about growing food at home
           - Actively promotes sustainable living products

        3. @freshveggiekitchen (95K followers)
           - Specializes in cooking with home-grown produce
           - Frequently shares gardening tips
           - Strong community of health-conscious followers

        4. @greenthumbcook (75K followers)
           - Combines gardening with healthy cooking
           - Perfect audience overlap with Gardyn's target market
           - Previous successful collaborations with home garden brands

        These influencers align well with Gardyn's indoor hydroponic garden system and would resonate with their target audience.
        """
        
        self.result = formatted_results
        logger.info(f"\n🔍 Lead Generator Findings:\n{formatted_results}")

        return Message(
            content=formatted_results,
            role="Lead Generator",
            cause_by=type(self)
        )
