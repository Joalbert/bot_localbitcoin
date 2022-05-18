from typing import Dict, List
import argparse

from bot import Bot
from user.localbitcoin import UserLocalbitcoin
from adapters.localbitcoin import AdapterLocalbitcoin
from connection.localbitcoin import ConnectionLocalBitcoin
from models import Feedback, UserData
from helpers import file_to_json


def get_username_from_file(file_path):
    data_json = file_to_json(file_path)
    result = []
    for user in data_json:
        result.append(UserData(user.get("username", "")))
    return result


def parse_arguments(args):
    parser = argparse.ArgumentParser(
                prog="Provide feedback user in file as per cli.")
    parser.add_argument("-k", "--key", 
        help="Key provided by Localbitcoin", required=True)
    parser.add_argument("-s", "--secret", 
        help="Secret provided by Localbitcoin", required=True)
    parser.add_argument("-n", "--name", 
        help="Name in localbitcoin")
    parser.add_argument("-u", "--username", 
        help="username in Localbitcoin", required=True)
    parser.add_argument("-f", "--file", 
        help="Json file with closed order selected to qualify", 
        required=True)
    parser.add_argument("-m", "--message", 
        help="Message for feedback", required=True)
    parser.add_argument("-p", "--points", 
        help="Score for each transaction", required=True)
    return parser.parse_args(args)

class Main:

    def __init__(self, user:UserData, credentials: Dict[str, str]):
        connection = ConnectionLocalBitcoin(credentials)
        adapter = AdapterLocalbitcoin()
        user_for_bot = UserLocalbitcoin(user, connection, adapter)
        self.bot = Bot(user_for_bot, user.name)    
    
    
    def set_feedback(self, users: List[UserData],
                    massive_feedback: Feedback):
        for user in users:
            self.bot.give_feedback(user, massive_feedback)
    
def script_main(argv=None):
    args = parse_arguments(argv)
    name = args.name if args.name else ""
    username = args.username
    
    user = UserData(username, name)
    credential = {"hmac_key":args.key, 
                "hmac_secret":args.secret}
    message = args.message
    score = args.points
    feedback = Feedback(message, score)
    file_path = args.file.strip()
    main = Main(user, credential)
    try:
        users = get_username_from_file(file_path)
    except (FileNotFoundError, Exception) as e:
        print(f"Error {e}")
        return 1
    try:     
        main.set_feedback(users,feedback)
    except (ConnectionError, Exception) as e:
        print(f"Error {e}")
        return 1
    else:
        return 0

if __name__ == "__main__":
    exit(script_main())
