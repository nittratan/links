# links
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

