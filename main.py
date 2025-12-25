# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import requests
import pandas as pd
import os
import time

OUT_DIR = "data"
OUT_FILE = os.path.join(OUT_DIR, f"technology_top_week.csv")
def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

def scrapper():
    headers = {
        # Reddit blocks many requests without a User-Agent
        "User-Agent": "reddit-tech-scraper/1.0 (by u_yourusername)"
    }
    url = "https://www.reddit.com/r/technology/top/.json?t=week&limit=100"
    resp = requests.get(url, headers=headers, timeout=30)
    resp.raise_for_status()

    payload = resp.json()

    posts = []
    for child in payload["data"]["children"]:
        d = child["data"]
        posts.append({
            "title": d.get("title"),
            "upvotes": d.get("ups"),
            "comments": d.get("num_comments"),
            "author": d.get("author"),
            "created_utc": d.get("created_utc"),
            "permalink": "https://www.reddit.com" + d.get("permalink", ""),
            "url": d.get("url"),
            "score": d.get("score"),
        })

    df = pd.DataFrame(posts)

    df["scraped_at_utc"] = int(time.time())
    return df

def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    df = scrapper()
    df.to_csv(OUT_FILE, index=False, encoding="utf-8")

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    #print_hi('PyCharm')
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
