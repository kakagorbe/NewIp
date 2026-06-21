import os
from cursor import load_cursor, reset_cursor

INPUT_FILE = "output/clean_ips.txt"

def read_count(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return sum(1 for line in f if line.strip())
    except:
        return 0

def total_ips():
    return read_count(INPUT_FILE)

def current_cursor():
    return load_cursor()

def scan_completed():
    total = total_ips()
    if total == 0:
        reset_cursor()
        return True
    cursor = current_cursor()
    if cursor >= total:
        reset_cursor()
        return True
    return False

def progress():
    total = total_ips()
    cursor = current_cursor()
    if total <= 0:
        return {"total": 0, "cursor": cursor, "percent": 0}
    percent = round((cursor / total) * 100, 2)
    if percent > 100:
        percent = 100
    return {"total": total, "cursor": cursor, "percent": percent}

def print_status():
    p = progress()
    print(f'TOTAL={p["total"]} CURSOR={p["cursor"]} PROGRESS={p["percent"]}%')
    if scan_completed():
        print("SCAN COMPLETE")
    else:
        print("SCAN RUNNING")

if __name__ == "__main__":
    print_status()
```

فایل هشتم: livebank.py

```python
import os

LIVE_BANK_FILE = "output/live_bank.txt"

def ensure_output():
    os.                f.write(
                    item + "\n"
                )

        return len(new_items)

    except:
        return 0

def replace_live(items):
    ensure_output()

    data = sorted(
        {
            normalize(x)
            for x in items
            if normalize(x)
        }
    )

    try:
        with open(
            LIVE_BANK_FILE,
            "w",
            encoding="utf-8"
        ) as f:
            f.write(
                "\n".join(data)
            )

        return len(data)

    except:
        return 0

def dedupe_live_bank():
    ensure_output()

    data = sorted(
        read_live_bank()
    )

    try:
        with open(
            LIVE_BANK_FILE,
            "w",
            encoding="utf-8"
        ) as f:
            f.write(
                "\n".join(data)
            )

        return len(data)

    except:
        return 0

def live_count():
    return len(
        read_live_bank()
    )

def read_live_lines():
    return sorted(
        read_live_bank()
    )

def clear_live_bank():
    ensure_output()

    with open(
        LIVE_BANK_FILE,
        "w",
        encoding="utf-8"
    ) as f:
        f.write("")

if __name__ == "__main__":
    count = dedupe_live_bank()

    print(
        f"LIVE={count}"
    )
