import os
import json
import time

class Exporter:
    @staticmethod
    def save(items, shard_id):
        os.makedirs("output", exist_ok=True)
        path = f"output/stream_{shard_id}.log"
        now = time.time()
        with open(path, "w") as f:
            for ip, port, score in items:
                f.write(json.dumps({
                    "ip": ip, 
                    "port": port, 
                    "score": score,
                    "expiry": now + (7 * 24 * 3600)
                }) + "\n")
