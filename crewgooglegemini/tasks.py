from agents import News_CrawlerAgent, News_ResearchAgent, News_SentimentAnalyser, News_WriterAgent
from crewai import Task
from tools import tool, tool1, tool2

research_task = Task(
    description="""
    Note:
    1. Research the latest news articles sources on the {topic} available on the internet through best unbiased news agencies.
    2. Focus more on the credibility of the sources and the sentiment of the news based on various aspects like language, tone, facts, geography, emotions, etc.
    3. Match the topic given by the user.
    """,
    expected_output="""
    Note:
    1. A list of news articles sources listing the title, link and headlines of the news on the topic with their URLs of several domains.
    2. Pass the list to the next agent.
    """,
    tools=[tool],
    agent=News_ResearchAgent,
)

write_task = Task(
    description="""
    Note:
    1. Generate a json file of several sources like title, link, source and headlines as key value pairs it receives from the News_ResearchAgent.
    2. The json file should be on the news - {topic} given by the user.
    3. Pass the json file to the News_CrawlerAgent.
    """,
    expected_output="""
    Note:
    1. A json file with all the sources, title, link and headlines.
    2. Do not miss any source.
    3. Maintain correct format as list of dictionaries.
    4. Pass the list generated directly to the News_CrawlerAgent.
    5. No json or ``` type markings in the file.
    """,
    tools=[tool],
    agent=News_WriterAgent,
    async_execution=False,
    output_file="news_urls.json",
)

crawl_task = Task(
    description="""
    Note:
    1. Crawl the news websites and get the news title related content from the sources link that is given in the list of dictionaries from the News_WriterAgent.
    2. Go through each dictionary key-value pair and get the content from the sources link and then crawl it efficiently ignoring the ads, navigation elements, and other irrelevant content.
    3. Handle different website structures and formats gracefully.
    4. You should only crawl the website within the limit of 100 words.
    5. Ignore all the characters which can give error in the string syntax
    6.  No json or ``` type markings in the file
    """,
    expected_output="""
    Note:
    1. A json file with all the sources, title, link, source, headlines and content crawled
    2. Do not miss any source, maintain correct format as list of dictionaries
    3. Use the provided tool that takes input as list of dictionaries from previous task/agent & returns output as list of dictionaries
    4. Generate output json file same as before with additional content key-value pair
    5. No json or ``` type markings in the file
    6. Efficiently crawl content ignoring ads, navigation and irrelevant elements
    7. Pass the list generated directly to the News_SentimentAnalyser agent.
    8. Limit content to 100 words per article
    9. Ignore characters that could cause string syntax errors
    """,
    tools=[tool1],
    agent=News_CrawlerAgent,
    output_file="news_content.json",
)

sentiment_task = Task(
    description="""
    Note:
    1. You are getting the list of dictionaries with the title, link, source, headlines and content crawled from the News_CrawlerAgent.
    2. Generate a sentiment and credibility score for each news article content present in that list of dictionaries.
    3. You can use the self-declared tool assigned to you to generate the sentiment and credibility score for each news article content present in that list of dictionaries.
    4. You should calculate the sentiment and credibility score for each news article content present in that list of dictionaries without any miss.
    5. No json or ``` type markings in the file
    """,
    expected_output="""
    Note:
    1. A json file with all the sources, title, link, source, headlines, content, sentiment and credibility score for each news article content present in list of dictionaries recieved from the News_CrawlerAgent.
    2. Do not miss any source, maintain correct format as list of dictionaries.
    3. Use the provided tool that takes input as list of dictionaries from previous task/agent & returns output as list of dictionaries.
    4. Generate output json file same as before with additional sentiment and credibility score as key-value pair in the dictionaries.
    5. No json or ``` type markings in the file
    """,
    tools=[tool2],
    agent=News_SentimentAnalyser,
    output_file="news_sentiment.json",
)
