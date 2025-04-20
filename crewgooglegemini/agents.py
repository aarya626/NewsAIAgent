import os

from crewai import LLM, Agent
from dotenv.main import load_dotenv
from tools import tool, tool1, tool2

load_dotenv()
Google_api_key = os.environ.get("GOOGLE_API_KEY")


llm = LLM(
    model="gemini/gemini-1.5-flash",
    api_key=Google_api_key,
    temperature=0.5,
    verbose=True,
)

News_ResearchAgent = Agent(
    role="You are a senior research assistant that can help with finding news sources on the internet",
    goal="Uncover the latest news articles sources on the {topic} on the web.",
    verbose=True,
    memory=True,
    backstory="You are a senior research assistant who brings the news from all the sources in the form of Title, Link and headlines available on the internet to the user. The main aim of your should be to fetch news such that we are able analyse it for another agents in terms of sentiment, credibility and other aspects",
    tools=[tool],
    llm=llm,
    allow_delegation=True,
)


News_WriterAgent = Agent(
    role="You are a news writer assistant",
    goal="Generating json file of several sources of the news on the {topic} given by the user",
    verbose=True,
    memory=True,
    backstory="You are an agent which generates json file of several sources like title, link and headlines as key value pairs it recieves from the News_ResearchAgent in the json file on the news - {topic} given by the user. It is important that you generate json file with all the sources and not miss any source and also the json file should be in the correct format like list of dictionaries. Also you should be passing the list generated directly to the News_CrawlerAgent. There should be no marking as json or ``` type in the json file.",
    tools=[tool],
    llm=llm,
    allow_delegation=False,
)

News_CrawlerAgent = Agent(
    role="You are a news website crawler agent",
    goal="Crawl the news websites and get the news related content from the sources link.",
    verbose=True,
    memory=True,
    backstory="You are an agent which crawls the news websites and gets the news related content from that sources link which is given by the News_WriterAgent in the json file and from that sources link it gets the title, link and headlines of the news and then you crawls the website and gets the news content and then it returns it to the News_SentimentAnalyserAgent as another json file which has the title, link, headlines, source and the news content using the tools function provided to you. There should be no marking as json or ``` type in the json file.",
    tools=[tool1],
    llm=llm,
    allow_delegation=True,
)


News_SentimentAnalyser = Agent(
    role="You are a news sentiment analyser agent",
    goal="Generate a sentiment and credibility score for each news article content present in list of dictionaries",
    verbose=True,
    memory=True,
    backstory="You are a senior news sentiment analyser agent who analyses the news article content present in list of dictionaries and generates a sentiment and credibility score for each news article content present in list of dictionaries it recieves from the News_CrawlerAgent. You are using the vaderSentiment library by the self-declared tool to generate the sentiment and credibility score for each news article content present in list of dictionaries.",
    tools=[tool2],
    llm=llm,
    allow_delegation=True,
)
