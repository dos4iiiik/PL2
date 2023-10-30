import json
import hashlib


# Класс для добавления транзакций к блокам
class Transaction:
    def __init__(self, sender, receiver, amount):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount

    def __dict__(self):
        return {
            "sender": self.sender,
            "receiver": self.receiver,
            "amount": self.amount
        }

    def __str__(self):
        return f"   Sender: {self.sender} -> Receiver: {self.receiver} | Amount: {self.amount} "


class Block:
    def __init__(self, index, timestamp, data,  transactions, previousHash = ''):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previousHash = previousHash
        self.transactions = transactions
        self.hash = self.calculateHash()

    def __dict__(self):
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "hash": self.hash,
            "previousHash": self.previousHash,
            "transactions": [tx.__dict__() for tx in self.transactions]
        }

    def calculateHash(self):
        return hashlib.sha256((str(self.index) + self.previousHash + self.timestamp + self.data +
                               json.dumps([tx.__dict__() for tx in self.transactions])).encode('utf-8')).hexdigest()

    def printBlock(self):
        print("Block #" + str(self.index))
        print("Timestamp #" + str(self.timestamp))
        print("Data: " + str(self.data))
        print("Block Hash: " + str(self.hash))
        print("Block Previous Hash: " + str(self.previousHash))
        print("Block Transactions: ")
        print(*[tx.__str__() for tx in self.transactions], sep='\n')
        print("---------------")


class BlockChain:
    def __init__(self):
        self.chain = [self.createGenesisBlock()]

    def createGenesisBlock(self):
        return Block(0, "04/10/2023", "Genesis Block",
                     [Transaction("Genesis", "Genesis", 0)], '0')

    def getLatestBlock(self):
        return self.chain[len(self.chain) - 1]

    def lenofchain(self):
        return len(self.chain)

    def addBlock(self, newBlock):
        newBlock.previousHash = self.getLatestBlock().hash
        newBlock.hash = newBlock.calculateHash()
        self.chain.append(newBlock)

    def isChainValid(self):
        for i in range(1, len(self.chain)):
            currentBlock = self.chain[i]
            previousBlock = self.chain[i - 1]
            # checks whether data has been tampered with
            if currentBlock.hash != currentBlock.calculateHash():
                return False
            if currentBlock.previousHash != previousBlock.hash:
                return False
            return True

    def printBlockChain(self):
        for i in range(1, len(self.chain)):
            self.chain[i].printBlock()

    def saveToJson(self, path):
        blocks_list = []
        with open(path, 'w') as outfile:
            for block in self.chain:
                blocks_list.append(block.__dict__())
            json.dump(blocks_list, outfile, indent=4)


def main():
    testChain = BlockChain()

    testChain.addBlock(Block(1, "01/10/2023", "One",
                             [Transaction("BG", "Telonus", 100),
                              Transaction("Drizzy", "Telonus", 200)]))
    testChain.addBlock(Block(2, "02/10/2023", "Two",
                             [Transaction("Super", "Beast", 1300),
                              Transaction("Frank", "Prody", 800),]))
    testChain.addBlock(Block(3, "03/10/2023", "Three", [Transaction("Kanye",
                                                                  "Khalid", 1500)]))
    testChain.addBlock(Block(4, "04/10/2023", "Four", [Transaction("Di",
                                                                 "Drizzy", 400000)]))
    testChain.printBlockChain()
    # no tampering in our block chain yet so should be true here
    print("Chain valid? " + str(testChain.isChainValid()))
    path = input("Введите название для json-файла, куда будет сохранен блокчейн: ")
    testChain.saveToJson(path)


# Only run the main() function, if this is the root script running.
# This allows importing this script file to use its functions inside other scripts.
if __name__ == '__main__':
    main()

