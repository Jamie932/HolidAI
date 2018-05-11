import praw
import requests
import pycountry
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
from tabulate import tabulate

reddit = praw.Reddit(client_id='V8_4nOhk63r1ew', client_secret="IMIO-HQFsK1rArL9ZdubTZKdVHo", user_agent='windows:com.Jamie932.holidai:v1.0.0 (by /u/jamie932)')
subreddit = reddit.subreddit('travel+solotravel+backpacking+earthporn')
sia = SIA()
comments = []
count = 0

for submission in subreddit.top('day'): 
	for comment in submission.comments:
			if hasattr(comment, "body") and comment.distinguished==None:
				count += 1
				for country in pycountry.countries:
					if country.name in comment.body:
						polarity = sia.polarity_scores(comment.body)
						toAdd = [{'score' : comment.score, 'country' : country.name, "polarity" : polarity}]
						
						for d in comments:
							if d['country'] == country.name:
								d['score'] = comment.score + d['score']

								for polar in d['polarity']:
									polar = (polarity[polar] + polarity[polar])/2

								print("Updated " + country.name)
								toAdd = []

						comments += toAdd
								
top_countries_score = sorted(comments, key=lambda country: country['score'], reverse=True)[:10]
top_countries_positive = sorted(comments, key=lambda country: country['polarity']['pos'] - country['polarity']['neg'], reverse=True)[:10]
top_countries_negative = sorted(comments, key=lambda country: country['polarity']['neg'] - country['polarity']['pos'], reverse=True)[:10]
top_countries_average = sorted(comments, key=lambda country: country['polarity']['neu'], reverse=True)[:10]

print("-----------------------")
print("Best Scored Countries")
print("-----------------------")
print(tabulate(top_countries_score, headers={'score': 'Score', 'country': 'Country', 'polarity': 'Polarity'}))
print()
print("-----------------------")
print("Most Positive Countries")
print("-----------------------")
print(tabulate(top_countries_positive, headers={'score': 'Score', 'country': 'Country', 'polarity': 'Polarity'}))
print()
print("-----------------------")
print("Most Negative Countries")
print("-----------------------")
print(tabulate(top_countries_negative, headers={'score': 'Score', 'country': 'Country', 'polarity': 'Polarity'}))
print()
print("-----------------------")
print("Most Average Countries")
print("-----------------------")
print(tabulate(top_countries_average, headers={'score': 'Score', 'country': 'Country', 'polarity': 'Polarity'}))
print()
print("Number of posts scanned: " + str(count))