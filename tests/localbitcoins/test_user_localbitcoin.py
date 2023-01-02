from unittest import TestCase

from models import ChatMessage, UserData, Chat, Feedback
from user.localbitcoin import UserLocalbitcoin
from adapters.localbitcoin import AdapterLocalbitcoin
from tests.mocks import (MockConnection, mock_list_ad,
                         mock_list_my_ads, mock_list_all, mock_list_all_order,
                         mock_list_all_chat_messages)
from tests import (SELL_JSON_LOC, BUY_JSON_LOC, CLOSED_ORDER_LOC,
                   OPENED_ORDER_LOC)

CREDENTIAL = {"hmac_key": "dummy", "hmac_secret": "dummy"}


class TestUser(TestCase):

    def setUp(self) -> None:
        adapter = AdapterLocalbitcoin()
        connection = MockConnection(CREDENTIAL)
        user = UserData("John Doe")
        partner = UserData("user")
        self.username = user
        self.user = UserLocalbitcoin(user, connection, adapter)
        self.partner = UserLocalbitcoin(partner, connection, adapter)
        return super().setUp()

    def test_get_user_ads(self):
        expected_value = mock_list_my_ads()
        ads = self.user.get_user_ads()
        self.assertEqual(ads, expected_value)

    def test_read_buy_ads(self):
        expected_value = mock_list_all(BUY_JSON_LOC)
        ads = self.user.read_buy_ads()
        self.assertEqual(ads, expected_value)

    def test_read_sell_ads(self):
        expected_value = mock_list_all(SELL_JSON_LOC)
        ads = self.user.read_sell_ads()
        self.assertEqual(ads, expected_value)

    def test_write_price_ad(self):
        self.assertTrue(self.user.write_price_ad(12, 100))

    def test_read_closed_order(self):
        expected_value = mock_list_all_order(CLOSED_ORDER_LOC)
        # breakpoint()
        data = self.user.read_closed_order()
        self.assertEqual(data, expected_value)

    def test_write_feedback_order(self):
        self.assertTrue(self.user.write_feedback_order(
            UserData("john"),
            Feedback("Hello World!",
                     UserLocalbitcoin.FEEDBACK_POSITIVE))
        )

    def test_read_opened_orders(self):
        expected_value = mock_list_all_order(OPENED_ORDER_LOC)
        data = self.user.read_opened_orders()
        self.assertEqual(data, expected_value)

    def test_read_messages_chat(self):
        expected_value = mock_list_all_chat_messages()
        data = self.user.read_messages_chat(Chat(1))
        self.assertEqual(data, expected_value)

    def test_write_message_chat(self):
        self.assertTrue(self.user.write_message_chat(Chat(1),
                                                     ChatMessage(
                                                                 1,
                                                                 self.username,
                                                                 "Hello World!"
                                                                 )
                                                     )
                        )

    def test_set_get_partner_ads(self):
        ads = mock_list_ad()
        ads_id = [ad.id for ad in ads]
        self.user.set_partner_ads("John", ads_id)
        self.assertEqual(self.user.get_partner_ads()["John"], ads_id)

    def test_remove_partner(self):
        ads = mock_list_ad()
        ads_id = [ad.id for ad in ads]
        self.user.set_partner_ads("John", ads_id)
        self.user.set_partner_ads("Gabriel", ads_id)
        self.user.remove_partner("John")
        self.assertNotIn("John", self.user.get_partner_ads().keys())
