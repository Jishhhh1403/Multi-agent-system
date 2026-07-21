from agents.Base_agent import Baseagent
from config.settings import settings
from prompts.knowledge_prompt import KNOWLEDGE_SYSTEM_PROMPT

class Knowledge_agent(Baseagent):
    def  __init__(self,model=None,memory=None):
        super().__init__(
            name="knowledge",
            model=model or settings.default_model,
            tools=[],
            system_prompt=KNOWLEDGE_SYSTEM_PROMPT,
            memory=memory
        )