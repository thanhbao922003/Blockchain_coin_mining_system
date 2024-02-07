import json
import random

# Dữ liệu blockchain hiện tại
admin_names = ["Dev Coder", "MM Coder","Exchange Coder"]
account_names = ["Thanh Bao Coder", "Tran Ngoc Chinh Coder", "Sai Coder","Nguyen Coder","Nhi Coder"]
DATA = [
    [
       {"from": "", "to": "Dev Coder", "amount": 30000},
       {"from": "", "to": "MM Coder", "amount": 30000},
       {"from": "", "to": "Exchange Coder", "amount": 30000},
    ],
    [
        {"from": "", "to": "Thanh Bao Coder", "amount": 100},
        {"from": "Thanh Bao Coder", "to": "Tran Ngoc Chinh Coder", "amount": 10},
        {"from": "Tran Ngoc Chinh Coder", "to": "Sai Coder", "amount": 5}
    ],
    [
        {"from": "Tran Ngoc Chinh Coder", "to": "Thanh Bao Coder", "amount": 3},
        {"from": "MM Coder", "to": "Thanh Bao Coder", "amount": 50},
        {"from": "Thanh Bao Coder", "to": "Dev Coder", "amount": 5}
    ]
]

# Thêm 10,000 block nữa với mỗi block có 3 giao dịch
for _ in range(10000):
    # Tạo số lượng giao dịch ngẫu nhiên từ 1 đến 4
    num_transactions = random.randint(1,4)

    # Tạo giao dịch ngẫu nhiên
    new_transactions = []
    for _ in range(num_transactions):
        sender = random.choice(admin_names)  # Người gửi ngẫu nhiên
        receiver = random.choice(account_names)  # Người nhận ngẫu nhiên, có thể trùng với người gửi
        amount = random.uniform(1, 1.5)  # Số lượng token ngẫu nhiên

        transaction = {"from": sender, "to": receiver, "amount": amount}
        new_transactions.append(transaction)
    
    # Thêm block mới vào blockchain_data
    DATA.append(new_transactions)

# Lưu vào file JSON
with open('DATA.json', 'w') as json_file:
    json.dump(DATA, json_file, indent=2)

print("Dữ liệu đã được lưu vào blockchain_data.json.")
