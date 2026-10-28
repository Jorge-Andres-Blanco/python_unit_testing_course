import unittest
import os
from src.bank_account import BankAccount
from unittest.mock import patch
from src.exceptions import WithdrawalTimeRestrictionError

class BankAccountTests(unittest.TestCase):

    def setUp(self) -> None:
        self.account = BankAccount(balance_inicial=100, log_file="transaction_log.txt", currency='USD')

    def tearDown(self):
        log_file = self.account.log_file
        if os.path.exists(log_file):
            os.remove(log_file)

    def _count_lines(self, file):
        with open(file, "r") as f:
            return len(f.readlines())

    def test_deposit(self):
        balance = self.account.deposit(100)
        assert balance == 200

    def test_withdraw(self):
        balance = self.account.withdraw(100)
        assert balance == 0

    def test_get_balance(self):
        balance = self.account.get_balance()
        assert balance == 100

    def test_transaction_log(self):
        balance = self.account.get_balance()
        assert os.path.exists("transaction_log.txt")


    def test_count_transactions(self):
        assert self._count_lines(self.account.log_file) == 1
        self.account.deposit(100)
        assert self._count_lines(self.account.log_file) == 2

    
    @unittest.skipUnless(BankAccount.get_usd_to_crc()['response_code'] == 200, 'Response code not 200')
    def test_check_USD_to_CRC(self):
        usd_balance = self.account.balance
        self.account.exchange_USD_to_CRC()

        self.assertEqual(self.account.currency, 'CRC', 'Incorrect final currency')
        self.assertGreaterEqual(self.account.balance, usd_balance, 'USD balance is begger than CRC')

    @patch('src.bank_account.datetime')
    def test_withdraw_during_business_hours(self, mock_datetime):
        
        mock_datetime.now.return_value.hour = 10
        new_balance = self.account.withdraw(100)
        self.assertEqual(new_balance, 0)

    @patch('src.bank_account.datetime')
    def test_withdraw_raises_out_of_business_hours(self, mock_datetime):
            
            mock_datetime.now.side_effect = [unittest.mock.Mock(hour=7), unittest.mock.Mock(hour=18)]
            with self.assertRaises(WithdrawalTimeRestrictionError):
                self.account.withdraw(100)
                self.account.withdraw(100)