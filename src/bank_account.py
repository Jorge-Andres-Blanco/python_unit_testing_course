import requests

class BankAccount:
    
    def __init__(self, balance_inicial = 0, log_file = None, currency = 'USD'):
        self.balance = balance_inicial
        self.log_file = log_file
        self.currency = currency
        self._log_transaction("Account created")

    @staticmethod
    def get_usd_to_crc():
    
        try:
            response = requests.get("https://open.er-api.com/v6/latest/USD",
                                    timeout=5,
                                    )
            response.raise_for_status()
            
            data = response.json()


        except requests.exceptions.Timeout:
            print("The request timed out.")

        except requests.exceptions.ConnectionError:
            print("Could not connect to the server.")

        except requests.exceptions.HTTPError as e:
            print(f"HTTP error: {e}")

        except requests.exceptions.JSONDecodeError:
            print("The server returned invalid JSON.")

        

        return {'rate': data["rates"]["CRC"], 'response_code': response.status_code}

    def _log_transaction(self, message):
        if self.log_file:
            with open(self.log_file, "a") as f:
                f.write(f"{message}\n")

    def deposit(self, amount):
        if amount>0:
            self.balance += amount
            self._log_transaction(f"Deposited: {amount}. Current Balance: {self.currency} {self.balance}")
        return self.balance

    def withdraw(self, amount):
        if amount>0:
            self.balance -= amount
            self._log_transaction(f"Withdrew: {amount}. Current Balance: {self.currency} {self.balance}")
        return self.balance

    def get_balance(self):
        self._log_transaction(f"Checked balance. Current Balance: {self.currency} {self.balance}")
        return self.balance

    def transfer(self, receiver_account, amount):
        
        if amount > 0 and self.balance > amount:
            receiver_account.deposit(amount)
            self.withdraw(amount)
            self._log_transaction(f"Transferred: {amount}. Current Balance: {self.currency} {self.balance}")

        else:
            raise ValueError("The amount must be higher than the balance and higher than 0")
        return self.balance

    def exchange_CRC_to_USD(self):
        if self.currency == 'CRC':
            ex_rate_USD_to_CRC = self.get_usd_to_crc()['rate']
            new_balance = self.balance / ex_rate_USD_to_CRC
            self.balance = new_balance
            self.currency = 'USD'
            self._log_transaction('Currency exchange from CRC to USD. Current Balance: {self.currency} {self.balance}')
        else:
            print('Currency of account is not CRC')


    def exchange_USD_to_CRC(self):
        if self.currency == 'USD':
            ex_rate_USD_to_CRC = self.get_usd_to_crc()['rate']
            new_balance = self.balance * ex_rate_USD_to_CRC
            self.balance = new_balance
            self.currency = 'CRC'
            self._log_transaction('Currency exchange from USD to CRC. Current Balance: {self.currency} {self.balance}')
        else:
            print('Currency of account is not USD')