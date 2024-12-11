from dotenv import load_dotenv
from langchain_community.tools import DuckDuckGoSearchRun

from NowDotAI import NowDotAICrew
from NowDotAI.agents.langchain.tool_calling_react import ReActToolCallingNowDotAIAgent
from NowDotAI.common import configure_logging
from NowDotAI.tasks import SimpleTask


def main():
    search_tool = DuckDuckGoSearchRun()

    tools = [search_tool]

    researcher = ReActToolCallingNowDotAIAgent(
        tools=tools,
        verbose=True,
        chat_history=True,
        # llm=init_llm(
        #     llm_framework=LLMFramework.LANGCHAIN,
        #     llm_family=LLMFamily.ANTHROPIC,
        #     llm_name="claude-3-sonnet-20240229",
        # ),
    )

    outputs = []

    crew = NowDotAICrew()
    task = SimpleTask(
        crew=crew,
        name="produce comprehensive analysis report on AI advancements",
        description="""Conduct a comprehensive analysis of the latest advancements in AI.
      Identify key trends, breakthrough technologies, and potential industry impacts.
      Your final answer MUST be a full analysis report""",
        agent=researcher,
    )
    crew.run()
    print(task.output)

    # See whether the researcher's memory persists across tasks
    tldr_task = SimpleTask(
        crew=crew,
        name="provide a TLDR summary of the report",
        description="Write a short summary of the comprehensive analysis report on AI advancements that you just wrote.",
        agent=researcher,
    )

    crew.run()
    print(tldr_task.output)


if __name__ == "__main__":
    configure_logging(verbose=True)

    load_dotenv()
    main()
