import json
import os

class Checkpoint:
    def __init__(self, shard_id, every):
        self.path = f"output/ckpt_{shard_id}.json"
        self.every = every

    def load(self):
        if not os.path.exists(self.path):
            return 0
        try:
            return json.load(open(self.path)).get("i", 0)
        except:
            return 0

    def save(self, i):
        os.makedirs("output", exist_ok=True)
        tmp = self.path + ".tmp"
        with open(tmp, "w") as f:
            json.dump({"i": i}, f)
        os.replace(tmp, self.path)
