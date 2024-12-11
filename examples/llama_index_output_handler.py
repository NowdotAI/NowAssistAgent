from dotenv import load_dotenv
from langchain_community.tools import DuckDuckGoSearchRun


from NowDotAI import NowDotAICrew
from NowDotAI.agents.llama_index import ReActLlamaIndexNowDotAIAgent
from NowDotAI.common import configure_logging
from NowDotAI.tasks import SimpleTask
from NowDotAI.common.exceptions import InvalidOutput
from NowDotAI.common import AsyncBackend
from NowDotAI.tools import NowDotAITool


def main():
    """Main function of running the example."""
    search_tool = DuckDuckGoSearchRun()

    class OutputHandler(NowDotAITool):
        def run(self, output: str):
            if "medicine" not in output.lower():
                raise InvalidOutput("Add more information about AI applications in medicine.")

            return {"checked_output": output}

    output_handler = OutputHandler(
        name="output_handler", description="Output handler", return_direct=True
    )

    # TODO: add LlamaIndex native tools
    researcher = ReActLlamaIndexNowDotAIAgent(
        prompt_prefix="Your goal is to uncover cutting-edge developments in AI and data science",
        tools=[search_tool, output_handler],
        force_output_handler=True,
        verbose=True,
        max_iterations=16,  # default is 10, we add more because the output handler may reject the output
    )

    crew = NowDotAICrew(async_backend=AsyncBackend.NONE)

    # Create tasks for your agents
    task = SimpleTask(
        crew=crew,
        name="produce comprehensive analysis report on AI advancements",
        description="""Conduct a comprehensive analysis of the latest advancements in AI in 2024.
      Identify key trends, breakthrough technologies, and potential industry impacts.
      Your final answer MUST be a full analysis report""",
        agent=researcher,
    )

    # Get your crew to work!
    crew.run()

    print(task.output)
    return task.output


if __name__ == "__main__":
    configure_logging(verbose=True)

    load_dotenv()
    main()
