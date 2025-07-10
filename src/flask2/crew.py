from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task, llm
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List


@CrewBase
class AgenteGerenciador():
    """AgenteGerenciador crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    @llm
    def groq_llm(self):
        return LLM(
            model="groq/gemma2-9b-it",
            api_key="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"
        )

    @agent
    def planning_interpreter(self) -> Agent:
        return Agent(
            config=self.agents_config['planning_interpreter'], 
            verbose=True,
            llm=self.groq_llm()
        )

    @task
    def planning_interpreter_task(self) -> Task:
        return Task(
            config=self.tasks_config['planning_interpreter_task'],
        )

    @crew
    def crew(self) -> Crew:
        """Creates the AgenteGerenciador crew"""
        
        return Crew(
            agents=self.agents, 
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
            manager_llm=self.groq_llm()
        )
