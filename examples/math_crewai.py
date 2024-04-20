from dotenv import load_dotenv

from motleycrew import MotleyCrew, Task
from motleycrew.agent.crewai import CrewAIMotleyAgent
from motleycrew.tool.python_repl import create_repl_tool

load_dotenv()

repl_tool = create_repl_tool()

# Define your agents with roles and goals
solver1 = CrewAIMotleyAgent(
    role="High School Math Teacher",
    goal="Generate great solutions to math problems",
    backstory="""You are a high school math teacher with a passion for problem-solving.
To solve a math problem, you first reason about it, step by step, then generate the code to solve it exactly,
using sympy, then use the REPL tool to evaluate that code, and then
use the output to generate a human-readable solution.""",
    verbose=True,
    delegation=False,
    tools=[repl_tool],
)

solver = solver1

problems = [
    "Problem: If $725x + 727y = 1500$ and $729x+ 731y = 1508$, what are the values of $x$, $y$, and $x - y$ ?",
    "Drei Personen erhalten zusammen Fr. 2450. Die erste Person erh\u00e4lt Fr. 70 mehr als die zweite, aber Fr. 60 weniger als die dritte.\nWie viel erh\u00e4lt jede Person? ",
    "Find all numbers $a$ for which the graph of $y=x^2+a$ and the graph of $y=ax$ intersect. Express your answer in interval notation.",
]

# Create tasks for your agents
crew = MotleyCrew()
task1 = Task(
    crew=crew,
    name="solve math problem",
    description=f"""Create a nice human-readable solution to the following problem:
    {problems[1]}
     IN THE SAME LANGUAGE AS THE PROBLEM""",
    agent=solver,
)


# Instantiate your crew with a sequential process
result = crew.run(
    agents=[solver],
    verbose=True,  # You can set it to 1 or 2 to different logging levels
)

# Get your crew to work!
print(list(result._done)[0].outputs)

print("######################")