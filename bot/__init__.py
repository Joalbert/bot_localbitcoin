from decimal import Decimal
import random
from typing import List

from user import User
from models import ChatMessage, Ad, Chat, UserData, Feedback


class Bot:
    ''' Use User Interface to communicate with broker for
    reading messages, ads and write messages, feedbacks and update prices,
    do common task for ads such as filtering and removing'''
    ALREADY_GREET = -1
    GREET = 0
    FAIL_TO_GREET = 1

    def __init__(self, user: User, name: str):
        self.user = user
        self.username = name

    def read_own_ads(self) -> List[Ad]:
        self.ads = self.user.get_user_ads()
        return self.ads

    def welcome_message_chat(self, chat: Chat,
                             messages: List[ChatMessage],
                             greetings: List[ChatMessage]) -> int:
        who_i_am = self.user.get_username()
        for message in messages:
            if who_i_am == message.username:
                return self.ALREADY_GREET
        else:
            if(self.user.write_message_chat(
                    chat, random.choice(greetings))):
                return self.GREET
            return self.FAIL_TO_GREET

    def update_price_ads(self, *, own_ad: Ad, update_price: Decimal) -> bool:
        return self.user.write_price_ad(own_ad, update_price)

    def give_feedback(self, user_to_be_score: UserData,
                      feedback: Feedback) -> bool:
        return self.user.write_feedback_order(
            user_to_be_score, feedback)

    def filter_list_ads(self, minimun: Decimal, maximum: Decimal,
                        ads: List[Ad]) -> List[Ad]:
        valid_ads = []
        # breakpoint()
        for ad in ads:
            if (ad.minimum_value < maximum and ad.maximum_value > minimun):
                valid_ads.append(ad)
        return valid_ads

    def remove_own_ads(self, ads: List[Ad], own_ads: List[int]) -> List[Ad]:
        valid_ads = []
        for ad in ads:
            if not(ad.id in own_ads):
                valid_ads.append(ad)
        return valid_ads

    def get_bigger_price(self, ads: List[Ad]) -> Decimal:
        price = ads[0].price
        for ad in ads:
            if ad.price > price:
                price = ad.price
        return price

    def get_smaller_price(self, ads: List[Ad]) -> Decimal:
        price = ads[0].price
        for ad in ads:
            if ad.price < price:
                price = ad.price
        return price

    def read_opened_order(self):
        return self.user.read_opened_orders()

    def read_closed_order(self):
        return self.user.read_closed_order()

    def read_messages(self, chat: Chat):
        return self.user.read_messages_chat(chat)

    def read_my_ads(self):
        return self.user.get_user_ads()

    def read_buy_ads(self, **kwargs):
        return self.user.read_buy_ads(**kwargs)

    def read_sell_ads(self, **kwargs):
        return self.user.read_sell_ads(**kwargs)
