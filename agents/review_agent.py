from agents.Base_agent import Baseagent
from config.settings import settings
from prompts.review_prompts import REVIEW_SYSTEM_PROMPT

class Review_agent(Baseagent):
    def  __init__(self,model=None,memory=None):
        super().__init__(
            name="review",
            model=model or settings.default_model,
            tools=[],
            system_prompt=REVIEW_SYSTEM_PROMPT,
            memory=memory
        )
        