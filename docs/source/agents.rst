Agents
======

NowDotAICrew is first and foremost a multi-agent framework, so the concept of an agent is central to it.

An agent is essentially an actor that can perform tasks. Usually, it contains some kind of loop
that interacts with an LLM and performs actions based on the data it receives.


ReAct tool calling agent
------------------------
NowDotAICrew provides a robust general-purpose agent that implements
`ReAct prompting <https://react-lm.github.io/>`_: :class:`NowDotAI.agents.langchain.ReActToolCallingNowDotAIAgent`.
This agent is probably a good starting point for most tasks.

.. code-block:: python

    from NowDotAI.agents.langchain import ReActToolCallingNowDotAIAgent
    from langchain_community.tools import DuckDuckGoSearchRun

    agent = ReActToolCallingNowDotAIAgent(tools=[DuckDuckGoSearchRun()])
    agent.invoke({"prompt": "Which country currently has more population, China or India?"})


``ReActToolCallingNowDotAIAgent`` was tested with the newer OpenAI and Anthropic models, and it should work
with any model that supports function calling. If you want a similar agent for models without
function calling support, look at :class:`NowDotAI.agents.langchain.LegacyReActNowDotAIAgent`
or :class:`NowDotAI.agents.llama_index.ReActLlamaIndexNowDotAIAgent`.


Using agents from other frameworks
----------------------------------
For many tasks, it's reasonable to use a pre-built agent from some framework,
like Langchain, LlamaIndex, CrewAI etc. NowDotAICrew provides adapters for these frameworks,
which allow you to mix and match different agents together and easily provide them with any tools.


* :class:`NowDotAI.agents.langchain.LangchainNowDotAIAgent`
* :class:`NowDotAI.agents.llama_index.LlamaIndexNowDotAIAgent`
* :class:`NowDotAI.agents.crewai.CrewAINowDotAIAgent`


Creating your own agent
-----------------------
The simplest way to create your own agent is to subclass :class:`NowDotAI.agents.parent.NowDotAIAgentParent`.

Note that in a `crew <key_concepts.html#crew-and-knowledge-graph>`_,
not only an agent can be a `worker <key_concepts.html#tasks-task-units-and-workers>`_.
A worker is basically any `Runnable <https://python.langchain.com/v0.1/docs/expression_language/interface/>`_,
and all agents and tools implement the Runnable interface in NowDotAI.
