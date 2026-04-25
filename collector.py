import requests
import os

SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_KEY = os.environ["SUPABASE_KEY"]

API = "https://draw.ar-lottery01.com/WinGo/WinGo_1M/GetHistoryIssuePage.json?pageNo=1&pageSize=20"

COLOR_MAP = {
    0: "red-violet", 1: "green", 2: "red", 3: "green", 4: "red",
    5: "green-violet", 6: "red", 7: "green", 8: "red", 9: "green"
}

def get_color(n):
    return COLOR_MAP.get(n, "unknown")

def get_bs(n):
    return "BIG" if n >= 5 else "SMALL"

def get_oe(n):
    return "ODD" if n % 2 != 0 else "EVEN"

def fetch_and_save():
    try:
        res = requests.get(API, timeout=10)
        data = res.json()
        items = data.get("data", {}).get("list", [])

        headers = {
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {SUPABASE_KEY}",
            "Content-Type": "application/json",
            "Prefer": "resolution=ignore-duplicates"
        }

        saved = 0
        for item in items:
            number = int(item.get("number", 0))
            row = {
                "issue": item.get("issueNumber", ""),
                "number": number,
                "big_small": get_bs(number),
                "odd_even": get_oe(number),
                "color": get_color(number)
            }
            r = requests.post(
                f"{SUPABASE_URL}/rest/v1/wingo_1min",
                json=row,
                headers=headers,
                timeout=10
            )
            if r.status_code in [200, 201]:
                saved += 1

        print(f"Saved {saved} new records")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    fetch_and_save()
