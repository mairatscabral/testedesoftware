import requests
import json
import random
from faker import Faker
from requests.auth import HTTPBasicAuth

faker = Faker()
random.seed(42)

BASE_URL = "http://localhost:8000"  # ajuste se usar outra API
LOG_FILE = "sample_logs/auth_fuzz.jsonl"

AUTH = HTTPBasicAuth("admin", "admin123")

ENDPOINTS = [
    ("GET", "/items/{id}"),
    ("POST", "/items"),
]

def random_payload():
    return {
        "name": faker.word(),
        "price": faker.pyfloat(),
        "stock": random.randint(0, 300)
    }

def main():
    with open(LOG_FILE, "w", encoding='utf-8') as f:
        for _ in range(800):
            method, ep = random.choice(ENDPOINTS)
            url = BASE_URL + ep.replace("{id}", str(random.randint(1, 999999)))

            payload = random_payload() if method == "POST" else None
            try:
                resp = requests.request(
                    method, url, json=payload, auth=AUTH, timeout=10
                )
                f.write(json.dumps({
                    "status": resp.status_code,
                    "url": url,
                    "payload": payload,
                    "body": resp.text
                }, ensure_ascii=False) + "\n")
            except Exception as e:
                f.write(json.dumps({"error": str(e)}, ensure_ascii=False) + "\n")

if __name__ == "__main__":
    main()
