from typing import Optional, Callable
from langchain.agents import create_agent, AgentState
from langchain.agents.middleware import AgentMiddleware
from langchain_core.language_models import BaseChatModel
from langchain_core.tools import BaseTool
from config.settings import settings
from memory.memory_manager import MemoryManager

class Baseagent:
    """this is an entry point agent"""
    def __init__(
            self,
            name:str,
            model: str | BaseChatModel,
            tools:list[BaseTool|Callable]=None,
            system_prompt:str="",
            middleware: list[AgentMiddleware]=None,
            memory: Optional[MemoryManager]=None
            ):
        self.name=name
        self.model=model
        self.tools=tools or []
        self.system_prompt=system_prompt
        self.middleware= middleware or []
        self.memory=memory
        self._agent=None
    
    def build(self):
        self._agent=create_agent(
            model=self.model,
            tools=self.tools,
            systemprompt=self.system_prompt,
            middleware=self.middleware,
            name=self.name
        )

        return self._agent
    
    def ainvoke(self,query:str)->dict:
        if self._agent is None:
            self.build()
        result=self._agent.ainvoke(
            {
                "messages":[("user,query")]
            }
        )

        return result
    
    def invoke(self,query:str)->dict:
        if self._agent is None:
            self.build()
        result=self._agent.invoke(
            {
                "messages":[("user,query")]
            }
        )

        return result
    
    def get_last_response(self,result:dict)->str:
        messages=result.get(messages,[])
        for i in reversed(messages):
            if hasattr(msg,"content") and msg.type=="ai":
                return i.content
            return ""