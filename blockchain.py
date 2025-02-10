import hashlib
import time
import json
import datetime

class Block:
    def __init__(self, index, previous_hash, transactions, timestamp=None, nonce=0):
        # Initialize a block with index, previous hash, transactions, timestamp, nonce, and hash
        self.index = index
        self.previous_hash = previous_hash
        self.transactions = transactions
        self.timestamp = timestamp or time.time()
        self.nonce = nonce
        self.hash = self.calculate_hash()  # Hash is calculated without including itself

    def calculate_hash(self):
        # Calculate the hash of the block based on its data
        block_data = {
            'index': self.index,
            'previous_hash': self.previous_hash,
            'transactions': self.transactions,
            'timestamp': self.timestamp,
            'nonce': self.nonce
        }
        block_string = json.dumps(block_data, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def mine_block(self, difficulty):
        # Implement a basic proof-of-work mechanism
        target = '0' * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()  # Recalculate hash with updated nonce
        print(f"Block mined: {self.hash}")

class Blockchain:
    def __init__(self, difficulty=4):
        # Initialize the blockchain with a genesis block and set difficulty
        self.chain = [self.create_genesis_block()]
        self.difficulty = difficulty
        self.pending_transactions = []

    def create_genesis_block(self):
        # Create the genesis block (the first block in the chain)
        return Block(0, "0", ["Genesis Block"], time.time())

    def get_latest_block(self):
        # Get the latest block in the chain
        return self.chain[-1]

    def add_transaction(self, transaction):
        # Add a new transaction to the list of pending transactions
        self.pending_transactions.append(transaction)

    def mine_pending_transactions(self):
        # Mine a new block with the pending transactions
        if not self.pending_transactions:
            print("No transactions to mine.")
            return

        new_block = Block(len(self.chain), self.get_latest_block().hash, self.pending_transactions)
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)
        self.pending_transactions = []

    def is_chain_valid(self):
        # Validate the integrity of the blockchain
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            if current_block.hash != current_block.calculate_hash():
                print(f"Block {current_block.index} hash is invalid!")
                return False

            if current_block.previous_hash != previous_block.hash:
                print(f"Block {current_block.index} previous hash mismatch!")
                return False

        return True

    def print_chain(self):
        # Print the details of each block in the blockchain
        for block in self.chain:
            readable_time = datetime.datetime.fromtimestamp(block.timestamp).strftime('%Y-%m-%d %H:%M:%S') # timestamp converteded to Human redable format
            print(f"Block {block.index} [Hash: {block.hash}, Previous Hash: {block.previous_hash}, Transactions: {block.transactions}, Timestamp: {readable_time}, Nonce: {block.nonce}]")

if __name__ == "__main__":
    my_blockchain = Blockchain()

    print("Adding transactions and mining block 1...")
    my_blockchain.add_transaction("Transaction 1")
    my_blockchain.mine_pending_transactions()

    print("Adding transactions and mining block 2...")
    my_blockchain.add_transaction("Transaction 2")
    my_blockchain.add_transaction("Transaction 3")
    my_blockchain.mine_pending_transactions()

    print("\nBlockchain:")
    my_blockchain.print_chain()

    print("\nIs blockchain valid?", my_blockchain.is_chain_valid())

    print("\nTampering with block 1...")
    my_blockchain.chain[1].transactions = ["Tampered Transaction"]

    print("\nBlockchain after tampering:")
    my_blockchain.print_chain()

    print("\nIs blockchain valid?", my_blockchain.is_chain_valid())
