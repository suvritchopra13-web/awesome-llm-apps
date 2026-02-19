import requests
import json
import time

base_url = "http://127.0.0.1:8000"
test_email = f"py_test_{int(time.time())}@example.com"

def run_test():
    # 1. Register
    print("--- 1. Registering User ---")
    reg_resp = requests.post(f"{base_url}/register", json={"email": test_email})
    api_key = reg_resp.json()["api_key"]
    print(f"API Key: {api_key}")

    # 2. Usage
    print("\n--- 2. Checking Usage ---")
    usage_resp = requests.get(f"{base_url}/usage", headers={"X-Api-Key": api_key})
    print(json.dumps(usage_resp.json(), indent=2))

    # 3. Analyze
    print("\n--- 3. Running Analysis ---")
    print("Please wait (free scraper active)...")
    analyze_resp = requests.post(
        f"{base_url}/analyze",
        headers={"X-Api-Key": api_key},
        json={
            "company_url": "https://marmeto.com",
            "max_competitors": 1,
            "search_engine": "tavily"
        }
    )
    print("\n--- Final Analysis ---")
    print(json.dumps(analyze_resp.json(), indent=2))

if __name__ == "__main__":
    run_test()
