from typing import Dict, List
import argparse

from bot import Bot
from user.localbitcoin import UserLocalbitcoin
from adapters.localbitcoin import AdapterLocalbitcoin
from connection.localbitcoin import ConnectionLocalBitcoin
from models import UserData, Chat, ChatMessage
from helpers import file_to_json

def parse_arguments(args):
    parser = argparse.ArgumentParser(
                prog="Greet opened order in Localbitcoin.")
    parser.add_argument("-k", "--key", 
            help="Key provided by Localbitcoin", required=True)
    parser.add_argument("-s", "--secret", 
            help="Secret provided by Localbitcoin", required=True)
    parser.add_argument("-n", "--name", 
            help="Name in localbitcoin")
    parser.add_argument("-u", "--username", 
            help="username in Localbitcoin", required=True)
    parser.add_argument("-f", "--file", 
            help="Json file with greet for Users", required=True)
    return parser.parse_args(args)


def get_greeting_from_file(file_path, username):
    greet_json = file_to_json(file_path)
    greetings = []
    for id, greet in enumerate(greet_json):
        greetings.append(ChatMessage(id, username, greet["greet"]))
    return greetings


class Main:

    def __init__(self, user:UserData, credentials: Dict[str, str]):
        connection = ConnectionLocalBitcoin(credentials)
        adapter = AdapterLocalbitcoin()
        user_for_bot = UserLocalbitcoin(user, connection, adapter)
        self.bot = Bot(user_for_bot, user.name)    
    
    def greet_all_open_order(self, greeting:List[ChatMessage]):
        opened_orders = self.bot.read_opened_order()
        for order in opened_orders:
            chat = Chat(order.chat_id)
            messages = self.bot.read_messages(chat)
            self.bot.welcome_message_chat(chat, messages, greeting)

    
def script_main(argv=None):
    
    args = parse_arguments(argv)
    
    name = args.name if args.name else ""
    username = args.username
    file_path = args.file.strip()
    hkey =args.key
    hsecret = args.secret
    credential = {"hmac_key":hkey, "hmac_secret":hsecret}
    user = UserData(username, name)
    main = Main(user, credential)
    try:
        greetings = get_greeting_from_file(file_path, username)
    except (FileNotFoundError) as e:
        print(f"File Error: {e}")
        return 1
    except (KeyError) as e:
        print(f'Key Error: {e}, it should be "greeting"')
        return 1
    except (Exception) as e:
        print(f"Error: {e}")
        return 1
    try:
        main.greet_all_open_order(greetings)
    except (ConnectionError, Exception) as e:
        print(f"Error {e}")
        return 1
    else: 
        return 0
    

if __name__ == "__main__":
    exit(script_main())
