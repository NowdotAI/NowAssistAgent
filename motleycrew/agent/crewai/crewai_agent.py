from typing import Optional, Any, Sequence

from motleycrew.tool import MotleyTool
from motleycrew.common import MotleySupportedTool
from motleycrew.common import LLMFramework
from motleycrew.common.llms import init_llm
from motleycrew.agent.parent import MotleyAgentAbstractParent
from motleycrew.agent.crewai import CrewAIMotleyAgentParent
from motleycrew.agent.crewai import CrewAIAgentWithConfig


class CrewAIMotleyAgent(CrewAIMotleyAgentParent):
    def __init__(
        self,
        role: str,
        goal: str,
        backstory: str,
        delegation: bool | Sequence[MotleyAgentAbstractParent] = False,
        tools: Sequence[MotleySupportedTool] | None = None,
        llm: Optional[Any] = None,
        verbose: bool = False,
    ):
        if tools is None:
            tools = []

        if llm is None:
            # CrewAI uses Langchain LLMs by default
            llm = init_llm(llm_framework=LLMFramework.LANGCHAIN)

        def agent_factory(tools: dict[str, MotleyTool]):
            langchain_tools = [t.to_langchain_tool() for t in tools.values()]
            agent = CrewAIAgentWithConfig(
                role=role,
                goal=goal,
                backstory=backstory,
                verbose=verbose,
                allow_delegation=False,  # Delegation handled by MotleyAgentParent
                tools=langchain_tools,
                llm=llm,
            )
            return agent

        super().__init__(
            goal=goal,
            name=role,
            agent_factory=agent_factory,
            delegation=delegation,
            tools=tools,
            verbose=verbose,
        )
