from typing import Dict, Any
from connection import Connection


class ConnectionLocalBitcoin(Connection):
    _base_url = "https://api.binance.com"

    def get_sell_ads(self, **kwargs) -> Any:
        """ Get sell ads availables for some country and
        a specific page of pagination"""
        pass

    def get_buy_ads(self, **kwargs) -> Any:
        """ Get buy ads availables for some country
        and a specific page of pagination"""
        pass

    def get_user_ads(self) -> Any:
        """Get user ads"""
        pass
    
    def create_user_ads(self, **kwargs) -> bool:
        """Create user ads"""
        pass
    
    def get_closed_order(self) -> Any:
        """ Get messages from closed orders"""
        pass
    def post_username_feedback(self, *, username: str,
                               message: Dict[str, str]) -> bool:
        """ Post feedback from specific username"""
        pass

    def get_contact_messages(self, contact_id: str) -> Any:
        """ Get contact messages from chat for specific contact id"""
        pass

    def get_opened_order(self) -> Any:
        """ Get our active ads"""
        pass

    def get_messages_active_order(self, contact_id: str) -> Any:
        """ Get messages from open orders"""
        pass

    def post_contact_messages(self, contact_id: str,
                              message: str) -> bool:
        """ Post a message for a chat"""
        pass

    def update_price_ad(self, ad_id: str, value: str) -> bool:
        pass
