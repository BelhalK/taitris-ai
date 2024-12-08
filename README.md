[![X (formerly Twitter)](https://img.shields.io/twitter/follow/BelhalK?style=social)](https://twitter.com/BelhalK)
[![GitHub](https://img.shields.io/github/followers/BelhalK?label=Follow&style=social)](https://github.com/BelhalK)

# Taitris: AI-Powered Influencer Marketing Automation

Taitris is an intelligent framework that automates and optimizes influencer marketing campaigns using advanced AI agents and language models. By leveraging both proprietary models like GPT-4 and open-source alternatives like LLaMA, Taitris handles the entire influencer marketing workflow - from discovery to outreach to negotiation.

## Key Features

### 🤖 Intelligent AI Agents
- **LeadGenerator**: Identifies and qualifies relevant influencers based on your campaign criteria
- **OutreachSales**: Crafts and sends personalized outreach messages to potential collaborators
- **Negotiator**: Handles compensation discussions and agreement terms automatically

### 🔧 Technical Capabilities
- Supports multiple LLM backends (GPT-3.5, GPT-4, LLaMA models)
- Integrates with external APIs for enhanced functionality (SerpAPI, social media)
- Configurable via YAML for easy customization

### 💪 Benefits
- Fully automated end-to-end campaign management
- Data-driven influencer selection and qualification
- Consistent and personalized communication
- Efficient negotiation and agreement process
- Scalable for campaigns of any size


# How to use Taitris

### Running Python code

You can run your first campaign script `influencers_campaign.py` by typing the following command:

```
python influencers_campaign.py --company name-of-the-company --objective test --quota_seeding 10 --budget 1000 --negotiate True
```

# Roadmap ahead

Taitris is about onboarding new agents, make them collaborate and ship an end-to-end marketing campaign with a first focus on product seeding.

* ✅ function calling such as SerpAPI for google search
* 🎯 advanced function calling (social media scraping and outreach)
* 🎯 automated support for open source and closed source LLMs
* 🎯 automated follow up from each agent
* 🎯 evaluation of lead quality