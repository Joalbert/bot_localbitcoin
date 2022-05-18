from unittest import TestCase
from unittest.mock import patch

from examples.script_greet import Main, get_greeting_from_file, script_main
from models import ChatMessage, UserData
from tests.mocks import MockConnection, MockConnectionError

CREDENTIALS = {
            "hmac_key": "Connection should be mocked in each method",
            "hmac_secret":"Connection should be mocked in each method"
            }

class TestGreet(TestCase):
    
    def setUp(self) -> None:
        self.user = UserData("john", "John Doe")
        with patch("examples.script_greet.ConnectionLocalBitcoin") as connection:
            connection.return_value = MockConnection(CREDENTIALS)
            self.main = Main(self.user,CREDENTIALS)
        self.MESSAGES = [
            ChatMessage(0,self.user.username, 
                        "Hello!"),
            ChatMessage(1,self.user.username, 
                        "Hi!"),
            ChatMessage(2,self.user.username, 
                        "Top of the morning to you!")
            ]
        return super().setUp()

    def test_get_greeting_from_file(self):
        
        self.assertEqual(get_greeting_from_file(
                    "tests/examples/json/greeting.json", 
                    self.user.username), 
                    self.MESSAGES)

    def test_greet_all_opened_order(self):
        self.assertIsNone(
            self.main.greet_all_open_order(self.MESSAGES))

        with patch("examples.script_greet.ConnectionLocalBitcoin") as connection:
            connection.return_value = MockConnectionError(CREDENTIALS)
            main = Main(self.user, CREDENTIALS) 
            with self.assertRaises(ConnectionError):
                main.greet_all_open_order(self.MESSAGES)

    def test_cli(self):
        args = [
            "-k 1234",
            "-s 1234",
            "-n John Doe",
            "-u jd",
            "-f tests/examples/json/greeting.json",
            ]
        with patch("examples.script_greet.ConnectionLocalBitcoin") as connection:
            connection.return_value = MockConnection(CREDENTIALS)
            self.assertEqual(script_main(args), 0)

        args = [
            "-k 1234",
            "-s 1234",
            "-u jd",
            "-f tests/examples/json/greeting.json",
            ]

        with patch("examples.script_greet.ConnectionLocalBitcoin") as connection:
            connection.return_value = MockConnection(CREDENTIALS)
            self.assertEqual(script_main(args), 0)


    def test_bad_cli(self):
        args = [
            "-s 1234",
            "-n John Doe",
            "-u jd",
            "-f tests/examples/json/greeting.json",
            ]
        with patch("examples.script_greet.ConnectionLocalBitcoin") as connection:
            connection.return_value = MockConnection(CREDENTIALS)
            with self.assertRaises(SystemExit):
                script_main(args)


        args = [
            "-k 1234",
            "-n John Doe",
            "-u jd",
            "-f tests/examples/json/greeting.json",
            ]
        with patch("examples.script_greet.ConnectionLocalBitcoin") as connection:
            connection.return_value = MockConnection(CREDENTIALS)
            with self.assertRaises(SystemExit):
                script_main(args)


        args = [
            "-k 1234",
            "-s 1234",
            "-n John Doe",
            "-f tests/examples/json/greeting.json",
            ]
        with patch("examples.script_greet.ConnectionLocalBitcoin") as connection:
            connection.return_value = MockConnection(CREDENTIALS)
            with self.assertRaises(SystemExit):
                script_main(args)


        args = [
            "-k 1234",
            "-s 1234",
            "-n John Doe",
            "-u jd",
            ]
        with patch("examples.script_greet.ConnectionLocalBitcoin") as connection:
            connection.return_value = MockConnection(CREDENTIALS)
            with self.assertRaises(SystemExit):
                script_main(args)
