from typing import Dict, List
from decimal import Decimal
import abc

from models import Ad, Feedback, Order, ChatMessage, UserData, Chat


class User(abc.ABC):
    """"User Actions in platform"""

    @abc.abstractmethod
    def get_user_ads(self) -> List[Ad]:
        """User's ads"""
        pass

    @abc.abstractmethod
    def read_buy_ads(self, **kwargs) -> List[Ad]:
        """Read all buy ads in the webpage"""
        pass

    @abc.abstractmethod
    def read_sell_ads(self, **kwargs) -> List[Ad]:
        """Read all sell ads in the webpage"""
        pass

    @abc.abstractmethod
    def write_price_ad(self, ad: Ad, price: Decimal) -> bool:
        """Update price for an advertisement for user"""
        pass

    @abc.abstractmethod
    def read_closed_order(self) -> List[Order]:
        """ Read feedback for a transaction """
        pass

    @abc.abstractmethod
    def write_feedback_order(self, user_to_be_score: UserData,
                             feedback: Feedback) -> bool:
        """Write feedback for a transaction """
        pass

    @abc.abstractmethod
    def read_opened_orders(self) -> List[Order]:
        """ Write a message for a chat """
        pass

    @abc.abstractmethod
    def read_messages_chat(self, chat: Chat) -> List[ChatMessage]:
        """ Write a message for a chat """
        pass

    @abc.abstractmethod
    def write_message_chat(self, chat: Chat, message: ChatMessage) -> bool:
        """ Write a message for a chat """
        pass

    @abc.abstractmethod
    def set_partner_ads(self, user: UserData, partner_ads: List[Ad]) -> None:
        pass

    @abc.abstractmethod
    def get_partner_ads(self) -> Dict[str, List[Ad]]:
        pass

    @abc.abstractmethod
    def remove_partner(self, key) -> bool:
        pass

    @abc.abstractmethod
    def get_username(self):
        pass
