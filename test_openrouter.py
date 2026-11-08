"""
OpenRouter API Connection & Model Tester.
Run: python test_openrouter.py
"""

import json
import urllib.error
import urllib.request

from config import OPENROUTER_API_KEY, OPENROUTER_MODEL


def test_connection():
    if not OPENROUTER_API_KEY:
        print("❌ OPENROUTER_API_KEY is not set in config.py")
        return False

    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "HTTP-Referer": "http://localhost:8501",
        "X-Title": "AI Video Studio",
    }
    payload = {
        "model": OPENROUTER_MODEL,
        "messages": [
            {
                "role": "user",
                "content": "Write a dramatic 1-sentence opening hook about the deep ocean.",
            }
        ],
    }

    print(f"Testing OpenRouter API with model: {OPENROUTER_MODEL}...")
    try:
        req = urllib.request.Request(
            url, data=json.dumps(payload).encode("utf-8"), headers=headers
        )
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            content = data["choices"][0]["message"]["content"].strip()
            print("\n✅ Connection Successful!")
            print(f"Narrative Hook: \"{content}\"")
            return True
    except urllib.error.HTTPError as e:
        print(f"❌ HTTP Error {e.code}: {e.read().decode('utf-8')}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


if __name__ == "__main__":
    test_connection()

