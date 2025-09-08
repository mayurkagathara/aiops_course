import requests

def ask_llm_ollama(prompt, model="qwen2.5:1.5b"):
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": model, "prompt": prompt, "stream": False}
        )
        response.raise_for_status()
        return response.json()["response"]
    except Exception as e:
        return f"[EXCEPTION]: {str(e)}"
