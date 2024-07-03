import datetime

# Decorator 
def log_transaction(transaction_type):
    def decorator(func):
        def wrapper(self, *args, **kwargs):    #arguements and kwywordargs
            result = func(self, *args, **kwargs)
            amount = args[0]
            timestamp = datetime.datetime.now()
            self.transactions.append((transaction_type, amount, timestamp))
            return result
        return wrapper
    return decorator

class BankAccount:
    def __init__(self, name, initial_balance):
        self.name = name
        self.balance = initial_balance
        self.transactions = []

    @log_transaction("Credit")
    def deposit(self, amount):
        self.balance += amount

    @log_transaction("Debit")
    def withdraw(self, amount):
        if amount <= self.balance:
            self.balance -= amount
        else:
            print("Insufficient balance")

    def transfer(self, amount, other_account):
        if amount <= self.balance:
            self.balance -= amount
            other_account.balance += amount
            timestamp = datetime.datetime.now()
            self.transactions.append(("Debit", amount, "Transfer to " + other_account.name, timestamp))
            other_account.transactions.append(("Credit", amount, "Received from " + self.name, timestamp))
        else:
            print("Insufficient balance")

    def get_balance(self):
        return self.balance

    def show_transactions(self):
        headers = ["Transaction Type", "Amount", "Description", "Date & Time"]
        print(f"{headers[0]:<15} | {headers[1]:<10} | {headers[2]:<25} | {headers[3]}")
        print("-" * 70)
        for transaction in self.transactions:
            if len(transaction) == 3:
                print(f"{transaction[0]:<15} | {transaction[1]:<10} | {'':<25} | {transaction[2]}")
            else:
                print(f"{transaction[0]:<15} | {transaction[1]:<10} | {transaction[2]:<25} | {transaction[3]}")

accounts = {}

while True:
    print("1. Create Account")
    print("2. Login")
    print("3. Exit")
    choice = input("Enter your choice: ")

    if choice == '1':
        name = input("Enter account holder name: ")
        if name in accounts:
            print("Account already exists.")
        else:
            password = input("Enter password: ")
            initial_balance = float(input("Enter initial deposit: "))
            accounts[name] = {
                'account': BankAccount(name, initial_balance),
                'password': password
            }
            print(f"Account created for {name} with initial balance of ${initial_balance}")

    elif choice == '2':
        name = input("Enter account holder name: ")
        if name in accounts:
            password = input("Enter password: ")
            if accounts[name]['password'] == password:
                print("Login successful")
                while True:
                    print("3. Withdraw Money")
                    print("4. Transfer Money")
                    print("5. Check Balance")
                    print("6. Show Transactions")
                    print("7. Logout")
                    choice = input("Enter your choice: ")

                    if choice == '3':
                        amount = float(input("Enter amount to withdraw: "))
                        accounts[name]['account'].withdraw(amount)
                    elif choice == '4':
                        target_name = input("Enter the name of the account to transfer to: ")
                        if target_name in accounts:
                            amount = float(input("Enter amount to transfer: "))
                            accounts[name]['account'].transfer(amount, accounts[target_name]['account'])
                        else:
                            print("Target account does not exist")
                    elif choice == '5':
                        balance = accounts[name]['account'].get_balance()
                        print(f"Your balance is ${balance}")
                    elif choice == '6':
                        accounts[name]['account'].show_transactions()
                    elif choice == '7':
                        print("Logged out")
                        break
                    else:
                        print("Invalid choice. Please try again.")
            else:
                print("Incorrect password.")
        else:
            print("Account does not exist.")

    elif choice == '3':
        print("Exiting...")
        break

    else:
        print("Invalid choice. Please try again.")
