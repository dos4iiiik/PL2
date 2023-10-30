import json
import os

def print_blockchain(path):
    with open(path, 'r') as json_file:
        data = json.load(json_file)

    for i in data:
        print("Block #" + str(i['index']))
        print("Timestamp #" + i['timestamp'])
        print("Data: " + i['data'])
        print("Block Hash: " + i['hash'])
        print("Block Previous Hash: " + i['previousHash'])
        print("Block Transactions: ")
        for tx in i['transactions']:
            print('\tSender:', tx['sender'], ' -> ', 'Receiver:', tx['receiver'],'| Amount:', tx['amount'])
        print("---------------")

def main():
    path = input("Enter the name of the blockchain file: ")
    if os.path.isfile(path):
        try:
            print_blockchain(path)
        except ValueError:
            print('Error! Invalid data in file.')
    else:
        print('Error! File not found at the specified path.')


if __name__ == '__main__':
    main()






