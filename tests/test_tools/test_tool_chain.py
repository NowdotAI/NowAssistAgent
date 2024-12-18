import pytest

from NowDotAI.tools import NowDotAITool


class ToolMock:
    def invoke(self, input: dict, *args, **kwargs):
        return input

    def _run(self, input: dict, *args, **kwargs):
        return input


@pytest.fixture
def tools():
    tool1 = NowDotAITool(ToolMock())
    tool2 = NowDotAITool(ToolMock())
    return [tool1, tool2]


def test_tool_chain(tools):
    tool1, tool2 = tools
    tool_chain = tool1 | tool2
    assert hasattr(tool_chain, "invoke")
    prompt = {"prompt": "test prompt"}
    assert tool_chain.invoke(prompt) == prompt
