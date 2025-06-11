from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

@CrewBase
class CybersecurityProject():
    """Cybersecurity and Content Creation crew"""


    def __init__(self, llm=None):
        self.llm = llm  # Recebe o LLM configurado


    @agent
    def cybersecurity_expert(self) -> Agent:
        return Agent(
            config=self.agents_config['cybersecurity_expert'], 
            llm=self.llm,
            verbose=True
        )

    @task
    def scam_check_task(self) -> Task:
        return Task(
            config=self.tasks_config['scam_check_task'],
            agent=self.cybersecurity_expert()
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Cybersecurity Project crew"""
        return Crew(  
            agents=[self.cybersecurity_expert()],
            tasks=[self.scam_check_task()],
            process=Process.sequential,
            verbose=True,
        )