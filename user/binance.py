from typing import Dict, List

from connection.localbitcoin import ConnectionLocalBitcoin
from adapters.localbitcoin import AdapterLocalbitcoin
from user import User
from models import Ad, Order, ChatMessage, UserData, Chat, Feedback


class BinanceUser(User):
    """"User Actions in platform"""

    def get_user_ads(self) -> List[Ad]:
        """User's ads"""
        pass

    def read_buy_ads(self, **kwargs) -> List[Ad]:
        """Read all buy ads in the webpage"""
        pass

    def read_sell_ads(self, **kwargs) -> List[Ad]:
        """Read all sell ads in the webpage"""
        pass

    def write_price_ad(self, ad_id, price) -> bool:
        """Update price for an advertisement for user"""
        pass

    def read_closed_order(self) -> List[Order]:
        """ Read feedback for a transaction """
        pass

    def write_feedback_order(self, user_to_be_score: UserData,
                             feedback: Feedback) -> bool:
        """Write feedback for a transaction """
        pass

    def read_opened_orders(self) -> List[Order]:
        """ Write a message for a chat """
        pass

    def read_messages_chat(self, chat: Chat) -> List[ChatMessage]:
        """ Write a message for a chat """
        pass

    def write_message_chat(self, chat: Chat, message: ChatMessage) -> bool:
        """ Write a message for a chat """
        pass

    def set_partner_ads(self, key, partner_ads) -> None:
        pass 

    def get_partner_ads(self) -> Dict[str, List[Ad]]:
        pass

    def remove_partner(self, key) -> bool:
        pass

    def get_username(self):
        pass
