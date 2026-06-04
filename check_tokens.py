
import pandas as pd

df = pd.read_csv("data/tech_news_articles.csv")

article = df[df["article_id"] == "NEWS_0010"].iloc[0]["text"]

print(article[:4000])
