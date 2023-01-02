from typing import Dict, List
from decimal import Decimal
import argparse

from bot import Bot
from user.localbitcoin import UserLocalbitcoin
from adapters.localbitcoin import AdapterLocalbitcoin
from connection.localbitcoin import ConnectionLocalBitcoin
from models import UserData, Ad
from helpers import file_to_json


def parse_arguments(args):
    parser = argparse.ArgumentParser(
        prog="Update prices in Localbitcoin.")
    parser.add_argument("-k", "--key",
                        help="Key provided by Localbitcoin", required=True)
    parser.add_argument("-s", "--secret",
                        help="Secret provided by Localbitcoin", required=True)
    parser.add_argument("-n", "--name",
                        help="Name in localbitcoin")
    parser.add_argument("-u", "--username",
                        help="username in Localbitcoin", required=True)
    parser.add_argument("-p", "--partner",
                        help="File json with Ads info for partners",
                        required=True)
    parser.add_argument("-o", "--own",
                        help="File json with our own Ads",
                        required=True)
    parser.add_argument("-b", "--buy",
                        help="Feed buy ads",
                        action="store_true")
    parser.add_argument("-l", "--list",
                        help="List of synonyms for banks",
                        required=True)
    return parser.parse_args(args)


def get_ads_from_file(file_path):
    data_json = file_to_json(file_path)
    adapter = AdapterLocalbitcoin()
    return adapter.to_list_ad(data_json["data"]["ad_list"])


def get_banks_from_file(file_path):
    data_json = file_to_json(file_path)
    data = []
    for datum in data_json["banks"]:
        data.append(datum)
    return data


def filter_banks(ads: List[Ad], white_list: List[str]):
    """ filter banks from a bigger list ads and kept the one
        which name contains any of the list name given in white
        list"""
    valid_ads = []
    for ad in ads:
        cleaned_bank = ad.bank.lower().strip()
        for possible_name in white_list:
            if (possible_name.lower() in cleaned_bank or
                    cleaned_bank in possible_name.lower()):
                valid_ads.append(ad)
                break
    return valid_ads


class Main:

    def __init__(self, user: UserData, credentials: Dict[str, str]):
        connection = ConnectionLocalBitcoin(credentials)
        adapter = AdapterLocalbitcoin()
        user_for_bot = UserLocalbitcoin(user, connection, adapter)
        self.bot = Bot(user_for_bot, user.name)


def script_main(argv=None):
    # Get values from user
    args = parse_arguments(argv)
    amount = Decimal(
        input(
            "Please, introduce amount you would like to increase/reduce"
        ))
    # Process user value
    is_buy = args.buy

    try:
        own_ads = get_ads_from_file(args.own.strip())
    except FileNotFoundError as e:
        print(f"File Error in {args.own}: {e}")
        return 1
    except KeyError as e:
        print(
            (f"Key Error in {args.own}: {e},"
             f"it should be as the get in /api/ads/"
             "for own user")
        )
        return 1
    except Exception as e:
        print(f"Error in {args.own}: {e}")
        return 1

    try:
        partner_ads = get_ads_from_file(args.partner.strip())
    except FileNotFoundError as e:
        print(f"File Error in {args.partner}: {e}")
        return 1
    except KeyError as e:
        print(
            (f"Key Error in {args.partner}: {e},"
             f"it should be as the get in /api/ads/"
             "for partner user")
        )
        return 1
    except Exception as e:
        print(
            (f"Error in {args.partner}: {e},"
             f"data should be as the get in /api/ads/"
             "for partner user")
        )
        return 1

    try:
        bank_name = get_banks_from_file(args.list.strip())
    except FileNotFoundError as e:
        print(f"File Error in {args.list}: {e}")
        return 1
    except KeyError as e:
        print(f"Key Error in {args.list}: {e} and"
              " it should be a list of object with "
              'attribute "banks"')
        return 1
    except Exception as e:
        print(f"Error in {args.list}: {e}")
        return 1

    team_ads = own_ads + partner_ads
    credential = {"hmac_key": args.key,
                  "hmac_secret": args.secret}
    user = UserData(args.username.strip(), args.name)

    # Create instance Main
    main = Main(user, credential)

    # update prices
    # Getting publications
    try:
        all_ads = main.bot.read_buy_ads() if is_buy \
            else main.bot.read_sell_ads()
    except (ConnectionError, Exception) as e:
        print(f"Error {e}")
        return 1

    # Filter to leave only rivals
    for ad in own_ads:
        filtered_ads_by_price = main.bot.filter_list_ads(
            ad.minimum_value, ad.maximum_value, all_ads
        )
        filtered_team_ads = main.bot.remove_own_ads(
            filtered_ads_by_price, [ad.id for ad in team_ads]
        )
        filtered_final = filter_banks(
            filtered_team_ads, bank_name)
        # No competitors
        if not filtered_final:
            continue
        if is_buy:
            target_price = main.bot.get_smaller_price(
                filtered_final) + amount
        if not is_buy:
            target_price = main.bot.get_bigger_price(
                filtered_final) + amount
        try:
            response = main.bot.update_price_ads(own_ad=ad,
                                                 update_price=target_price)
        except (ConnectionError, Exception) as e:
            print(f"Error {e} with ad {ad.id} during updation")
        else:
            if not response:
                print(f"Fail to update ad {ad.id}")
    return 0


if __name__ == "__main__":
    exit(script_main())
