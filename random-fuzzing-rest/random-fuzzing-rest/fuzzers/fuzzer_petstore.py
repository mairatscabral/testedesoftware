import requests
import json
import random
import time
import hashlib
from faker import Faker
from concurrent.futures import ThreadPoolExecutor, as_completed

faker = Faker()
random.seed(42)
Faker.seed(42)

BASE_URL = "https://petstore.swagger.io/v2"
LOG_FILE = "sample_logs/petstore_fuzz.jsonl"

ENDPOINTS = [
    ("POST", "/pet"),
    ("PUT", "/pet"),
    ("GET", "/pet/{id}"),
    ("DELETE", "/pet/{id}")
]

TOTAL_REQUESTS = 1500
CONCURRENCY = 10
TIMEOUT = 10

def random_pet():
    return {
        "id": random.randint(1, 5_000_000),
        "name": faker.first_name(),
        "photoUrls": [faker.uri() for _ in range(random.randint(0, 3))],
        "status": random.choice([
            "available", "pending", "sold",
            123, None, {"unexpected": True}
        ])
    }

def fingerprint(status, body):
    return hashlib.sha1(f"{status}|{body[:500]}".encode()).hexdigest()

def call_api(session, method, endpoint):
    url = BASE_URL + endpoint

    if "{id}" in endpoint:
        url = url.replace("{id}", str(random.randint(1, 3_000)))

    json_body = None
    if method in ["POST", "PUT"]:
        json_body = random_pet()

    try:
        resp = session.request(method, url, json=json_body, timeout=TIMEOUT)
        return {
            "ok": True,
            "method": method,
            "url": url,
            "status": resp.status_code,
            "body": resp.text,
            "payload": json_body
        }
    except Exception as e:
        return {"ok": False, "error": str(e), "url": url, "method": method}

def is_failure(res):
    if not res["ok"]:
        return True
    return 500 <= res["status"] <= 599

def main():
    failures = {}

    with open(LOG_FILE, "w", encoding="utf-8") as f,             ThreadPoolExecutor(max_workers=CONCURRENCY) as ex,             requests.Session() as session:

        futures = []
        for _ in range(TOTAL_REQUESTS):
            method, path = random.choice(ENDPOINTS)
            futures.append(ex.submit(call_api, session, method, path))

        for future in as_completed(futures):
            res = future.result()
            f.write(json.dumps(res, ensure_ascii=False) + "\n")

            if is_failure(res):
                fp = fingerprint(res.get("status", "EXC"), res.get("body", ""))
                if fp not in failures:
                    failures[fp] = 0
                failures[fp] += 1

    print("Total falhas únicas:", len(failures))

if __name__ == "__main__":
    main()
