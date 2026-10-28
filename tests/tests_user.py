import unittest
import os
from faker import Faker
from src.user import User
from src.bank_account import BankAccount

class UserTests(unittest.TestCase):
    
    def setUp(self) -> None:
        self.faker = Faker(locale="en")
        self.user = User(name=self.faker.name(), email=self.faker.email())

    def test_user_creation(self):
        
        gen_name = self.faker.name()
        gen_email = self.faker.email()

        user = User(name=gen_name, email=gen_email)

        self.assertEqual(user.name, gen_name)
        self.assertEqual(user.email, gen_email)


    def test_user_multiple_accounts(self):

        for _ in range(3):
            bank_account = BankAccount(
            balance_inicial= self.faker.random_int(min = 100, max = 2000, step = 50),
            log_file = self.faker.file_name(extension=".txt"),
            currency= 'USD'
            )
            self.user.add_account(account=bank_account)

        expected_value = self.user.get_total_balance()
        value = sum(account.get_balance() for account in self.user.accounts)

        self.assertEqual(value, expected_value)

    def tearDown(self):

        for account in self.user.accounts:
            os.remove(account.log_file)
