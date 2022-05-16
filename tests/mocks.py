from typing import List, Dict, Any
from decimal import Decimal
from datetime import datetime
from unittest import result

from adapters.localbitcoin import AdapterLocalbitcoin
from adapters import Adapter
from connection.localbitcoin import ConnectionLocalBitcoin
from connection import Connection
from user import User
from models import Ad, Order, ChatMessage, Feedback, UserData, Chat
from tests import (file_to_json, MESSAGES_LOC, CLOSED_ORDER_LOC, MY_ADS_JSON_LOC, 
            SELL_JSON_LOC, BUY_JSON_LOC, OPENED_ORDER_LOC)


class MockConnection(ConnectionLocalBitcoin):
     
    def __init__(self, credentials:Dict[str, str])->None:
        return 
     
    def get_sell_ads(self, **kwargs)->List[Dict[str, str]]:
        return file_to_json(SELL_JSON_LOC)
  
    def get_buy_ads(self, **kwargs)->List[Dict[str, str]]:
        """ Get buy ads availables for some country and a specific page of pagination"""
        return file_to_json(BUY_JSON_LOC)
 
    def get_user_ads(self)->List[Dict[str, str]]:
        """Get user ads"""
        return file_to_json("tests/json/localbitcoin/ads-reduce.json")
         
    def post_username_feedback(self, *, 
            username:str, message:Dict[str, str])-> bool:
        """ Post feedback from specific username"""
        return True
     
    def get_contact_messages(self, 
            contact_id:str)->List[Dict[str, str]]:
        """ Get contact messages from chat for specific contact id"""
        return file_to_json(MESSAGES_LOC)
     
    def post_contact_messages(self, 
                            contact_id:str, 
                            message:str)->bool:
        """ Post a message for a chat"""
        return True    
     
    def get_opened_order(self)->List[Dict[str, str]]:
        """ Get our active ads"""
        return file_to_json(OPENED_ORDER_LOC)
     
    def get_closed_order(self)->List[Dict[str, str]]:
        """ Get messages from closed orders"""
        # breakpoint()
        return file_to_json(CLOSED_ORDER_LOC)
     
    def get_messages_active_order(self, 
            contact_id:str)->List[Dict[str, str]]:
        """ Get messages from open orders"""
        return file_to_json(MESSAGES_LOC)
     
    def update_price_ad(self,ad_id, value)->bool:
        return True
    
    def create_user_ads(self, **kwargs)->bool:
        """Create user ads"""
        return True

class MockAdapter(AdapterLocalbitcoin):
    """Mock adapter"""
    def to_list_ad(self, data: List[Dict[str, Any]]) -> List[Ad]:
        return mock_list_ad()

    def to_list_order(self, data: List[Dict[str, Any]]) -> List[Order]:
        return mock_list_order()
    
    def to_list_messages(self, data: List[Dict[str, Any]]) -> List[ChatMessage]:
        return mock_list_chat_messages()


class MockResponse:
    
    SELL_ADS ="https://localbitcoins.com/sell-bitcoins-online/ved/.json?page=1"
    BUY_ADS ="https://localbitcoins.com/buy-bitcoins-online/ved/.json?page=1"
    MY_ADS = "https://localbitcoins.com/api/ads/"
    OPENED_ORDER = "https://localbitcoins.com/api/dashboard/"
    CLOSED_ORDER = "https://localbitcoins.com/api/dashboard/closed/"
    MESSAGES = "https://localbitcoins.com/api/contact_messages/76511874/"



    def __init__(self, token) -> None:
        pass

            
    def _url_value(self, url):
        if(url==self.SELL_ADS):
            return file_to_json(SELL_JSON_LOC)
        if (url==self.BUY_ADS):
            return file_to_json(BUY_JSON_LOC)
        if (url == self.MY_ADS):
            return file_to_json(MY_ADS_JSON_LOC)
        if (url == self.OPENED_ORDER):
            return file_to_json(OPENED_ORDER_LOC)
        if (url == self.CLOSED_ORDER):
            return file_to_json(CLOSED_ORDER_LOC)
        if (url == self.MESSAGES):
            return file_to_json(MESSAGES_LOC)
                        
    
    def call(self, method_http, url):
        if method_http == "GET":
            self.response = self._url_value(url)
            return self

    def json(self):
        return self.response  

class MockUser(User):
    """"User Actions in platform"""

    def __init__(self, user:UserData, connection:Connection, adapter: Adapter):
        self.connection = connection
        self.adapter = adapter
        self.user = user
        self.partner_ads:Dict[str,List[Ad]] = dict()

    def get_username(self):
        return self.user.username

    def get_user_ads(self)->List[Ad]:
        """User's ads"""
        return mock_list_ad()
    
    def read_buy_ads(self, **kwargs)->List[Ad]:
        """Read all buy ads in the webpage"""
        return mock_list_ad()


    def read_sell_ads(self, **kwargs)->List[Ad]:
        """Read all sell ads in the webpage"""
        return mock_list_ad()

    
    def write_price_ad(self, ad:Ad, price:Decimal)->bool:
        """Update price for an advertisement for user"""
        return True

    def read_closed_order(self)->List[Order]:
        """ Read feedback for a transaction """
        return mock_list_order()

    def write_feedback_order(self, user_to_be_score:UserData, 
            feedback:Feedback)->bool:
        """Write feedback for a transaction """
        return True

    def read_opened_orders(self)->List[Order]:
        """ Write a message for a chat """
        return mock_list_order()

    def read_messages_chat(self, chat:Chat)->List[ChatMessage]:
        """ Write a message for a chat """
        return mock_list_chat_messages()

    def write_message_chat(self, chat:Chat, message:ChatMessage)->bool:
        """ Write a message for a chat """
        return True

    def set_partner_ads(self, user:UserData, partner_ads:List[Ad])->None:
        return 

    
    def get_partner_ads(self)->Dict[str,List[Ad]]:
        return {"user":mock_list_ad()}


    def remove_partner(self, key)->bool:
        return True


def mock_list_ad():
    ads_json = file_to_json(MY_ADS_JSON_LOC)
    return [Ad(
            int(ads_json["data"]["ad_list"][0]["data"]["ad_id"]),
            Decimal(ads_json["data"]["ad_list"][0]["data"]["temp_price"]),
            Decimal(ads_json["data"]["ad_list"][0]["data"]["min_amount_available"]),
            Decimal(ads_json["data"]["ad_list"][0]["data"]["max_amount_available"]),
            ads_json["data"]["ad_list"][0]["data"]["bank_name"],
            ads_json["data"]["ad_list"][0]["data"]["profile"]["username"],
            ads_json["data"]["ad_list"][0]["data"]["visible"]
            )]

def mock_list_all(location):
    ads_json = file_to_json(location)
    result = []
    for item in ads_json["data"]["ad_list"]:
        result.append(Ad(
            int(item["data"]["ad_id"]),
            Decimal(item["data"]["temp_price"]),
            Decimal(item["data"]["min_amount_available"]),
            Decimal(item["data"]["max_amount_available"]),
            item["data"]["bank_name"],
            item["data"]["profile"]["username"],
            item["data"]["visible"]
            ))
    return result

def mock_list_my_ads():
    ads_json = file_to_json("tests/json/localbitcoin/ads-reduce.json")
    return [Ad(
            int(ads_json["data"]["ad_list"][0]["data"]["ad_id"]),
            Decimal(ads_json["data"]["ad_list"][0]["data"]["temp_price"]),
            Decimal(ads_json["data"]["ad_list"][0]["data"]["min_amount_available"]),
            Decimal(ads_json["data"]["ad_list"][0]["data"]["max_amount_available"]),
            ads_json["data"]["ad_list"][0]["data"]["bank_name"],
            ads_json["data"]["ad_list"][0]["data"]["profile"]["username"],
            ads_json["data"]["ad_list"][0]["data"]["visible"]
            )]


def mock_list_order():
    ads_json = file_to_json(CLOSED_ORDER_LOC)
    return [Order(
            int(
                datetime.fromisoformat(
                ads_json["data"]["contact_list"][0]["data"]["created_at"]).timestamp()
                ),
            ads_json["data"]["contact_list"][0]["data"]["seller"]["username"],
            ads_json["data"]["contact_list"][0]["data"]["buyer"]["username"],
            "",
            "",
            ads_json["data"]["contact_list"][0]["data"]["contact_id"],
            False
            )]

def mock_list_all_order(location):
    # breakpoint()
    ads_json = file_to_json(location)
    result = []
    for item in ads_json["data"]["contact_list"]:
        result.append(
            Order(
                    int(datetime.fromisoformat(item["data"]["created_at"]).timestamp()),
                    item["data"]["seller"]["username"],
                    item["data"]["buyer"]["username"],
                    "",
                    "",
                    int(item["data"]["contact_id"]),
                    not (item["data"]["closed_at"] is None or item["data"]["closed_at"]=="")
                )
        ) 
    return result


def mock_list_chat_messages():
    ads_json = file_to_json(MESSAGES_LOC)
    return [ChatMessage(
            int(
                datetime.fromisoformat(
                ads_json["data"]["message_list"][0]["created_at"]).timestamp()
                ),
            ads_json["data"]["message_list"][0]["sender"]["username"],
            ads_json["data"]["message_list"][0]["msg"],
            )]

def mock_list_all_chat_messages():
    ads_json = file_to_json(MESSAGES_LOC)
    result = []
    for item in ads_json["data"]["message_list"]:
        result.append(ChatMessage(
            int(
                datetime.fromisoformat(
                item["created_at"]).timestamp()
                ),
            item["sender"]["username"],
            item["msg"],
            ))
    return result


def mock_several_ads():
    ads_json = file_to_json(MY_ADS_JSON_LOC)
    return [Ad(
            int(ads_json["data"]["ad_list"][0]["data"]["ad_id"]),
            Decimal(1_000),
            Decimal(1_000),
            Decimal(12_000),
            ads_json["data"]["ad_list"][0]["data"]["bank_name"],
            ads_json["data"]["ad_list"][0]["data"]["profile"]["username"],
            ads_json["data"]["ad_list"][0]["data"]["visible"]
            ),
            Ad(
            int(ads_json["data"]["ad_list"][1]["data"]["ad_id"]),
            Decimal(1_200),
            Decimal(2_000),
            Decimal(15_000),
            ads_json["data"]["ad_list"][1]["data"]["bank_name"],
            ads_json["data"]["ad_list"][1]["data"]["profile"]["username"],
            ads_json["data"]["ad_list"][1]["data"]["visible"]
            ),
            Ad(
            int(ads_json["data"]["ad_list"][2]["data"]["ad_id"]),
            Decimal(800),
            Decimal(20_000),
            Decimal(50_000),
            ads_json["data"]["ad_list"][2]["data"]["bank_name"],
            ads_json["data"]["ad_list"][2]["data"]["profile"]["username"],
            ads_json["data"]["ad_list"][2]["data"]["visible"]
            ),
            Ad(
            int(ads_json["data"]["ad_list"][3]["data"]["ad_id"]),
            Decimal(900),
            Decimal(70_000),
            Decimal(100_000),
            ads_json["data"]["ad_list"][3]["data"]["bank_name"],
            ads_json["data"]["ad_list"][3]["data"]["profile"]["username"],
            ads_json["data"]["ad_list"][3]["data"]["visible"]
            )]