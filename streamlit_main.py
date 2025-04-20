import streamlit as st
from crewgooglegemini.main import summarize_article, extract_keywords, analyze_sentiment


st.set_page_config(page_title="NewsAIAgent", layout="wide")
st.title("📰 NewsAIAgent")
st.markdown("Analyze, summarize, and extract insights from news articles using AI.")


article_text = st.text_area("Enter the news article text here:", height=300)


if st.button("Analyze"):
    if article_text.strip() == "":
        st.warning("Please enter the text of a news article to analyze.")
    else:
        with st.spinner("Analyzing the article..."):
            summary = summarize_article(article_text)
            keywords = extract_keywords(article_text)
            sentiment = analyze_sentiment(article_text)

        st.subheader("📝 Summary")
        st.write(summary)

        st.subheader("🔑 Keywords")
        st.write(", ".join(keywords))

        st.subheader("📊 Sentiment Analysis")
        st.write(f"The sentiment of the article is **{sentiment}**.")
