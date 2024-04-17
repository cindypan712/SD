import requests
import json

base_url = 'https://api.kivaws.org/graphql?query='

# query.txt is where query is modified
f_query = open('query.txt', 'r')
query = f_query.read()
# gets rid of newline
query = query.replace('\n', '')

r = requests.get(base_url + query)
f_output = open('query_output.txt', 'w')
output_json = r.json()
json.dump(output_json, f_output, indent=3)
f_output.close()

filtered_values = {}
# filter output_json
if 'data' in output_json:
    if 'lend' in output_json['data']:
        if 'loans' in output_json['data']['lend']:
            if 'values' in output_json['data']['lend']['loans']:
                # dummy variable just so the output can be a dictionary
                acc = 0
                for value in output_json['data']['lend']['loans']['values']:
                    length = len(value['description'].split())
                    # could change this threshold
                    if length >= 30:
                        filtered_values[acc] = value
                        acc += 1

f_filtered = open('filtered_output.txt', 'w')
json.dump(filtered_values, f_filtered, indent=3)
f_filtered.close()