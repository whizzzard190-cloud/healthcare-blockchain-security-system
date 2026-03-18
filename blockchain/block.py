import hashlib
import json
import time

class Blockchain:

    def __init__(self):
        self.chain = []
        self.create_block(previous_hash="0")

    def create_block(self, data=None, previous_hash="0"):
        block = {
            "index": len(self.chain) + 1,
            "timestamp": time.time(),
            "data": data,
            "previous_hash": previous_hash,
            "hash": ""
        }

        block["hash"] = self.hash_block(block)
        self.chain.append(block)

        return block

    def hash_block(self, block):
        block_copy = block.copy()
        block_copy["hash"] = ""
        encoded = json.dumps(block_copy, sort_keys=True).encode()
        return hashlib.sha256(encoded).hexdigest()

    def add_ehr_record(self, ehr_data):
        previous_hash = self.chain[-1]["hash"]
        return self.create_block(data=ehr_data, previous_hash=previous_hash)