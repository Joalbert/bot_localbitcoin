from unittest import TestCase, mock
from decimal import Decimal

from tests.mocks import (MockAdapter, MockConnection, MockUser,
        mock_list_ad, mock_list_chat_messages, mock_several_ads)
from models import (Chat, ChatMessage, UserData, Feedback, Order, Ad)
from bot import Bot

class TestUser(TestCase):
    
    def setUp(self) -> None:
        adapter = MockAdapter()
        connection = MockConnection({"mock": "mock"})
        self.user = MockUser(UserData("John Doe"),connection, adapter)
        self.bot = Bot(self.user, "bot")
        return super().setUp()

    def test_read_own_ads(self):
        expected_value = mock_list_ad()
        ads = self.bot.read_own_ads()
        self.assertEqual(expected_value, ads)

    def test_welcome_message_chat(self):
        greetings = [ChatMessage(1, 
                                self.user.user,
                                message = "Hello!"),
                    ChatMessage(1, 
                                self.user.user,
                                message = "Top of the morning to you!"),
                    ChatMessage(1, 
                                self.user.user,
                                message = "Good morning!"),]
        messages =mock_list_chat_messages() 
        
        self.assertEqual(Bot.GREET, 
            self.bot.welcome_message_chat(
                Chat(123),
                messages,
                greetings
            ))

        messages[0] = ChatMessage(1,self.user.user.username,"Hello")
        self.assertEqual(Bot.ALREADY_GREET, 
            self.bot.welcome_message_chat(
                Chat(123),
                messages,
                greetings
            ))
    
    def test_update_price_ads(self):
        self.assertTrue(self.bot.update_price_ads(
            own_ad=Ad(1, Decimal(1000),Decimal(50), Decimal(100),
            "Bank", "user_publisher"),
            update_price=Decimal(1200)
        ))

    def test_give_feedback(self):
        self.assertTrue(
            self.bot.give_feedback(UserData("jonhlennon", "John"),
            Feedback("Thanks! Excellent!", "Well"))
        )
    
    def test_remove_own_ads(self):
        ads = mock_list_ad()
        own = [ad.id for ad in ads]
        # Check that if ads availables are the one in list of own, retur
        self.assertEqual([], 
                self.bot.remove_own_ads(ads, own))

        own = [ad.id+5 for ad in ads]
        self.assertEqual(ads, 
                self.bot.remove_own_ads(ads, own))
    

    def test_filter_list_ads_only_filter(self):
        ad_list = mock_several_ads()
        # Range ad2 20_000 - 50_000
        expected_value = [ad_list[2]]
        
        self.assertEqual(expected_value, 
                self.bot.filter_list_ads(Decimal(15_000), Decimal(25_000),
                    ad_list))

        self.assertEqual(expected_value, 
                self.bot.filter_list_ads(Decimal(25_000),Decimal(55_000),
                    ad_list))
    
        self.assertEqual(expected_value, 
                self.bot.filter_list_ads(Decimal(25_000), Decimal(35_000),
                    ad_list))

        self.assertEqual(expected_value, 
                self.bot.filter_list_ads(Decimal(19_000), Decimal(60_000),
                    ad_list))

        self.assertNotEqual(expected_value, 
                self.bot.filter_list_ads(Decimal(55_000), Decimal(60_000),
                    ad_list))
            
        self.assertNotEqual(expected_value, 
                self.bot.filter_list_ads(Decimal(10_000), Decimal(15_000),
                    ad_list))

    def test_get_bigger_price(self):
        ads = mock_several_ads()
        MAXIMUM = 1
        self.assertEqual(ads[MAXIMUM].price, 
                self.bot.get_bigger_price(ads))

    
    def test_get_smaller_price(self):
        ads = mock_several_ads()
        MINIMUM = 2
        self.assertEqual(ads[MINIMUM].price, 
                self.bot.get_smaller_price(ads))
