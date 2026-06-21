# downloader.py
import json
import requests
import os

OUTPUT_FILE = "output/ip_bank.txt"
CURSOR_FILE = "output/source_cursor.txt"

def load_config():
    with open("config.json", "r", encoding="utf-8") as f:
        return json.load(f)

def ensure_output():
    os.makedirs("output", exist_ok=True)

def load_cursor():
    ensure_output()
    if not os.path.exists(CURSOR_FILE):
        return 0
    try:
        with open(CURSOR_FILE, "r", encoding="utf-8") as f:
            return int(f.read().strip())
    except:
        return 0

def save_cursor(value):
    ensure_output()
    with open(CURSOR_FILE, "w", encoding="utf-8") as f:
        f.write(str(value))

def fetch_source(url):
    try:
        r = requests.get(url, timeout=30)
        if r.ok:
            lines = r.text.splitlines()
            return [x.strip() for x in lines if x.strip()]
    except:
        pass
    return []

def download_sources():
    cfg = load_config()
    sources = cfg.get("sources", [])
    ips_per_source = cfg.get("ips_per_source", 10000)
    cursor = load_cursor()
    
    if cursor >= len(sources):
        cursor = 0
        save_cursor(0)
    
    source_url = sources[cursor] if cursor < len(sources) else sources[0]
    all_ips = fetch_source(source_url)
    all_ips = all_ips[:ips_per_source]
    
    next_cursor = cursor + 1
    if next_cursor >= len(sources):
        next_cursor = 0
    
    save_cursor(next_cursor)
    
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(all_ips))
    
    print(f"SOURCE={source_url} IPS={len(all_ips)} CURSOR={cursor}->{next_cursor}")

if __name__ == "__main__":
    download_sources()
