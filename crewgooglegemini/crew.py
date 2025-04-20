from agents import News_CrawlerAgent, News_ResearchAgent, News_SentimentAnalyser, News_WriterAgent
from crewai import Crew, Process
from tasks import crawl_task, research_task, sentiment_task, write_task

crew = Crew(
    agents=[News_ResearchAgent, News_WriterAgent, News_CrawlerAgent, News_SentimentAnalyser],
    tasks=[research_task, write_task, crawl_task, sentiment_task],
    process=Process.sequential,
)

user_input = input("Enter the topic for the news summary: ")

result = crew.kickoff(inputs={"topic": user_input})

print("Your summarised news is: ", result)
