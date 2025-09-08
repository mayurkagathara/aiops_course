import requests
import json
import os 
from dotenv import load_dotenv
load_dotenv()

OLLAMA_URL = "http://localhost:11434/api/generate"
#MODEL_NAME = "gemma:2b-instruct"
MODEL_NAME = "qwen2.5:1.5b"


def query_llm_offline(prompt: str) -> str:
  payload = {
    "model": MODEL_NAME,
    "prompt": prompt,
    "stream": False,
    "temperature": 0.2,
  }
  print(payload)
  try:
    response = requests.post(OLLAMA_URL, json=payload, timeout=600)
    response.raise_for_status()
    return response.json()["response"]
  except Exception as e:
    return f"LLM error: {str(e)}"

def query_llm_openrouter(prompt: str) -> str:
  response = requests.post(
    url="https://openrouter.ai/api/v1/chat/completions",
    headers={
      "Authorization": "Bearer " + os.getenv('OPENROUTER_API_KEY')
    },
    data=json.dumps({
      "model": "z-ai/glm-4.5-air:free", # Optional
      "messages": [
        {
          "role": "user",
          "content": prompt
        }
      ]
    })
  )
  try:
    return response.json()['choices'][0]['message']['content']
  except:
    return "Problem running the LLM" + response.text

query_llm = lambda prompt: query_llm_offline(prompt)