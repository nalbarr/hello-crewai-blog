# NOTE:
# - https://docs.crewai.com/en/quickstart
import os
from crewai import Agent, Task, Process, Crew, LLM
from crewai.project import CrewBase, agent, crew, task

# NOTE:
# - prefer Docling
# from crewai.knowledge.source.pdf_knowledge_source import PDFKnowledgeSource
from crewai.knowledge.source.crew_docling_source import CrewDoclingSource
from crewai_tools import SerperDevTool, DallETool
from dotenv import load_dotenv

import warnings

warnings.filterwarnings("ignore")

# config
load_dotenv()

# knowledge
"""
pdfs = PDFKnowledgeSource(
    file_paths=['article1.pdf',
                # 'article2.pdf',
                #'article3.pdf'
                ]
)
"""

pdfs = CrewDoclingSource(file_paths=["article1.pdf"])


# llms
llm = LLM(model="gpt-4o", api_key=os.environ.get("OPENAI_API_KEY"), temperature=0.4)


dalle = DallETool(
    model="dall-e-3",
    quality="standard",
    n=1,
    api_key=os.environ.get("OPENAI_API_KEY"),
    image_description="create an illustration style image about {topic}",
)


@CrewBase
class BlogWriter:
    """Crew to write a blog post"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def writer_style(self) -> Agent:
        return Agent(
            config=self.agents_config["writer_style"],
            verbose=1,
            knowledge_sources=[pdfs],
        )

    @agent
    def planner(self) -> Agent:
        return Agent(
            config=self.agents_config["planner"],
            verbose=True,
            tools=[SerperDevTool()],
            llm=llm,
        )

    @agent
    def content_writer(self) -> Agent:
        return Agent(config=self.agents_config["content_writer"], verbose=1)

    @agent
    def editor(self) -> Agent:
        return Agent(config=self.agents_config["editor"], verbose=1)

    @agent
    def illustrator(self) -> Agent:
        return Agent(
            config=self.agents_config["illustrator"], verbose=1, tools=[dalle], llm=llm
        )

    @task
    def style(self) -> Task:
        return Task(
            config=self.tasks_config["mystyle"],
        )

    @task
    def plan(self) -> Task:
        return Task(
            config=self.tasks_config["plan"],
        )

    @task
    def write(self) -> Task:
        return Task(
            config=self.tasks_config["write"], output_file="output/blog_post.md"
        )

    @task
    def edit(self) -> Task:
        return Task(config=self.tasks_config["edit"])

    @task
    def illustrate(self) -> Task:
        return Task(
            config=self.tasks_config["illustrate"], output_file="output/picture.txt"
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Blog Post crew"""

        return Crew(
            agents=[
                self.writer_style(),
                self.planner(),
                self.content_writer(),
                self.editor(),
                self.illustrator(),
            ],
            tasks=[
                self.style(),
                self.plan(),
                self.write(),
                self.edit(),
                self.illustrate(),
            ],
            process=Process.sequential,
            verbose=True,
        )
