import requests 
import json 
import ollama

url = "http://localhost:11434/api/chat"
model = "llama3.2:1b"
prompt = "What is Python Programming?"

payload = {
    "model": model, 
    "messages": [{"role": "user", "content": prompt}]
}
response = requests.post(url, json=payload, stream=True)

if response.status_code ==200: 
    for line in response.iter_lines(decode_unicode=True): 
        print(json.loads(line)["message"]["content"], end="")

# client = ollama.Client()
# response = client.generate(model=model, prompt=prompt)
# print(response.response)