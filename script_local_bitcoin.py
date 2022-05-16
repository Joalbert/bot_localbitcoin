from typing import Dict, List
from decimal import Decimal
import argparse

from bot import Bot
from user.localbitcoin import UserLocalbitcoin
from adapters.localbitcoin import AdapterLocalbitcoin
from connection.localbitcoin import ConnectionLocalBitcoin
from models import Feedback, UserData, Chat, Order, ChatMessage, Ad
from helpers import file_to_json

def parse_arguments(args):
    parser = argparse.ArgumentParser(
                prog="Cleaned directory in Dropbox.")
    parser.add_argument("-k", "--key", 
            help="Key provided by Localbitcoin", required=True)
    parser.add_argument("-s", "--secret", 
            help="Secret provided by Localbitcoin", required=True)
    parser.add_argument("-b", "--buy", 
                        help="Ads to update are buy publications",
                        action="store_true")
    parser.add_argument("-s", "--sell", 
                        help="Ads to update are sell publications",
                        action="store_true")
    parser.add_argument("-f", "--file", 
                        help="File json with Ads info for partners")

    
    return parser.parse_args(args)

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

    def get_ads(self):
        if not self.ads:
            self.ads = self.bot.read_my_ads()
        return self.ads

    def define_rivals(self, my_ad:Ad, ads:List[Ad]):
        return self.bot.filter_list_ads(
            my_ad.minimum_value, my_ad.maximum_value, ads)

    def update_price(self, ad, amount):
        self.bot.update_price_ads(own_ad=ad, amount=amount)

    def change_all_prices(self, amount_below:Decimal, 
            publication_list: List[Ad], partner_ads: List[Ad],
            is_reducing:bool):
        ads = self.get_ads()
        no_competition = ads.extend(partner_ads)    
        competition_list = self.bot.remove_own_ads(publication_list, 
                                no_competition)
        for ad in ads:
            competitors_in_my_range = self.define_rivals(ad, competition_list)
            if(is_reducing):
                change_price = self.bot.get_smaller_price(competitors_in_my_range)
            if(not is_reducing):
                change_price = self.bot.get_bigger_price(competitors_in_my_range) 
            self.update_price(ad, change_price+amount_below)

    
    def set_feedback(self, massive_feedback: Feedback):
        closed_orders = self.bot.read_closed_order()
        for order in closed_orders:
            if(self.bot.user.get_username()==order.buyer):
                self.bot.give_feedback(order.seller, massive_feedback)
            else:
                self.bot.give_feedback(order.buyer, massive_feedback)
    
    def read_buy_publication(self,**kwargs):
        return self.bot.read_buy_ads(**kwargs)

    def read_sell_publication(self,**kwargs):
        return self.bot.read_sell_ads(**kwargs)

    def set_partners_ads(self, partner_json):
        self.partners_ads

    def get_partners_ads(self):
        return self.partners_ads

def script_main(argv=None):
    args = parse_arguments(argv)
    name = input("Write your name")
    username = input("Write your username")
    amount = input("Please, introduce amount you would like to increase/reduce")
    
    if args.buy:
        ads = main.read_buy_publication()
    
    if args.sell:
        ads = main.read_sell_publication()
    
    
    user = UserData(username, name)
    credential = {"hmac_key":args.key, 
                "hmac_secret":args.secret}
    
    main = Main(user, credential)
    feedback = Feedback("Excellent!", 
                    UserLocalbitcoin.FEEDBACK_POSITIVE)
    
    main.set_feedback(feedback)
    main.greet_all_open_order()
    

    
    main.set_partners_ads(file_to_json(args.file))
    main.change_all_prices( Decimal(amount), ads, 
                            main.get_partners_ads(), False)


if __name__ == "__main__":
    exit(script_main())
