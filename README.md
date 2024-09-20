# links
https://tanaypratap.notion.site/bytr-brochure-6eca974ac9b5413fb5bbcbbd21195242
[My Drive Link](https://drive.google.com/drive/folders/1MWg0PLcXU5NQ7u4gFQ09MPXt3xrc2HmK?usp=sharing)

[Roadmap](https://roadmap.sh/)
[Bigdata](https://github.com/datastacktv/data-engineer-roadmap)
[links](https://github.com/thapatechnical/reactfirebaseYoutube/)

import json

def write_json_file(data, filename):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

# Example usage:
data = [
    {"name": "Alice", "age": 30},
    {"name": "Bob", "age": 25},
    {"name": "Charlie", "age": 35}
]

write_json_file(data, 'output.json')




import json

def text_to_json(text_file_path):
    data = {}
    with open(text_file_path, 'r') as file:
        current_claim = None
        for line_number, line in enumerate(file, start=1):
            line = line.strip()
            if line.startswith('*'):
                if current_claim:
                    data[current_claim['Claim']] = current_claim
                current_claim = {'Claim': line.lstrip('*')}
            else:
                parts = line.split(':')
                if len(parts) == 2:
                    key, value = parts
                    current_claim[key.strip()] = value.strip()
                else:
                    print(f"Error: Invalid format in line {line_number}: {line}")

        # Add the last claim
        if current_claim:
            data[current_claim['Claim']] = current_claim

    return data

# Example usage:
text_file_path = 'data.txt'
json_data = text_to_json(text_file_path)

# Print or save JSON data
print(json.dumps(json_data, indent=4))

# If you want to save the JSON data to a file, uncomment the following lines:
# with open('output.json', 'w') as json_file:
#     json.dump(json_data, json_file, indent=4)

