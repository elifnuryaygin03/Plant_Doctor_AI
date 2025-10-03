import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL_URL = "https://api.groq.com/openai/v1/chat/completions"

def query_llm(prompt: str, max_tokens: int = 250):
    """Kullanıcının sorusunu LLM API'ye gönderir ve 4 alanlı function call JSON döndürür."""
    if not GROQ_API_KEY:
        return {"hata": "GROQ_API_KEY bulunamadı"}
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "meta-llama/llama-4-scout-17b-16e-instruct",
        "messages": [
            {"role": "system", "content": "Sen bir bitki doktorusun. Kullanıcıdan gelen sorunlara function call ile aşağıdaki JSON alanlarını tek seferde döndür:\nsorun (kısa açıklama), nedenler (liste), cozum_onerileri (liste), bakim_onerileri (liste)"},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": max_tokens,
        "temperature": 0.7,
        "function_call": {"name": "bitki_analizi"},
        "functions": [
            {
                "name": "bitki_analizi",
                "description": "Bitki sorunlarını analiz eder ve bakım önerileri sunar.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "sorun": {"type": "string"},
                        "nedenler": {"type": "array", "items": {"type": "string"}},
                        "cozum_onerileri": {"type": "array", "items": {"type": "string"}},
                        "bakim_onerileri": {"type": "array", "items": {"type": "string"}}
                    },
                    "required": ["sorun", "nedenler", "cozum_onerileri", "bakim_onerileri"]
                }
            }
        ]
    }
    try:
        response = requests.post(MODEL_URL, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        result = response.json()
        if "choices" in result and result["choices"]:
            function_call = result["choices"][0]["message"].get("function_call")
            if function_call:
                return json.loads(function_call["arguments"])
        return {"hata": f"Beklenmeyen LLM API yanıtı: {result}"}
    except Exception as err:
        return {"hata": str(err)}