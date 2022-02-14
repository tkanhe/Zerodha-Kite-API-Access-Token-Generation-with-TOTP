import pyotp
import requests
import sys
from urllib.parse import urlparse, parse_qs
from kiteconnect import KiteConnect

totp_key = "Your TOTP key"
username = "Your username"
password = "Your password"
api_key = "API key"
client_secret = "API secret"

kite = KiteConnect(api_key=api_key)


def read_file():
    with open("token.txt", "r") as f:
        token = f.read()
    return token


def write_file(token):
    with open("token.txt", "w") as f:
        f.write(token)


def setup():
    session = requests.Session()
    request_id = session.post("https://kite.zerodha.com/api/login", {"user_id": username, "password": password}).json()["data"]["request_id"]
    session.post("https://kite.zerodha.com/api/twofa", {"user_id": username, "request_id": request_id, "twofa_value": pyotp.TOTP(totp_key).now()})
    api_session = session.get(f"https://kite.trade/connect/login?api_key={api_key}")
    parsed = urlparse(api_session.url)
    request_token = parse_qs(parsed.query)["request_token"][0]
    access_token = kite.generate_session(request_token, api_secret=client_secret)["access_token"]
    kite.set_access_token(access_token)
    write_file(access_token)
    print("Got the access token!!!")
    print(kite.profile())


def check():
    try:
        token = read_file()
    except FileNotFoundError:
        print("Getting the access token!")
        setup()
        sys.exit()
    kite.set_access_token(token)
    try:
        profile = kite.profile()
        print("You already have a access token!")
        print(profile)
    except (Exception,):
        print("Getting the access token!")
        setup()


if __name__ == "__main__":
    check()
