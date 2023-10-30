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
        flag = input("Хотите добавить блок? (y/n)").lower()
        if flag == 'y':
            transaction = []
            inp = 'y'
            while inp == 'y':
                sender, receiver = input("Введите отправителя, получателя транзакции через пробел: ").split()
                amount = int(input("Введите сумму транзакции: "))
                transaction.append(Transaction(sender, receiver, amount))
                inp = input('Хотите добавить еще одну транзакцию? (y/n)').lower()
            data = input("Веедите данные, которые вы хотите добавить в блок: ")
            blockchain.addBlock(Block(blockchain.lenofchain() - 1, str(date.today()), data, transaction))
            print("Блок добавлен!")
            blockchain.saveToJson(path)
        elif flag == 'n':
            break
        else:
            print("Некорректный ввод, введите n/y.")

        chek = input("Хотиет просмотреть содержимое обновленного файла? (y/n)").lower()
        if chek == 'y':
            blockchain.printBlockChain()


def main():
    path = input("Введите название json-файла, "
                 "где хранится блокчейн, "
                 "в который необходимо добавить блоки: ")
    if os.path.isfile(path):
        try:
            read_bc_from_file(path)
        except ValueError:
            print('Error! Invalid data in file.')
    else:
        print('Error! File not found at the specified path.')



if __name__ == '__main__':
    main()