import requests
import json
import random
from faker import Faker

faker = Faker()
random.seed(42)

BASE_URL = "http://localhost:8000"
LOG_FILE = "sample_logs/crud_fuzz.jsonl"

ENDPOINTS = [
    ("POST", "/items"),
    ("PUT", "/items/{id}"),
    ("GET", "/items/{id}"),
    ("DELETE", "/items/{id}")
]

def random_item():
    return {
        "name": faker.word(),
        "price": random.choice([faker.pyfloat(), "invalid", -999]),
        "stock": random.randint(-10, 1000),
    }

def call_api(method, path):
    url = BASE_URL + path
    if "{id}" in path:
        url = url.replace("{id}", str(random.randint(1, 999999)))

    payload = None
    if method in ["POST", "PUT"]:
        payload = random_item()

    try:
        resp = requests.request(method, url, json=payload, timeout=10)
        return {
            "ok": True,
            "method": method,
            "url": url,
            "status": resp.status_code,
            "body": resp.text,
            "payload": payload
        }
    except Exception as e:
        return {"ok": False, "error": str(e)}

def main():
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        for _ in range(1000):
            method, ep = random.choice(ENDPOINTS)
            res = call_api(method, ep)
            f.write(json.dumps(res, ensure_ascii=False) + "\n")

if __name__ == "__main__":
    main()
