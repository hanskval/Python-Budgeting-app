import unittest
from src.DAO.transactionsDAO import TransactionsDAO
from src.database.connection import get_database_connection
from src.database.initialize_database import initialize_database
import src.DAO.userDAO as userDAO


class TestuserDAO(unittest.TestCase):
    def setUp(self):
        initialize_database()
        self.connection = get_database_connection()
        self.transactions_dao = TransactionsDAO(self.connection)
        self.users_dao = userDAO.UserDAO(self.connection)
        self.users_dao.create("testuser", "password123")
        id = self.users_dao.find_by_username("testuser")['id']
        self.transactions_dao.create(
            user_id=id, amount=100.0, category="Salary", description="Monthly salary")

    def test_find_by_user_id(self):
        user = self.users_dao.find_by_username("testuser")
        transactions = self.transactions_dao.find_by_user_id(user['id'])
        self.assertEqual(len(transactions), 1)

    def test_create_transaction(self):
        user = self.users_dao.find_by_username("testuser")
        self.transactions_dao.create(
            user_id=user['id'], amount=-50.0, category="Groceries", description="Weekly groceries")
        transactions = self.transactions_dao.find_by_user_id(user['id'])
        self.assertEqual(len(transactions), 2)
    

    def test_get_balance(self):
        user = self.users_dao.find_by_username("testuser")
        balance = self.transactions_dao.get_balance(user['id'])
        self.assertEqual(balance, 100.0)

    def test_delete_transaction(self):
        user = self.users_dao.find_by_username("testuser")
        transactions = self.transactions_dao.find_by_user_id(user['id'])
        transaction_id = transactions[0]['id']
        self.transactions_dao.delete(transaction_id)
        transactions_after_delete = self.transactions_dao.find_by_user_id(user['id'])
        self.assertEqual(len(transactions_after_delete), 0)