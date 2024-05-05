import requests

API_URL = "https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-8B"
API_TOKEN = "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"
headers = {"Authorization": f"Bearer {API_TOKEN}"}

def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()
	
output = query({
	"inputs": "Can you please let us know more details about your ",
})
print(output)