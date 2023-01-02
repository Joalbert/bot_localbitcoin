from unittest import TestCase
from unittest.mock import patch
from decimal import Decimal

from examples.script_update_price import (Main,
                                          get_ads_from_file, script_main,
                                          get_banks_from_file,
                                          filter_banks)
from models import Ad, UserData
from tests.mocks import MockConnection

CREDENTIALS = {
    "hmac_key": "Connection should be mocked in each method",
    "hmac_secret": "Connection should be mocked in each method"
}
ADS = [Ad(int("1442920"), Decimal("142613.52"), Decimal("14.27"),
          Decimal("31.39"),
          "PAG MOVIL✅CARIBE✅MERCANTIL✅PROVINCIA En línea ✅✅✅✅",
          "thd68"),
       Ad(int("1410674"), Decimal("155043.14"), Decimal("150.00"),
          Decimal("1814.56"),
           "BDVENEZUELA✅MERCANTIL☑️BNC✅BANESCO⏩PAGO MÓVIL",
           "AbrahamP1")]

BANKS = ["mercantil", "merc", "m e r c a n t i l"]

DUMMY_ADS = [Ad(int("1442920"), Decimal("142613.52"), Decimal("14.27"),
                Decimal("31.39"),
                "PAG MOVIL✅CARIBE✅MERCANTIL✅PROVINCIA En línea ✅✅✅✅",
                "thd68"),
             Ad(int("1410674"), Decimal("155043.14"), Decimal("150.00"),
                Decimal("1814.56"),
                "BDVENEZUELA✅MERCANTIL☑️BNC✅BANESCO⏩PAGO MÓVIL",
                "AbrahamP1"),
             Ad(int("1442921"), Decimal("142613.52"), Decimal("14.27"),
                Decimal("31.39"),
                "SANTANDER",
                "rivaliño"),
             Ad(int("1410672"), Decimal("155043.14"), Decimal("150.00"),
                Decimal("1814.56"),
                "S A N T A N D E R",
                "rivaliño"),
             Ad(int("1442922"), Decimal("142613.52"), Decimal("14.27"),
                Decimal("31.39"),
                "CARIBE",
                "rivaliño"),
             Ad(int("1410676"), Decimal("155043.14"), Decimal("150.00"),
                Decimal("1814.56"),
                "CARIBE",
                "rivaliño")]


class TestUpdatePrice(TestCase):

    def setUp(self) -> None:
        self.user = UserData("john", "John Doe")
        with patch(("examples.script_local_feedback."
                    "ConnectionLocalBitcoin")) as connection:
            connection.return_value = MockConnection(CREDENTIALS)
            self.main = Main(self.user, CREDENTIALS)
        return super().setUp()

    def test_get_ads_from_file(self):
        self.assertEqual(get_ads_from_file(
            "tests/examples/json/update-price/partner_ads.json"),
            ADS)

    def test_get_banks_from_file(self):
        self.assertEqual(get_banks_from_file(
            "tests/examples/json/update-price/bank_list.json"),
            BANKS)

    def test_filter_banks(self):
        BANKS_ALLOWED = ["santander", "s a n t a n d e r"]
        expected_value = [
            Ad(int("1442921"), Decimal("142613.52"), Decimal("14.27"),
               Decimal("31.39"), "SANTANDER", "rivaliño"),
            Ad(int("1410672"), Decimal("155043.14"), Decimal("150.00"),
               Decimal("1814.56"),
               "S A N T A N D E R", "rivaliño")]

        self.assertEqual(filter_banks(DUMMY_ADS, BANKS_ALLOWED),
                         expected_value)

    def test_cli_update(self):
        args = [
            "-k 1234",
            "-s 1234",
            "-n John Doe",
            "-u xyz2000",
            "-p tests/examples/json/update-price/partner_ads.json",
            "-o tests/examples/json/update-price/own_ads.json",
            "-b",
            "-l tests/examples/json/update-price/bank_list.json",
        ]

        with patch(("examples.script_update_price."
                    "ConnectionLocalBitcoin")) as connection:
            connection.return_value = MockConnection(CREDENTIALS)
            with patch("examples.script_update_price.input") as input:
                input.return_value = "-10"
                self.assertEqual(script_main(args), 0)

        args = [
            "-k 1234",
            "-s 1234",
            "-n John Doe",
            "-u xyz2000",
            "-p tests/examples/json/update-price/partner_ads.json",
            "-o tests/examples/json/update-price/own_ads.json",
            "-l tests/examples/json/update-price/bank_list.json",
        ]

        with patch(("examples.script_update_price."
                    "ConnectionLocalBitcoin")) as connection:
            connection.return_value = MockConnection(CREDENTIALS)
            with patch("examples.script_update_price.input") as input:
                input.return_value = "10"
                self.assertEqual(script_main(args), 0)

    def test_bad_cli_update(self):
        args = [
            "-s 1234",
            "-n John Doe",
            "-u xyz2000",
            "-p tests/examples/json/update-price/partner_ads.json",
            "-o tests/examples/json/update-price/own_ads.json",
            "-b",
            "-l tests/examples/json/update-price/bank_list.json",
        ]

        with patch(("examples.script_update_price."
                    "ConnectionLocalBitcoin")) as connection:
            connection.return_value = MockConnection(CREDENTIALS)
            with patch("examples.script_update_price.input") as input:
                input.return_value = "-10"
                with self.assertRaises(SystemExit):
                    script_main(args)

        args = [
            "-k 1234",
            "-n John Doe",
            "-u xyz2000",
            "-p tests/examples/json/update-price/partner_ads.json",
            "-o tests/examples/json/update-price/own_ads.json",
            "-b",
            "-l tests/examples/json/update-price/bank_list.json",
        ]

        with patch(("examples.script_update_price."
                    "ConnectionLocalBitcoin")) as connection:
            connection.return_value = MockConnection(CREDENTIALS)
            with patch("examples.script_update_price.input") as input:
                input.return_value = "-10"
                with self.assertRaises(SystemExit):
                    script_main(args)

        args = [
            "-k 1234",
            "-s 1234",
            "-n John Doe",
            "-p tests/examples/json/update-price/partner_ads.json",
            "-o tests/examples/json/update-price/own_ads.json",
            "-b",
            "-l tests/examples/json/update-price/bank_list.json",
        ]

        with patch(("examples.script_update_price."
                    "ConnectionLocalBitcoin")) as connection:
            connection.return_value = MockConnection(CREDENTIALS)
            with patch("examples.script_update_price.input") as input:
                input.return_value = "-10"
                with self.assertRaises(SystemExit):
                    script_main(args)

        args = [
            "-k 1234",
            "-s 1234",
            "-n John Doe",
            "-u xyz2000",
            "-o tests/examples/json/update-price/own_ads.json",
            "-b",
            "-l tests/examples/json/update-price/bank_list.json",
        ]

        with patch(("examples.script_update_price."
                    "ConnectionLocalBitcoin")) as connection:
            connection.return_value = MockConnection(CREDENTIALS)
            with patch("examples.script_update_price.input") as input:
                input.return_value = "-10"
                with self.assertRaises(SystemExit):
                    script_main(args)

        args = [
            "-k 1234",
            "-s 1234",
            "-n John Doe",
            "-u xyz2000",
            "-p tests/examples/json/update-price/partner_ads.json",
            "-b",
            "-l tests/examples/json/update-price/bank_list.json",
        ]

        with patch(("examples.script_update_price."
                    "ConnectionLocalBitcoin")) as connection:
            connection.return_value = MockConnection(CREDENTIALS)
            with patch("examples.script_update_price.input") as input:
                input.return_value = "-10"
                with self.assertRaises(SystemExit):
                    script_main(args)

        args = [
            "-k 1234",
            "-s 1234",
            "-n John Doe",
            "-u xyz2000",
            "-p tests/examples/json/update-price/partner_ads.json",
            "-o tests/examples/json/update-price/own_ads.json",
            "-b",
        ]

        with patch(("examples.script_update_price."
                    "ConnectionLocalBitcoin")) as connection:
            connection.return_value = MockConnection(CREDENTIALS)
            with patch("examples.script_update_price.input") as input:
                input.return_value = "-10"
                with self.assertRaises(SystemExit):
                    script_main(args)

    def test_bad_file_update(self):
        args = [
            "-k 1234",
            "-s 1234",
            "-n John Doe",
            "-u xyz2000",
            "-p tests/examples/json/update-price/no_exist.json",
            "-o tests/examples/json/update-price/own_ads.json",
            "-l tests/examples/json/update-price/bank_list.json",
        ]

        with patch(("examples.script_update_price."
                    "ConnectionLocalBitcoin")) as connection:
            connection.return_value = MockConnection(CREDENTIALS)
            with patch("examples.script_update_price.input") as input:
                input.return_value = "-10"
                self.assertEqual(script_main(args), 1)

        args = [
            "-k 1234",
            "-s 1234",
            "-n John Doe",
            "-u xyz2000",
            "-p tests/examples/json/update-price/partner_ads.json",
            "-o tests/examples/json/update-price/no_exist.json",
            "-l tests/examples/json/update-price/bank_list.json",
        ]

        with patch(("examples.script_update_price."
                    "ConnectionLocalBitcoin")) as connection:
            connection.return_value = MockConnection(CREDENTIALS)
            with patch("examples.script_update_price.input") as input:
                input.return_value = "-10"
                self.assertEqual(script_main(args), 1)

        args = [
            "-k 1234",
            "-s 1234",
            "-n John Doe",
            "-u xyz2000",
            "-p tests/examples/json/update-price/partner_ads.json",
            "-o tests/examples/json/update-price/own_ads.json",
            "-l tests/examples/json/update-price/no_exist.json",
        ]

        with patch(("examples.script_update_price."
                    "ConnectionLocalBitcoin")) as connection:
            connection.return_value = MockConnection(CREDENTIALS)
            with patch("examples.script_update_price.input") as input:
                input.return_value = "-10"
                self.assertEqual(script_main(args), 1)

    def test_bad_data_file_update(self):
        args = [
            "-k 1234",
            "-s 1234",
            "-n John Doe",
            "-u xyz2000",
            "-p tests/examples/json/update-price/bad_partner_ads.json",
            "-o tests/examples/json/update-price/own_ads.json",
            "-l tests/examples/json/update-price/bank_list.json",
        ]

        with patch(("examples.script_update_price."
                    "ConnectionLocalBitcoin")) as connection:
            connection.return_value = MockConnection(CREDENTIALS)
            with patch("examples.script_update_price.input") as input:
                input.return_value = "-10"
                self.assertEqual(script_main(args), 1)

        args = [
            "-k 1234",
            "-s 1234",
            "-n John Doe",
            "-u xyz2000",
            "-p tests/examples/json/update-price/partner_ads.json",
            "-o tests/examples/json/update-price/bad_own_ads.json",
            "-l tests/examples/json/update-price/bank_list.json",
        ]

        with patch(("examples.script_update_price."
                    "ConnectionLocalBitcoin")) as connection:
            connection.return_value = MockConnection(CREDENTIALS)
            with patch("examples.script_update_price.input") as input:
                input.return_value = "-10"
                self.assertEqual(script_main(args), 1)

        args = [
            "-k 1234",
            "-s 1234",
            "-n John Doe",
            "-u xyz2000",
            "-p tests/examples/json/update-price/partner_ads.json",
            "-o tests/examples/json/update-price/own_ads.json",
            "-l tests/examples/json/update-price/bad_bank_list.json",
        ]

        with patch(("examples.script_update_price."
                    "ConnectionLocalBitcoin")) as connection:
            connection.return_value = MockConnection(CREDENTIALS)
            with patch("examples.script_update_price.input") as input:
                input.return_value = "-10"
                self.assertEqual(script_main(args), 1)
