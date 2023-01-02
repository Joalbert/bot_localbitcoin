import argparse

from user.localbitcoin import UserLocalbitcoin
from adapters.localbitcoin import AdapterLocalbitcoin
from connection.localbitcoin import ConnectionLocalBitcoin
from models import UserData, Ad

from bot import Bot

def parse_arguments(args):
    """ Create args for run from termninal"""
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
    return parser.parse_args(args)

def main(argv=None):
    args = parse_arguments(argv)
    credential = {"hmac_key": args.key,
                  "hmac_secret": args.secret}
    user = UserData(args.username.strip(), args.name)

    connection = ConnectionLocalBitcoin(credential)
    adapter = AdapterLocalbitcoin()
    user_for_bot = UserLocalbitcoin(user, connection, adapter)
    bot = Bot(user_for_bot, user.name)
    own_ads = bot.read_my_ads()
    with open("own_ads.json","+w") as f:
        f.write(own_ads)


if __name__ == "__main__":
    main()
