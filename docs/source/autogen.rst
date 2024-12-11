AutoGen-related Examples
========================

Here are some examples that firstly, show how some AutoGen patterns translate into NowDotAI (in particular,
how cases where UserProxy is only used as an AgentExecutor don't need multiple agents in other frameworks),
and secondly, how to use NowDotAI together with autogen, both by wrapping a collection of autogen agents as
a NowDotAI tool, and by giving NowDotAI tools and agents as tools to autogen.

.. toctree::
   :maxdepth: 2

   examples/math_single_agent
   examples/integrating_autogen
