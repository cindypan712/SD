import requests
import json

base_url = 'https://api.kivaws.org/graphql?query='

# query.txt is where query is modified
f_query = open('query.txt', 'r')
query = f_query.read()
# gets rid of newline
query = query.replace('\n', '')

r = requests.get(base_url+ query)
f_output = open('query_output.txt', 'w')
json_comments = json.dump(r.json(), f_output, indent=3)
f_output.close()