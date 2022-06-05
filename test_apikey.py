from time import sleep
from kiteconnect import KiteConnect
import pandas as pd
from datetime import datetime, timedelta, time
from selenium import webdriver
from sqlalchemy import create_engine

time_end = datetime.now() + timedelta(minutes=1)


def test_time_loop(true=None):
    while datetime.now() < time_end:
        api_key()


def api_key():
    ak = 'API Key'
    ask = 'Secret API'
    kite = KiteConnect(api_key=ak)
    requst_tkn = set_up()
    print(requst_tkn)
    data = kite.generate_session(requst_tkn, api_secret=ask)
    kite.set_access_token(data["access_token"])
    # print(data['access_tkn'])
    trd_portfolio = {'INFY': {'token': 408065}}
    token = "408065"
    to_date = datetime.now()
    from_date = to_date - timedelta(minutes=2)
    interval = "minute"
    records = kite.historical_data(token, from_date, to_date, interval)
    df = pd.DataFrame(records)
    df.to_csv("datatest.csv", mode='a')

    # create sqlalchemy engine
    engine = create_engine("mysql+pymysql://{user}:{pw}@localhost/{db}"
                           .format(user="username",
                                   pw="pw",
                                   db="db name"))
    # Insert whole DataFrame into MySQL
    df.to_sql('data67', con=engine, if_exists='append', chunksize=100000, index=False)
    print(data.to_sql)

    print(records)
    print(df)


def set_up():
    driver = webdriver.Chrome("chromedriver location")
    # URL of the website
    url = "https://kite.trade/connect/login?api_key=API key"
    driver.get("https://kite.trade/connect/login?api_key=API key")
    # driver.minimize_window()
    z_userid = "userid"
    z_pwd = "password"
    z_pin = "pin"
    # Set username
    sleep(2)
    inputElement = driver.find_element_by_id("userid")
    inputElement.send_keys(z_userid)
    # Set password
    pwdElement = driver.find_element_by_id("password")
    pwdElement.send_keys(z_pwd)
    # Login
    inputElement.submit()

    # Set PIN (6 digit)
    sleep(4)
    pwdElement = driver.find_element_by_id("pin")
    pwdElement.send_keys(z_pin)
    pwdElement.submit()

    # Getting current URL
    sleep(5)
    get_url = driver.current_url
    # Printing the URL
    print(get_url)
    print(get_url.split("request_token=")[-1].split('&')[0])
    access_token = get_url.split("request_token=")[-1].split('&')[0]
    return access_token
