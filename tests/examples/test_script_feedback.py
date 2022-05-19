from unittest import TestCase
from unittest.mock import patch

from examples.script_local_feedback import Main, get_username_from_file, script_main
from models import ChatMessage, Feedback, UserData
from tests.mocks import MockConnection, MockConnectionError
from user.localbitcoin import UserLocalbitcoin

CREDENTIALS = {
            "hmac_key": "Connection should be mocked in each method",
            "hmac_secret":"Connection should be mocked in each method"
            }
USERNAMES = [UserData("Venew2017"), UserData("Avatarplus")]

class TestFeedback(TestCase):
    
    def setUp(self) -> None:
        self.user = UserData("john", "John Doe")
        with patch("examples.script_local_feedback.ConnectionLocalBitcoin") as connection:
            connection.return_value = MockConnection(CREDENTIALS)
            self.main = Main(self.user,CREDENTIALS)
        return super().setUp()

    def test_get_username_from_file(self):
        self.assertEqual(get_username_from_file(
                    "tests/examples/json/feedback.json"), 
                    USERNAMES)

    
    def test_set_feedback_script(self):
        feedback = Feedback("Excellent!", 
                        UserLocalbitcoin.FEEDBACK_POSITIVE)
        
        self.assertIsNone(
            self.main.set_feedback(USERNAMES, feedback)
            )

    def test_cli_feedback(self):
        args = [
            "-k 1234",
            "-s 1234",
            "-n John Doe",
            "-u jd",
            "-f tests/examples/json/feedback.json",
            "-m Excellent!",
            "-p positive",
            ]
        with patch("examples.script_local_feedback.ConnectionLocalBitcoin") as connection:
            connection.return_value = MockConnection(CREDENTIALS)
            self.assertEqual(script_main(args), 0)

        args = [
            "-k 1234",
            "-s 1234",
            "-u jd",
            "-f tests/examples/json/feedback.json",
            "-m Excellent!",
            "-p positive",
            ]
        
        with patch("examples.script_local_feedback.ConnectionLocalBitcoin") as connection:
            connection.return_value = MockConnection(CREDENTIALS)
            self.assertEqual(script_main(args), 0)


    def test_bad_cli(self):
        args = [
            "-s 1234",
            "-n John Doe",
            "-u jd",
            "-f tests/examples/json/feedback.json",
            "-m Excellent!",
            "-p positive",
            ]
        with patch("examples.script_local_feedback.ConnectionLocalBitcoin") as connection:
            connection.return_value = MockConnection(CREDENTIALS)
            with self.assertRaises(SystemExit):
                script_main(args)


        args = [
            "-k 1234",
            "-n John Doe",
            "-u jd",
            "-f tests/examples/json/feedback.json",
            "-m Excellent!",
            "-p positive",
            ]
        with patch("examples.script_local_feedback.ConnectionLocalBitcoin") as connection:
            connection.return_value = MockConnection(CREDENTIALS)
            with self.assertRaises(SystemExit):
                script_main(args)


        args = [
            "-k 1234",
            "-s 1234",
            "-n John Doe",
            "-f tests/examples/json/feedback.json",
            "-m Excellent!",
            "-p positive",
            ]
        with patch("examples.script_local_feedback.ConnectionLocalBitcoin") as connection:
            connection.return_value = MockConnection(CREDENTIALS)
            with self.assertRaises(SystemExit):
                script_main(args)


        args = [
            "-k 1234",
            "-s 1234",
            "-n John Doe",
            "-u jd",
            "-m Excellent!",
            "-p positive",
            ]
        with patch("examples.script_local_feedback.ConnectionLocalBitcoin") as connection:
            connection.return_value = MockConnection(CREDENTIALS)
            with self.assertRaises(SystemExit):
                script_main(args)


        args = [
            "-k 1234",
            "-s 1234",
            "-n John Doe",
            "-u jd",
            "-f tests/examples/json/feedback.json",
            "-p positive",
            ]
        with patch("examples.script_local_feedback.ConnectionLocalBitcoin") as connection:
            connection.return_value = MockConnection(CREDENTIALS)
            with self.assertRaises(SystemExit):
                script_main(args)

        args = [
            "-k 1234",
            "-s 1234",
            "-n John Doe",
            "-u jd",
            "-f tests/examples/json/feedback.json",
            "-m Excellent!",
            ]
        with patch("examples.script_local_feedback.ConnectionLocalBitcoin") as connection:
            connection.return_value = MockConnection(CREDENTIALS)
            with self.assertRaises(SystemExit):
                script_main(args)

    def test_cli_bad_data_feedback(self):
        args = [
            "-k 1234",
            "-s 1234",
            "-n John Doe",
            "-u jd",
            "-f tests/examples/json/bad_feedback.json",
            "-m Excellent!",
            "-p positive",
            ]
        with patch("examples.script_local_feedback.ConnectionLocalBitcoin") as connection:
            connection.return_value = MockConnection(CREDENTIALS)
            self.assertEqual(script_main(args), 1)

    
    def test_cli_bad_file_feedback(self):
        args = [
            "-k 1234",
            "-s 1234",
            "-n John Doe",
            "-u jd",
            "-f tests/examples/json/no_existant.json",
            "-m Excellent!",
            "-p positive",
            ]
        with patch("examples.script_local_feedback.ConnectionLocalBitcoin") as connection:
            connection.return_value = MockConnection(CREDENTIALS)
            self.assertEqual(script_main(args), 1)