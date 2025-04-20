import json
import os

from bs4 import BeautifulSoup
from crewai_tools import BaseTool, SerperDevTool
from dotenv.main import load_dotenv
from firecrawl import FirecrawlApp
from pydantic import PrivateAttr
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

load_dotenv()

Serper_api_key = os.environ.get("SERPER_API_KEY")
api_key = os.environ.get("FIRECRAWL_API_KEY")


tool = SerperDevTool()


class NewsCrawlerTool(BaseTool):
    name: str = "news_crawler_tool"
    description: str = (
        "A tool to scrape content from news websites using provided URLs. "
        "The tool extracts both raw HTML and plain text content."
    )
    function_description: str = "This tool is used to crawl the news websites and get the news title related content from the sources link that is given in the list of dictionaries from the News_WriterAgent."
    _app: FirecrawlApp = PrivateAttr()

    def __init__(self, api_key: str):
        super().__init__()
        self._app = FirecrawlApp(api_key=api_key)

    def crawl_news_content(self, input_data: list[dict]) -> list[dict]:
        try:
            # with open(input_file, 'r') as f:
            #     articles = json.load(f)
            output_data = []
            for article in input_data:
                url = article["link"]
                if not url:
                    continue

                try:
                    scrape_result = self._app.scrape_url(
                        url, params={"formats": ["markdown", "html"]}
                    )
                    main_text = None
                    if "html" in scrape_result:
                        soup = BeautifulSoup(scrape_result["html"], "html.parser")
                        main_text = soup.get_text(strip=True)
                    article["content"] = main_text if main_text else "Content not found"
                except Exception as scrape_error:
                    # Handle errors for specific articles
                    article["content"] = f"Error scraping content: {scrape_error}"

                output_data.append(article)

            print("Scraping completed and saved to the file.")
            return output_data

        except Exception as e:
            print(f"An error occurred: {e}")

    def _run(self, input_data: list[dict]) -> list[dict]:
        """
        Abstract method implementation for BaseTool.

        Args:
            input_data (list[dict]): A list of dictionaries, each containing:
                - 'title': Title of the article.
                - 'link': URL of the article.
                - 'headline': Short description (optional).
                - 'source': Source of the article (optional).

        Returns:
            list: List of dictionaries with updated content for each article.
        """
        return self.crawl_news_content(input_data)


tool1 = NewsCrawlerTool(api_key=api_key)


class ArticleAnalysisTool(BaseTool):
    name: str = "article_analysis_tool"
    description: str = (
        "A tool to analyze news articles for sentiment and calculate a heuristic credibility score. "
        "It takes a list of articles with their title, link, and content and returns the analysis results."
    )

    _analyzer: SentimentIntensityAnalyzer = PrivateAttr()

    def __init__(self):
        super().__init__()
        self._analyzer = SentimentIntensityAnalyzer()

    def analyze_sentiment(self, content: str) -> dict:
        """
        Analyze the sentiment of the provided content.

        Args:
            content (str): The text content of an article.

        Returns:
            dict: Sentiment analysis results, including sentiment type and score.
        """
        sentiment_scores = self._analyzer.polarity_scores(content)
        sentiment = "Neutral"
        if sentiment_scores["compound"] >= 0.05:
            sentiment = "Positive"
        elif sentiment_scores["compound"] <= -0.05:
            sentiment = "Negative"
        return {"Sentiment": sentiment, "Score": sentiment_scores["compound"]}

    def calculate_credibility(self, article: dict) -> int:
        """
        Calculate a heuristic credibility score for the article.

        Args:
            article (dict): A dictionary with article details, including the link and content.

        Returns:
            int: A credibility score between 0 and 100.
        """
        credibility = 50
        source_reputation = 35 if "business-standard" in article.get("link", "").lower() else 15
        quality_bonus = 15 if len(article.get("content", "")) > 200 else 5
        credibility += source_reputation + quality_bonus
        return min(credibility, 100)

    def process_articles(self, articles: list[dict]) -> list[dict]:
        """
        Process a list of articles to analyze sentiment and calculate credibility.

        Args:
            articles (list[dict]): List of articles with title, link, and content.

        Returns:
            list[dict]: Processed articles with additional sentiment and credibility data.
        """
        results = []
        for article in articles:
            sentiment_result = self.analyze_sentiment(article.get("content", ""))
            credibility_score = self.calculate_credibility(article)
            processed_article = {
                "Title": article.get("title", ""),
                "Link": article.get("link", ""),
                "Content": article.get("content", ""),
                "Sentiment": sentiment_result["Sentiment"],
                "Sentiment Score": sentiment_result["Score"],
                "Credibility Score": credibility_score,
            }
            results.append(processed_article)
        return results

    def _run(self, input_data: list[dict]) -> list[dict]:
        """
        Run method for executing the tool's logic.

        Args:
            input_data (list[dict]): List of articles to process, with title, link, and content.

        Returns:
            list[dict]: Processed articles with sentiment and credibility scores.
        """
        if not input_data or not isinstance(input_data, list):
            raise ValueError("Input must be a list of dictionaries with article details.")
        return self.process_articles(input_data)


tool2 = ArticleAnalysisTool()
