import sys
import pyotp
from kiteconnect import KiteConnect
from urllib.parse import urlparse, parse_qs
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

totp_key = 'Your TOTP key'
username = 'Your username'  # ZYXXXX
password = 'Your password'
api_key = 'API key'
client_secret = 'API secret'

kite = KiteConnect(api_key=api_key)


def read_file():
    with open("token.txt", "r") as f:
        token = f.read()
    return token


def write_file(token):
    with open('token.txt', 'w') as f:
        f.write(token)


def setup():
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-notifications")
    options.add_argument('--headless')
    driver = webdriver.Chrome('chromedriver.exe', options=options)
    driver.get('https://kite.trade/connect/login?api_key=' + api_key)

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id=\"userid\"]"))).send_keys(username)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id=\"password\"]"))).send_keys(password)
    driver.find_element_by_xpath("//*[@id=\"container\"]/div/div/div/form/div[4]/button").click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id=\"totp\"]"))).send_keys(pyotp.TOTP(totp_key).now())
    driver.find_element_by_xpath("//*[@id=\"container\"]/div/div/div[2]/form/div[3]/button").click()
    WebDriverWait(driver, 10).until((EC.url_changes(driver.current_url)))

    parsed = urlparse(driver.current_url)
    request_token = parse_qs(parsed.query)['request_token'][0]
    access_token = kite.generate_session(request_token, api_secret=client_secret)['access_token']
    kite.set_access_token(access_token)
    write_file(access_token)
    print('Got the access token!!!')
    print(kite.profile())


def check():
    try:
        token = read_file()
    except FileNotFoundError:
        print('Getting the access token!')
        setup()
        sys.exit()
    kite.set_access_token(token)
    try:
        profile = kite.profile()
        print('You already have a access token!')
        print(profile)
    except (Exception,):
        print('Getting the access token!')
        setup()


if __name__ == '__main__':
    check()
