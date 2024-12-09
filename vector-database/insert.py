import json

import requests

import weaviate

def json_print(data):
    print(json.dumps(data, indent = 2))

resp = requests.get("https://raw.githubusercontent.com/weaviate-tutorials/quickstart/main/data/jeopardy_tiny.json")
data = json.loads(resp.text)

client = weaviate.Client(
    url = weaviate_url,                                                     # `weaviate_url`: your Weaviate URL
    auth_client_secret = weaviate.auth.AuthApiKey(weaviate_key),            # `weaviate_key`: your Weaviate API key
    additional_headers = {"X-HuggingFace-Api-Key": hf_api_key}
)

class_obj = {
    "class": "firstproject",
    "vectorizer": "text2vec-huggingface",
    "moduleConfig": {
        "text2vec-huggingface": {
        "model": "sentence-transformers/all-MiniLM-L6-v2"
        }
    },
    "vectorIndexType": "flat", # https://weaviate.io/developers/weaviate/concepts/vector-index
     "properties": [
        {"name": "answer", "dataType": ["text"]},
        {"name": "question", "dataType": ["text"]},
        {"name": "category", "dataType": ["text"]},
        {"name": "combined_text", "dataType": ["text"]}
    ]
}

if client.schema.exists("firstproject"):
   client.schema.delete_class("firstproject")
 
client.schema.create_class(class_obj)

with client.batch.configure(batch_size = 5) as batch:
    for i, d in enumerate(data):
        properties = {
            "answer": d["Answer"],
            "question": d["Question"],
            "category": d["Category"],
            "combined_text": d["Question"] + " " + d["Answer"]
        }

        combined_text = d["Question"] + " " + d["Answer"]

        # uuid = weaviate.util.generate_uuid5(properties["combined_text"])

        batch.add_data_object(
            data_object = properties,
            class_name = "firstproject",
            # uuid = uuid
        )

response = (
    client.query
    .get("firstproject", ["question", "answer"])
    .with_near_text({"concepts": ["animal"]})
    .with_additional(["vector"])
    .with_limit(2)
    .do()
)

print(json_print(response))

response = (
    client.query
    .get("firstproject", ["question", "answer"])
    .with_bm25(query = "animal")
    .with_additional(["vector"])
    .with_limit(3)
    .do()
)

print(json_print(response))

response = (
    client.query
    .get("firstproject", ["question", "answer"])
    .with_hybrid(query = "animal", alpha = 0.5)
    .with_additional(["vector"])
    .with_limit(3)
    .do()
)

print(json_print(response))