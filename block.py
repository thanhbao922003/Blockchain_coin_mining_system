import hashlib
import json
from datetime import datetime, timedelta
import random

# tạo một block
class Block:
    def __init__(self,data) :
        self.data = data
        self.prev_hash = ""
        self.nonce = 0
        self.hash = ""
        self.total_time = ""

# tạo hàm băm data với thuật toán sha512
def hash(block):
    data = json.dumps(block.data) + block.prev_hash + str(block.nonce)
    data = data.encode('utf-8')
    return hashlib.sha256(data).hexdigest()
# tạo blockchain la chuoi cac block
class Blockchain:
    def __init__(self,miner) :
        self.miner = miner
        self.chain = [] # genesis block
        self.reward = 50  # Phần thưởng ban đầu
        self.halving_interval = 3000  # Số block giảm phần thưởng


        genesis_block = Block("Geneis Block")
        genesis_block.hash = hash(genesis_block)

        self.chain.append(genesis_block)

    def get_block_subsidy(self, height):
        halvings = height // self.halving_interval
        # Force block reward to zero when right shifting is undefined.
        if halvings >= 64:
            return 0

        # Subsidy is cut in half every halving interval
        n_subsidy = self.reward // (2 ** halvings)
        return n_subsidy

    def add_block(self, data):
         # Kiểm tra giới hạn số lượng token trong một giao dịch
        for transaction in data:
            if transaction["amount"] > 999999:
                print("Transaction amount exceeds the limit (999.999). Block not added.")
                return

        total_transactions = len(data)
        block=Block(data)

        block.data.append({"from":"", "to": self.miner, "amount": self.get_block_subsidy(len(self.chain) - 1) + total_transactions}) # thưởng cho miner khi mã hóa được block

        block.hash = hash(block)
        block.prev_hash = self.chain[-1].hash
        start = datetime.now()  # bắt đầu đếm time
        elapsed_time = timedelta()
        while not hash(block).startswith("0") or elapsed_time < timedelta(seconds=0):
            block.nonce += 1
            block.hash = hash(block)
            elapsed_time = datetime.now() - start
        end = datetime.now()  # ket thuc đếm time
        block.total_time = str(end-start)

        # Kiểm tra số dư của mỗi tài khoản
        if not self.is_balance_valid():
            return
        #  Kiểm tra tổng số token của tất cả các tài khoản và miner
        elif not self.sum_balance_valid():
            return
        else:
            self.chain.append(block)


    def print(self):
      chain_number = 1

      # duyet cac phan tu trong list
      for block in self.chain:
          print('Block number:', chain_number)
          print("Data:", block.data)
          print("Previous hash:", block.prev_hash)
          print("Hash:", block.hash)
          print("Nonce:", block.nonce)
          print("Total time:", block.total_time)
          print("-------------------------------------------------------------------------------------------------------")
          print("")
          chain_number += 1
    def is_valid(self):
        for i in range(1, len(self.chain)):

            current_block = self.chain[i]
            prev_block =  self.chain[i-1]

            if hash(current_block) != current_block.hash:
                return False
            if prev_block.hash != current_block.prev_hash:
                return False
            # check thêm điều kiện
        return True
    def sum_balance_valid(self):
        sum=0
        accounts = set()
        for block in self.chain:
            if isinstance(block.data, list):
                for transaction in block.data:
                    accounts.add(transaction["from"])
                    accounts.add(transaction["to"])
                accounts.discard("")
        for account in accounts:
            balance = self.get_balance(account)
            sum = sum + balance
        if sum >1000000:
                print("Sum of all tokens exceeds the limit (1.000.000). Block not added.")
                self.chain.pop()
                return False
        return True

    def is_balance_valid(self):
        accounts = set()
        for block in self.chain:
            if isinstance(block.data, list):
                for transaction in block.data:
                    accounts.add(transaction["from"])
                    accounts.add(transaction["to"])
                accounts.discard("")
        for account in accounts:

            balance = self.get_balance(account)
            # Kiểm tra số dư của mỗi tài khoản
            if not (0 <= balance <= 1000000):
                print(f"Balance of {account} ({balance} CTC) is not within the valid range (0, 1.000.000). Block not added.")
                self.chain.pop()
                return False
        return True

    def get_balance(self,person):
        balance = 0  # số dư
        for block in self.chain:
            if type(block.data) != list :
                continue
            for transfer in block.data :
                if transfer["from"] == person:   # nếu chuyển đi thì bị trừ tiền
                    balance = balance -transfer["amount"] - random.uniform(0.1, 1)
                if transfer["to"] == person:   # nếu nhận vào thì + tiền
                    balance = balance +transfer["amount"]
        return balance
    def print_all_accounts(self):
        accounts = set()
        total_token = 0
        for block in self.chain:
            if isinstance(block.data, list):
                for transaction in block.data:
                    accounts.add(transaction["from"])
                    accounts.add(transaction["to"])
                accounts.discard("")
        for account in accounts:
            balance = self.get_balance(account)
            total_token = total_token + balance
        account_balances = {account: self.get_balance(account) for account in accounts}
        sorted_account_balances = sorted(account_balances.items(), key=lambda item: item[1], reverse=True)
        print("All Accounts:")
        print(f"Total Token: {total_token} CTC")
        for account, balance in sorted_account_balances:
            print(f"  {account}: {balance} CTC")
        print("-------------------------------------------------------------------------------------------------------")
    def get_accounts(self):
      accounts = set()
      for block in self.chain:
          if isinstance(block.data, list):
              for transaction in block.data:
                  accounts.add(transaction["from"])
                  accounts.add(transaction["to"])
              accounts.discard("")
      return accounts


blockchain = Blockchain("Miner")

# Đọc dữ liệu từ file JSON
with open('DATA.json', 'r') as json_file:
    DATA = json.load(json_file)

# Thêm block từ dữ liệu JSON vào blockchain
for block_transactions in DATA:
    if blockchain.is_balance_valid() == False:
        break
    else:
        blockchain.add_block(block_transactions)

blockchain.print_all_accounts()

blockchain.print()
print("Is valid :", blockchain.is_valid())
