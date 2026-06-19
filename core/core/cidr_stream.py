import random

class CIDRStream:
    def __init__(self, cidrs, limit):
        self.cidrs = cidrs
        self.limit = limit

    def stream(self):
        random.shuffle(self.cidrs)

        per_source = {}

        for cidr in self.cidrs:
            src = cidr.split("/")[0]

            if src not in per_source:
                per_source[src] = []

            if len(per_source[src]) >= self.limit:
                continue

            ip = self._fake_expand(cidr)
            per_source[src].append(ip)

            yield ip

    def _fake_expand(self, cidr):
        base = cidr.split("/")[0].split(".")
        return ".".join(base[:3] + [str(random.randint(1, 254))])
