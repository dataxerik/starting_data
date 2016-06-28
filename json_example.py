import json, requests

serialized = """{ "title" : "Data Science Book",
                  "author" : "Joel Grus",
                  "publications" : 2014,
                "topics" : [ "data", "science", "data science" ] }"""

# parse the JSON to create a Python dict
deserialized = json.loads(serialized)
if "data science" in deserialized["topics"]:
    print(deserialized)


endpoint = ""

repos = json.loads(requests.get(endpoint).text)