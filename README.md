[![X (formerly Twitter)](https://img.shields.io/twitter/follow/BelhalK?style=social)](https://twitter.com/BelhalK)
[![GitHub](https://img.shields.io/github/followers/BelhalK?label=Follow&style=social)](https://github.com/BelhalK)

# Taitris: Influencer Marketing Campaign Automation

Taitris is a fully automated and agentic framework specifically designed to streamline and enhance your influencer marketing campaigns. It utilizes state-of-the-art language models including OpenAI's GPT-3.5 Turbo, GPT-4, and a suite of open-source models such as Meta's LLaMA-3-8b-chat-hf, providing unparalleled capabilities in generating, managing, and optimizing influencer engagements.

With Taitris, you can automate your influencer marketing campaigns with precision and efficiency, allowing you to focus on strategy and growth while the system handles the intricate details of influencer engagements. Embrace Taitris and transform your approach to influencer marketing with cutting-edge AI technology.

# How to use Taitris


### Running Python code

You can run your first campaign script `influencers_campaign.py` by typing the following command:

```
python influencers_campaign.py --company name-of-the-company --objective test --quota_seeding 10 --budget 1000 --negotiate True
```

### LLMs supported

Taitris use the following closed and open source LLMs. Choices are made by the user in the `config.yaml` file. Several costs are to consider when making those choices.
* GPT-3.5 and GPT-4 (OpenAI)
* Llama3-8b and Llama2-7b 


# Features of Taitris
Taitris integrates various specialized AI agents that work in harmony to automate complex tasks within influencer marketing campaigns. The main agents include:

### LeadGenerator
The `LeadGenerator` agent utilizes advanced AI algorithms to identify potential influencers who align with your brand's values and campaign goals. By analyzing vast amounts of data across social platforms, this agent pinpoints influencers who have the reach, demographic engagement, and content style that best match your target audience. This ensures a high-potential starting point for campaign engagements.

### OutreachSales
Once potential leads are identified, the `OutreachSales` agent takes over to initiate contact. This agent is equipped with capabilities to craft personalized outreach messages that are both engaging and reflective of your brand’s voice. Using natural language processing models like GPT-3.5 Turbo and GPT-4, `OutreachSales` efficiently handles initial communications, setting the stage for fruitful collaborations.

### Negotiator
The `Negotiator` agent is designed to handle discussions regarding collaboration terms, including compensation, content expectations, and timelines. The `Negotiator` ensures that agreements are reached swiftly and efficiently, minimizing manual oversight and speeding up campaign launches.


# How Taitris Works
Taitris seamlessly integrates these agents into a cohesive system that synchronizes each step of the campaign process. From lead generation through to final negotiations, each agent communicates and shares relevant data to maintain consistency and optimize outcomes. This synchronization not only saves time but also enhances the effectiveness of your marketing efforts, ensuring that each influencer relationship is maximized for best results.

The use of advanced LLMs ensures that all interactions are natural, engaging, and highly personalized, which is critical in the influencer marketing space where authenticity is key.



# Roadmap ahead

Taitris is about onboarding new agents, make them collaborate and ship an end-to-end marketing campaign with a first focus on product seeding.

* ✅ function calling such as SerpAPI for google search
* 🎯 advanced function calling (social media scraping and outreach)
* 🎯 automated support for open source and closed source LLMs
* 🎯 automated follow up from each agent
* 🎯 evaluation of lead quality