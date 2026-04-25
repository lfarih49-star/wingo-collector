import requests
import os

SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_KEY = os.environ["SUPABASE_KEY"]

API = "https://draw.ar-lottery01.com/WinGo/WinGo_1M/GetHistoryIssuePage.json?pageNo=1&pageSize=20"

headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "resolution=ignore-duplicates"
}

COLOR_MAP = {
    0: "red-violet", 1: "green", 2: "red", 3: "green", 4: "red",
    5: "green-violet", 6: "red", 7: "green", 8: "red", 9: "green"
}

def fetch_data():
    try:
        res = requests.get(API, timeout=10)
        data = res.json()
        return data.get("data", {}).get("list", [])
    except Exception as e:
        print("API Error:", e)
        return []

def process(item):
    number = int(item.get("number", 0))
    return {
        "issue": item.get("issueNumber", ""),
        "number": number,
        "big_small": "BIG" if number >= 5 else "SMALL",
        "odd_even": "ODD" if number % 2 else "EVEN",
        "color": COLOR_MAP.get(number, "unknown")
    }

def save(rows):
    url = f"{SUPABASE_URL}/rest/v1/wingo_1min"
    res = requests.post(url, json=rows, headers=headers)
    print("Insert status:", res.status_code)
    print("Response:", res.text)

def main():
    items = fetch_data()

    if not items:
        print("No data from API")
        return

    rows = [process(i) for i in items]

    print(f"Fetched {len(rows)} items")
    save(rows)

if __name__ == "__main__":
    main()
