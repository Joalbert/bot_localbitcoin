import unittest
from unittest.mock import patch

from connection.localbitcoin import ConnectionLocalBitcoin
from tests import (file_to_json, BUY_JSON_LOC, SELL_JSON_LOC, 
            MY_ADS_JSON_LOC, MESSAGES_LOC, OPENED_ORDER_LOC, 
            CLOSED_ORDER_LOC)
from tests.mocks import MockResponse
from models import UserData

DUMMY_TOKEN = {"hmac_key": "1234", "hmac_secret": "1234"}


class Test(unittest.TestCase):

    def setUp(self) -> None:
        self.connection = ConnectionLocalBitcoin(DUMMY_TOKEN)
        
        return super().setUp()
    
    def check_get(self, expected_value, function_to_check, **kwargs):
    
        with patch('connection.localbitcoin.hmac') as response:
            response.return_value = MockResponse(DUMMY_TOKEN)         
            result = function_to_check(**kwargs)  
            self.assertEqual(result, expected_value)

    def check_get_no_argument(self, expected_value, function_to_check):
    
        with patch('connection.localbitcoin.hmac') as response:
            response.return_value = MockResponse(DUMMY_TOKEN)         
            result = function_to_check()  
            self.assertEqual(result, expected_value)

    def test_get_sell_ads(self):
        kwargs ={"country_identifier":"ved","page":1} 
        expected_value = file_to_json(SELL_JSON_LOC)

        self.check_get(expected_value,
                self.connection.get_sell_ads,
                **kwargs)
        
    def test_get_buy_ads(self):
        kwargs ={"country_identifier":"ved","page":1} 
        expected_value = file_to_json(BUY_JSON_LOC)

        self.check_get(expected_value,
                    self.connection.get_buy_ads,
                **kwargs)


    def test_get_user_ads(self):
        expected_value = file_to_json(MY_ADS_JSON_LOC)

        self.check_get_no_argument(expected_value,
                    self.connection.get_user_ads)

    
    def test_get_closed_order(self):
        expected_value = file_to_json(CLOSED_ORDER_LOC)
        self.check_get_no_argument(expected_value,
                self.connection.get_closed_order)


    def test_get_opened_order(self):
        expected_value = file_to_json(OPENED_ORDER_LOC)
        self.check_get_no_argument(expected_value,
                    self.connection.get_opened_order)
    
    
    def test_get_messages_active_order(self):
        expected_value = file_to_json(MESSAGES_LOC)
        chat_id = str(76511874)
        with patch('connection.localbitcoin.hmac') as response:
            response.return_value = MockResponse(DUMMY_TOKEN)         
            result = self.connection.get_messages_active_order(chat_id) 
            self.assertEqual(result, expected_value)
   

    def test_post_username_feedback(self):
        message={"msg": "Excellent", 
                "feedback":"positive"}
        with patch('connection.localbitcoin.hmac') as response:
            response.return_value = MockResponse(DUMMY_TOKEN)         
            self.assertTrue(
                self.connection.post_username_feedback(
                    username="user",message=message)
                    )
        
    
    def test_post_contact_messages(self):
        message="Hello", 
                
        with patch('connection.localbitcoin.hmac') as response:
            response.return_value = MockResponse(DUMMY_TOKEN)         
            self.assertTrue(
                self.connection.post_contact_messages(
                    contact_id="1234",message=message)
                    )
        
    def test_update_price_ad(self):
        with patch('connection.localbitcoin.hmac') as response:
            response.return_value = MockResponse(DUMMY_TOKEN)         
            self.assertTrue(
                self.connection.update_price_ad(123, 1000))
        
            