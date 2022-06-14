import json


with open('Commands.json', 'r') as json_file:
    json_object = json.load(json_file)


print(json.dumps(json_object, indent=4, ensure_ascii=False, separators =("", " = ")))

print(json_object.keys())