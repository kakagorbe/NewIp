import json
import requests
import os

OUTPUT_FILE = "output/ip_bank.txt"

def load_config():
    with open("config.json", "r", encoding="utf-8") as f:
        return json.load(f)

def fetch_source(url):
    try:
        r = requests.get(url, timeout=30)
        if r.ok:
            return r.text.splitlines()
    except:
        pass
    return []

def download_sources():
    cfg = load_config()
    all_ips = set()
    existing_ips = set()
    if os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
            existing_ips = set(line.strip() for line in f if line.strip())
    for url in cfg.get("sources", []):
        new_ips = fetch_source(url)
        all_ips.update(new_ips)
    all_ips.update(existing_ips)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(sorted(all_ips)))

if __name__ == "__main__":
    download_sources()
