from typing import Optional, Any
import json
from pathlib import Path

from langchain_core.language_models import BaseLanguageModel
from langchain_core.runnables import (
    RunnablePassthrough,
    RunnableLambda,
)
from langchain_core.tools import Tool
from langchain_core.prompts.base import BasePromptTemplate
from langchain_core.prompts import PromptTemplate

from langchain_core.pydantic_v1 import BaseModel, Field

from motleycrew.tool import MotleyTool
from motleycrew.common import LLMFramework
from motleycrew.common.llms import init_llm
from motleycrew.common.utils import print_passthrough
from motleycrew.storage import MotleyGraphStore

from question_struct import Question
from question_inserter import QuestionInsertionTool


default_prompt = PromptTemplate.from_template(
    """
You are a part of a team. The ultimate goal of your team is to
answer the following Question: '{question_text}'.\n
Your team has discovered some new text (delimited by ```) that may be relevant to your ultimate goal.
text: \n ``` {context} ``` \n
Your task is to ask new questions that may help your team achieve the ultimate goal.
If you think that the text is relevant to your ultimate goal, then ask new questions.
New questions should be based only on the text and the goal Question and no other previous knowledge.

You can ask up to {num_questions} new questions.
Return the questions each on a new line and ending with a single question mark.
Don't return anything else except these questions.
"""
)

# " The new questions should have no semantic overlap with questions in the following list:\n"
# " {previous_questions}\n"


class QuestionGeneratorTool(MotleyTool):
    """
    Gets a question as input
    Retrieves relevant docs (llama index basic RAG)
    (Retrieves existing questions from graph (to avoid overlap))
    Generates extra questions (research agent prompt)

    Adds questions as children of current q by calling Q insertion tool once
    exits
    """

    def __init__(
        self,
        query_tool: MotleyTool,
        graph: MotleyGraphStore,
        max_questions: int = 3,
        llm: Optional[BaseLanguageModel] = None,
        prompt: str | BasePromptTemplate = None,
    ):
        langchain_tool = create_question_generator_langchain_tool(
            query_tool=query_tool,
            graph=graph,
            max_questions=max_questions,
            llm=llm,
            prompt=prompt,
        )

        super().__init__(langchain_tool)


class QuestionGeneratorToolInput(BaseModel):
    """Input for the Question Generator Tool."""

    question: Question = Field(description="The input question for which to generate subquestions.")


def create_question_generator_langchain_tool(
    query_tool: MotleyTool,
    graph: MotleyGraphStore,
    max_questions: int = 3,
    llm: Optional[BaseLanguageModel] = None,
    prompt: str | BasePromptTemplate = None,
):
    if llm is None:
        llm = init_llm(llm_framework=LLMFramework.LANGCHAIN)

    llm.bind(json_mode=True)

    if prompt is None:
        prompt = default_prompt
    elif isinstance(prompt, str):
        prompt = PromptTemplate.from_template(prompt)

    assert isinstance(prompt, BasePromptTemplate), "Prompt must be a string or a BasePromptTemplate"

    def partial_inserter(input_dict: dict):
        out = QuestionInsertionTool(graph=graph, question=input_dict["question"]).to_langchain_tool()
        return (out,)

    def insert_questions(input_dict) -> None:
        inserter = input_dict["question_inserter"]["question_inserter"][0]
        questions_raw = input_dict["subquestions"].content
        questions = [q.strip() for q in questions_raw.split("\n") if len(q.strip()) > 1]

        inserter.invoke({"questions": questions})

    def set_context(input_dict: dict):
        context = input_dict["context"]
        graph.set_property(
            entity_id=input_dict["question"]["question"].id,
            property_name="context",
            property_value=json.dumps(input_dict["context"]),
        )

    # TODO: add context to question node
    pipeline = (
        {
            "question": RunnablePassthrough(),
            "context": query_tool.to_langchain_tool(),
            "question_inserter": RunnableLambda(partial_inserter),
        }
        | RunnableLambda(print_passthrough)
        | {
            "subquestions": RunnablePassthrough.assign(question_text=lambda x: x["question"]["question"].question)
            | prompt.partial(num_questions=max_questions)
            | llm,
            "context_setter": RunnableLambda(set_context),
            "question_inserter": RunnablePassthrough(),
        }
        | RunnableLambda(print_passthrough)
        | RunnableLambda(insert_questions)
    )

    return Tool.from_function(
        func=lambda question: pipeline.invoke({"question": question}),
        name="Question Generator Tool",
        description="""Generate a list of questions based on the input question, 
    and insert them into the knowledge graph.""",
        args_schema=QuestionGeneratorToolInput,
    )


if __name__ == "__main__":
    import kuzu
    from llama_index.graph_stores.kuzu import KuzuGraphStore

    here = Path(__file__).parent
    db_path = str(here / "test2")

    db = kuzu.Database(db_path)
    graph_store = KuzuGraphStore(db)

    query_tool = MotleyTool.from_langchain_tool(
        Tool.from_function(
            func=lambda question: [
                "Germany has consisted of many different states over the years",
                "The capital of France has moved in 1815, from Lyons to Paris",
                "France actually has two capitals, one in the north and one in the south",
            ],
            name="Query Tool",
            description="Query the library for relevant information.",
            args_schema=QuestionGeneratorToolInput,
        )
    )

    tool = QuestionGeneratorTool(
        query_tool=query_tool,
        graph=graph_store,
        max_questions=3,
    )

    tool.invoke({"question": "What is the capital of France?"})
    print("Done!")
