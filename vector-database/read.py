import json

import weaviate

def json_print(data):
    print(json.dumps(data, indent = 2))

client = weaviate.Client(
    url = weaviate_url,                                                     # `weaviate_url`: your Weaviate URL
    auth_client_secret = weaviate.auth.AuthApiKey(weaviate_key),        # `weaviate_key`: your Weaviate API key
    additional_headers = {"X-HuggingFace-Api-Key": hf_api_key}
)

response = client.schema.get("firstproject")

query = (
    client.query.get(
        "firstproject",
        ["answer", "question", "category", "combined_text"]
    )
)

result = query.do()
print(json_print(result["data"]["Get"]))