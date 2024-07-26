import json
results = json.load(open('results.json'), )
for word, list in results.items():
    print(word + ': ' + str(list[1]))