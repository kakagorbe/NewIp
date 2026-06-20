import os
import json

def cleanup_output():
    files_to_keep = [
        "best_ips.txt",
        "domains.txt",
        "results.txt",
        "scan_cursor.txt",
        "current_part.txt"
    ]
    
    files_to_limit = {
        "scanned_cache.txt": 10000,
        "tcp_live.txt": 5000,
        "tls_live.txt": 3000,
        "https_live.txt": 2000,
        "fingerprint_results.txt": 2000,
        "live_bank.txt": 10000,
        "ip_bank.txt": 5000,
        "clean_ips.txt": 5000
    }
    
    for f in os.listdir("output"):
        if f.endswith(".tmp"):
            try:
                os.remove(os.path.join("output", f))
            except:
                pass
    
    for f, limit in files_to_limit.items():
        path = os.path.join("output", f)
        if os.path.exists(path):
            try:
                with open(path, "r") as fp:
                    lines = fp.readlines()
                if len(lines) > limit:
                    with open(path, "w") as fp:
                        fp.writelines(lines[-limit:])
            except:
                pass
    
    for f in ["geo_cache.json", "https_meta.json"]:
        path = os.path.join("output", f)
        if os.path.exists(path):
            try:
                with open(path, "r") as fp:
                    data = json.load(fp)
                if isinstance(data, dict) and len(data) > 1000:
                    items = list(data.items())[-1000:]
                    data = dict(items)
                with open(path, "w") as fp:
                    json.dump(data, fp)
            except:
                pass

if __name__ == "__main__":
    cleanup_output()
