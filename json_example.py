import json, requests
from dateutil.parser import parse
from collections import Counter

serialized = """{ "title" : "Data Science Book",
                  "author" : "Joel Grus",
                  "publications" : 2014,
                "topics" : [ "data", "science", "data science" ] }"""

with open("credentials.json") as f:
    credentials = json.load(f)
print(credentials['access_token'])

# parse the JSON to create a Python dict
deserialized = json.loads(serialized)
if "data science" in deserialized["topics"]:
    print(deserialized)


endpoint = "https://api.github.com/users/joelgrus/repos"

repos = json.loads(requests.get(endpoint).text)

dates = [parse(repo["created_at"]) for repo in repos]
month_counts = Counter(date.month for date in dates)
weekday_counts = Counter(date.weekday for date in dates)

print("month counts: {} and weekday counts: {}".format(month_counts, weekday_counts))

last_5_repositories = sorted(repos, key=lambda r: r["created_at"], reverse=True)[:5]
last_5_languages = [repo["language"] for repo in last_5_repositories]

print("5 repos {} and 5 languages {}".format(last_5_repositories, last_5_languages))