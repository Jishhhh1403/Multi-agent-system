from agents.Base_agent import Baseagent
from config.settings import settings
from prompts.documentation_prompts import DOCUMENTATION_SYSTEM_PROMPT

class Documentation_agent(Baseagent):
    def  __init__(self,model=None,memory=None):
        super().__init__(
            name="documentation",
            model=model or settings.default_model,
            tools=[],
            system_prompt=DOCUMENTATION_SYSTEM_PROMPT,
            memory=memory
        )