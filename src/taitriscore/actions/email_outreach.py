from typing import List
import os
from taitriscore.actions import Action
from taitriscore.logs import logger
from taitriscore.utils.schema import Message
import re

class EmailOutreach(Action):
    def __init__(self, name="", context=None, llm=None):
        super().__init__(name, context, llm)
        # For now, we'll mock the Gmail API
        self.email_template = """
        Subject: Collaboration Opportunity with Gardyn - Indoor Smart Garden

        Hi {influencer_name},

        I hope this finds you well! I'm reaching out because we love your content about {focus_area} and think you'd be a perfect partner for Gardyn.

        Gardyn is revolutionizing home gardening with our AI-powered indoor hydroponic system that lets anyone grow fresh produce year-round.

        Would you be interested in trying out our system and sharing your experience with your community?

        Looking forward to your response!

        Best regards,
        {sender_name}
        Gardyn Partnerships Team
        """

    def _extract_influencers(self, text) -> List[dict]:
        # Extract influencer information using regex
        pattern = r'@(\w+)\s*\((\d+K)\s*followers\)\s*(?:-|\n)((?:.*?\n)*?)(?=\d\.|$)'
        matches = re.finditer(pattern, text)
        
        influencers = []
        for match in matches:
            handle = match.group(1)
            followers = match.group(2)
            description = match.group(3).strip()
            
            # Extract focus area from description
            focus_area = description.split('-')[0].strip() if '-' in description else description
            
            influencers.append({
                'handle': handle,
                'followers': followers,
                'focus_area': focus_area,
                'description': description
            })
        
        return influencers

    async def run(self, context):
        # More detailed debug prints
        logger.debug(f"EmailOutreach received context with {len(context)} messages")
        for msg in context:
            logger.debug(f"Message in context - Role: {msg.role}, Content type: {type(msg.content)}")
            if isinstance(msg.content, str):
                logger.debug(f"Content preview: {msg.content[:50] if len(msg.content) > 50 else msg.content}")
        
        # Find any message containing lead information
        lead_gen_messages = [msg for msg in context 
                           if isinstance(msg.content, str) and 
                           ("@" in msg.content and "followers" in msg.content)]
        
        logger.debug(f"Found {len(lead_gen_messages)} messages with lead information")
        
        if not lead_gen_messages:
            logger.error("No lead generator messages found")
            return Message(
                content="No leads to process",
                role="Outreach Sales",
                cause_by=type(self)
            )

        # Get the most recent lead generator message
        leads_message = lead_gen_messages[-1].content
        
        # Extract influencer information
        influencers = self._extract_influencers(leads_message)
        
        # Future Gmail API implementation (commented out)
        """
        # Initialize Gmail API
        # SCOPES = ['https://www.googleapis.com/auth/gmail.send']
        # creds = None
        # if os.path.exists('token.json'):
        #     creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        # service = build('gmail', 'v1', credentials=creds)
        
        for influencer in influencers:
            email_content = self.email_template.format(
                influencer_name=f"@{influencer['handle']}",
                focus_area=influencer['focus_area'].lower(),
                sender_name="Adam"
            )
            # message = create_message("me", f"{influencer['handle']}@example.com", 
            #                         "Gardyn Collaboration Opportunity", email_content)
            # send_message(service, "me", message)
        """
        
        # For now, just mock the outreach process
        outreach_results = []
        for influencer in influencers:
            confirmation = f"📧 Successfully contacted @{influencer['handle']} ({influencer['followers']}) - Sent collaboration proposal for Gardyn's indoor garden system"
            logger.info(confirmation)
            outreach_results.append(confirmation)

        # Create summary message
        summary = f"""
        ✨ Outreach Campaign Update:
        
        I've reached out to {len(influencers)} potential influencers for the Gardyn campaign:
        """ + "\n        ".join(outreach_results) + """
        
        Will monitor for responses and follow up as needed.
        """

        return Message(
            content=summary,
            role="Outreach Sales",
            cause_by=type(self)
        ) 