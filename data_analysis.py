##
## ENV SETUP
##
import pandas as pd
import seaborn as sns
from collections import Counter
import numpy as np
import matplotlib.pyplot as plt


##
## VISUALIZATION
##
df = pd.read_csv("data/topics.csv")

topics = np.concatenate([list(df[str(i)])*(11-i) for i in range(1, 11)])
topic_frequency = Counter(topics)
topic_frequency = sorted(topic_frequency.items(), key=lambda kv: kv[1], reverse=True)
top_topic_frequency = topic_frequency[0:10]
top_topic_df = pd.DataFrame.from_dict(top_topic_frequency)
top_topic_df.columns = ["topic", "count"]
ax = sns.barplot(
	x="topic", y="count",
	data=top_topic_df, orient="v",
	color="salmon",
	palette=sns.light_palette("#FF635A", reverse=True, n_colors=len(top_topic_df))
)
plt.box(on=None)
ax.set_title("Weighted Count of Top Topics in IBS-related Forum Entries")
ax.set_xlabel("Topics")
ax.set_ylabel("Weighted Count")

# Sentiment Pie Chart
sentiment_map = {"P":"Positive", "N":"Negative", "NEU":"Neutral"}
sentiment_frequency = dict(Counter(df['sentiment'].dropna()))
labels = [sentiment_map[item] for item in list(sentiment_frequency.keys())]
sizes = list(sentiment_frequency.values())
sizes_pct = [i/sum(sizes) for i in sizes]
plt.pie(sizes, labels=labels, autopct='%1.1f%%', colors=sns.light_palette("#FF635A", reverse=True, n_colors=len(sizes)))
plt.title("Distribution of Sentiment in Forum Entries")