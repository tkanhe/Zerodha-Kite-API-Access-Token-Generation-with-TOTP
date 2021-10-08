# Zerodha Kite API Access Token Generation with TOTP

First, you will have to register for 2Factor TOTP on the Zerodha Kite website. While enabling TOTP, you have to scan the QR code using Google or Microsoft Authenticator and copy the TOTP KEY, as shown in the figure below.

![alt text](https://github.com/tkanhe/Zerodha-Kite-API-Access-Token-Genereation-with-TOTP/blob/main/Capture.PNG?raw=true)

### Method1 (Without Selenium Webdriver): 
- With the help of the *get-post requests session*, we can get the access token.

#### Dependencies: 
- PyOTP  ```pip install pyotp```
- Kiteconnect  ```pip install kiteconnect```


### Method2 (With Selenium Webdriver):
- Download the appropriate (as per your Google Chrome version) selenium chrome webdriver from https://chromedriver.chromium.org/downloads. 
- Put the ***chromedriver.exe*** file in the same folder as the script.

#### Dependencies: 
- Selenium  ```pip install selenium```
- PyOTP  ```pip install pyotp```
- Kiteconnect  ```pip install kiteconnect```


*For more info about what TOTP is and its registration procedure, please refer to this: https://tradewithpython.com/totp-login-zerodha-kiteconnect*.
