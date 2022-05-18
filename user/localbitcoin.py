from bdb import Breakpoint
from typing import Dict, List

from connection.localbitcoin import ConnectionLocalBitcoin
from adapters.localbitcoin import AdapterLocalbitcoin
from user import User 
from models import Ad, Order, ChatMessage, UserData, Chat, Feedback

class UserLocalbitcoin(User):
    """"User Actions in platform"""

    FEEDBACK_TRUST = "trust"
    FEEDBACK_POSITIVE = "positive"
    FEEDBACK_NEUTRAL = "neutral"
    FEEDBACK_BLOCK = "block"
    FEEDBACK_BLOCK_WO_FEEDBACK = "block_without_feedback"

    def __init__(self, user:UserData, 
                connection:ConnectionLocalBitcoin, 
                adapter: AdapterLocalbitcoin):
        self.connection = connection
        self.adapter = adapter
        self.user = user
        self.partner_ads:Dict[str,List[Ad]] = dict()

    def get_user_ads(self)->List[Ad]:
        """User's ads"""
        try:
            return self.adapter.to_list_ad(
                self.connection.get_user_ads()["data"]["ad_list"])
        except ConnectionError:
            raise
    
    def read_buy_ads(self, **kwargs)->List[Ad]:
        """Read all buy ads in the webpage"""
        try:
            return self.adapter.to_list_ad(
                self.connection.get_buy_ads(**kwargs)["data"]["ad_list"]
                )
        except ConnectionError:
            raise
    

    def read_sell_ads(self, **kwargs)->List[Ad]:
        """Read all sell ads in the webpage"""
        try:
            return self.adapter.to_list_ad(
                self.connection.get_sell_ads(**kwargs)["data"]["ad_list"])
        except ConnectionError:
            raise
    
    
    def write_price_ad(self, ad_id, price)->bool:
        """Update price for an advertisement for user"""
        return self.connection.update_price_ad(ad_id, price)


    def read_closed_order(self)->List[Order]:
        """ Read feedback for a transaction """
        return self.adapter.to_list_order(
            self.connection.get_closed_order()["data"]["contact_list"])
    

    def write_feedback_order(self, user_to_be_score:UserData, 
            feedback:Feedback)->bool:
        """Write feedback for a transaction """
        return self.connection.post_username_feedback(
            username=user_to_be_score.username, 
            message={
                "msg": feedback.message, 
                "feedback":feedback.feedback}
                )


    def read_opened_orders(self)->List[Order]:
        """ Write a message for a chat """
        return self.adapter.to_list_order(
            self.connection.get_opened_order()["data"]["contact_list"])


    def read_messages_chat(self, chat:Chat)->List[ChatMessage]:
        """ Write a message for a chat """
        return self.adapter.to_list_messages(
            self.connection.get_contact_messages(
                contact_id=str(chat.id))["data"]["message_list"])


    def write_message_chat(self, chat:Chat, message:ChatMessage)->bool:
        """ Write a message for a chat """
        return self.connection.post_contact_messages(
            str(chat.id), message.message)


    def set_partner_ads(self, key, partner_ads)->None:
        self.partner_ads[key] = partner_ads

    
    def get_partner_ads(self)->Dict[str,List[Ad]]:
        return self.partner_ads


    def remove_partner(self, key)->bool:
        return True if self.partner_ads.pop(key) else False

    def get_username(self):
        return self.user.username