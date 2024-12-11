# NowDotAI

[![PyPI - Version](https://img.shields.io/pypi/v/NowDotAI)](https://pypi.org/project/NowDotAI/)
[![CI](https://github.com/ShoggothAI/NowDotAI/actions/workflows/build.yml/badge.svg)](https://github.com/ShoggothAI/NowDotAI/actions/workflows/build.yml)

[Website](https://NowDotAI.ai) •︎ [Documentation](https://NowDotAI.readthedocs.io)

Welcome to NowDotAI, your ultimate framework for building multi-agent AI systems. With NowDotAI, you can seamlessly mix and match AI agents and tools from popular frameworks, design advanced workflows, and leverage dynamic knowledge graphs — all with simplicity and elegance.

Think of NowDotAI as a conductor that orchestrates a symphony of AI agents and tools. It provides building blocks for creating AI systems, enabling you to focus on the high-level design while NowDotAI takes care of the rest.

## Features
- **Integration**: Combine AI agents and tools from Langchain, LlamaIndex, CrewAI, and Autogen. Use tools from Langchain and LlamaIndex, with more integrations coming soon.
- **Flexibility**: Provide your agents with any tools or even other agents. All components implement Langchain's Runnable API, making them compatible with LCEL.
- **Advanced Flow Design**: Design systems of any complexity by just coding a brief set of rules. Simply chain tasks together or utilize knowledge graphs for sophisticated flow design.
- **Caching and Observability**: Built-in open-source observability with [Lunary](https://github.com/lunary-ai/lunary) and caching of HTTP requests, including LLM API calls, with [motleycache](https://github.com/ShoggothAI/motleycache).

See our [quickstart](https://NowDotAI.readthedocs.io/en/latest/quickstart.html) page for an overview of the framework and its capabilities.


## Getting started

### Installation
```
pip install NowDotAI
```

### First steps
To get you started, here's a simple example of how to create a crew with two agents: a writer and an illustrator. The writer will write a short article, and the illustrator will illustrate it.

```python
from NowDotAI import NowDotAICrew
from NowDotAI.agents.langchain import ReActToolCallingNowDotAIAgent
from NowDotAI.tasks import SimpleTask
from NowDotAI.tools.image.dall_e import DallEImageGeneratorTool
from langchain_community.tools import DuckDuckGoSearchRun

crew = NowDotAICrew()

writer = ReActToolCallingNowDotAIAgent(name="writer", tools=[DuckDuckGoSearchRun()])
illustrator = ReActToolCallingNowDotAIAgent(name="illustrator", tools=[DallEImageGeneratorTool()])

write_task = SimpleTask(
    crew=crew, agent=writer, description="Write a short article about latest AI advancements"
)
illustrate_task = SimpleTask(
    crew=crew, agent=illustrator, description="Illustrate the given article"
)

write_task >> illustrate_task

crew.run()

print(write_task.output)
print(illustrate_task.output)
```

Here, we have a chain of two consecutive tasks. A SimpleTask basically just contains a prompt and an agent that will execute it. The `>>` operator is used to chain tasks together.  
If you want to learn more about creating flows in such fashion, see our [blog with images](https://NowDotAI.readthedocs.io/en/latest/examples/blog_with_images.html) example.

### Knowledge graph and custom tasks
Under the hood, the tasks are stored in a knowledge graph, as well as all the data needed for their execution. You can create custom tasks that utilize the knowledge graph in any way you want. The graph can be used to control the flow of your system, or simply as a universal data store.

Please read our docs on [key concepts and API](https://NowDotAI.readthedocs.io/en/latest/key_concepts.html) to learn more about creating custom tasks and using the knowledge graph. Also, see how it all comes alive in the [research agent](https://NowDotAI.readthedocs.io/en/latest/examples/research_agent.html) example.

### Caching and observability
We provide a universal HTTP caching tool, [motleycache](https://github.com/ShoggothAI/motleycache), also available as a separate package. It can cache all HTTP requests made by your agents, including LLM and tool calls, out of the box. This is especially useful for debugging and testing.

NowDotAIcrew also comes with support for [Lunary](https://github.com/lunary-ai/lunary), an open-source observability platform. You can use it to monitor your agents' performance, visualize the flow of your system, and more.

To learn more about these features, see our [caching and observability](https://NowDotAI.readthedocs.io/en/latest/caching_observability.html) docs.

### Examples
We have a small but growing collection of examples in our [documentation](https://NowDotAI.readthedocs.io/en/latest/examples.html).

- For a working example of agents, tools, crew, and SimpleTask, check out the [blog with images](https://NowDotAI.readthedocs.io/en/latest/examples/blog_with_images.html).
- For a working example of custom tasks that fully utilize the knowledge graph backend, check out the [research agent](https://NowDotAI.readthedocs.io/en/latest/examples/research_agent.html).


## Support and contributions
We have a community [Discord server](https://discord.gg/P4Pxqf9MEs) where you can ask questions, share your ideas, and get help with your projects.

If you find a bug or have a feature request, feel free to [open an issue](https://github.com/ShoggothAI/NowDotAI/issues/new) in this repository.
Contributions of any kind are also welcome!
