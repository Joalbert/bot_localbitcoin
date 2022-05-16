from unittest import TestCase
from decimal import Decimal
from datetime import datetime

from tests import (file_to_json, MY_ADS_JSON_LOC, 
            MESSAGES_LOC, OPENED_ORDER_LOC)

from models import Ad, Order, ChatMessage 
from adapters.localbitcoin import AdapterLocalbitcoin 

class TestAdapter(TestCase):
    
    def test_to_list_ad(self):
        ads_json = file_to_json(MY_ADS_JSON_LOC)
        expected_value = [Ad(
            int(ads_json["data"]["ad_list"][0]["data"]["ad_id"]),
            Decimal(ads_json["data"]["ad_list"][0]["data"]["temp_price"]),
            Decimal(ads_json["data"]["ad_list"][0]["data"]["min_amount_available"]),
            Decimal(ads_json["data"]["ad_list"][0]["data"]["max_amount_available"]),
            ads_json["data"]["ad_list"][0]["data"]["bank_name"],
            ads_json["data"]["ad_list"][0]["data"]["profile"]["username"],
            ads_json["data"]["ad_list"][0]["data"]["visible"]
            )]

        adapter = AdapterLocalbitcoin()
        
        self.assertEqual(adapter.to_list_ad(
            [ads_json["data"]["ad_list"][0]]),expected_value )

    def test_to_list_order(self):
        ads_json = file_to_json(OPENED_ORDER_LOC)
        expected_value = [Order(
            int(
                datetime.fromisoformat(
                ads_json["data"]["contact_list"][0]["data"]["created_at"])\
                    .timestamp()
                ),
            ads_json["data"]["contact_list"][0]["data"]["seller"]["username"],
            ads_json["data"]["contact_list"][0]["data"]["buyer"]["username"],
            "",
            "",
            ads_json["data"]["contact_list"][0]["data"]["contact_id"],
            False
            )]

        adapter = AdapterLocalbitcoin()
        
        self.assertEqual(adapter.to_list_order(
            [ads_json["data"]["contact_list"][0]]),expected_value )


    def test_to_list_message(self):
        ads_json = file_to_json(MESSAGES_LOC)
        expected_value = [ChatMessage(
            int(
                datetime.fromisoformat(
                ads_json["data"]["message_list"][0]["created_at"])\
                    .timestamp()
                ),
            ads_json["data"]["message_list"][0]["sender"]["username"],
            ads_json["data"]["message_list"][0]["msg"],
            )]

        adapter = AdapterLocalbitcoin()
        
        self.assertEqual(adapter.to_list_messages(
            [ads_json["data"]["message_list"][0]]),expected_value )
