import hashlib
import time


class Block:
    def __init__(self, index, previous_hash, timestamp, data) -> None:
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        return hashlib.sha256(
            str(self.index).encode()
            + str(self.previous_hash).encode()
            + str(self.timestamp).encode()
            + str(self.data).encode()
        ).hexdigest()


class Blockchain:
    def __init__(self) -> None:
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(0, "0", int(time.time()), "genesis block")

    def add_block(self, data):
        previous_block = self.chain[-1]
        new_index = previous_block.index + 1
        new_timestamp = int(time.time())
        new_hash = previous_block.hash
        new_block = Block(new_index, new_hash, new_timestamp, data)
        self.chain.append(new_block)


if __name__ == "__main__":
    my_blockchain = Blockchain()
    my_blockchain.add_block("transaction 1")
    my_blockchain.add_block("transaction 2")

    for block in my_blockchain.chain:
        print(f"Block #{block.index}")
        print(f"timestamp: {block.timestamp}")
        print(f"data: {block.data}")
        print(f"hash: {block.hash}")
        print(f"previous hash: {block.previous_hash}\n")
