import json
from BlockchainCreation import Block, BlockChain, Transaction
import os
from datetime import date


def read_bc_from_file(path):
    with open(path, 'r') as json_file:
        data = json.load(json_file)
    blockchain = BlockChain()
    for i in data:
        block = Block(
            i['index'],
            i['timestamp'],
            i['data'],
            [Transaction(tx['sender'], tx['receiver'], tx['amount']) for tx in i['transactions']],
            i['previousHash'],
        )
        blockchain.chain.append(block)
    blockchain.printBlockChain()
    add_new_block(blockchain, path)


def add_new_block(blockchain, path):

    while 1:
        flag = input("Do you want to add a block?? (y/n)").lower()
        if flag == 'y':
            transaction = []
            inp = 'y'
            while inp == 'y':
                sender, receiver = input("Enter the sender and recipient of the transaction separated by a space: ").split()
                amount = int(input("Enter transaction amount: "))
                transaction.append(Transaction(sender, receiver, amount))
                inp = input('Do you want to add another transaction?? (y/n)').lower()
            data = input("Enter the data you want to add to the block: ")
            blockchain.addBlock(Block(blockchain.lenofchain() - 1, str(date.today()), data, transaction))
            print("Block added!")
            blockchain.saveToJson(path)
        elif flag == 'n':
            break
        else:
            print("Invalid input, please enter n/y.")

        chek = input("Would you like to view the contents of the updated file?? (y/n)").lower()
        if chek == 'y':
            blockchain.printBlockChain()


def main():
    path = input("Enter the name of the json file with the blockchain to which you want to add blocks: ")
    if os.path.isfile(path):
        try:
            read_bc_from_file(path)
        except ValueError:
            print('Error! Invalid data in file.')
    else:
        print('Error! File not found at the specified path.')


if __name__ == '__main__':
    main()