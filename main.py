import requests
from bs4 import BeautifulSoup
import smtplib
from dotenv import load_dotenv
import os

load_dotenv()

my_email = os.getenv("EMAIL")
password = os.getenv("PASSWORD")

header = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-GB,de;q=0.8,fr;q=0.6,en;q=0.4,ja;q=0.2",
    "Dnt": "1",
    "Priority": "u=1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Sec-Gpc": "1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:126.0) Gecko/20100101 Firefox/126.0",
}

response = requests.get("https://www.amazon.co.uk/Anker-High-Speed-Portable-Charger-Battery/dp/B0CZ9LH53B/?_encoding=UTF8&pd_rd_w=kgni8&content-id=amzn1.sym.1f37f23b-2d9d-4a08-a684-d27dce7c5378&pf_rd_p=1f37f23b-2d9d-4a08-a684-d27dce7c5378&pf_rd_r=7QXDGBFE70N5P855BJ2A&pd_rd_wg=Wzq8a&pd_rd_r=ed263194-bf1e-41a3-a635-b14e474c36b8&ref_=pd_hp_d_atf_dealz_cs", headers=header)
amazon_webpage = response.text

soup = BeautifulSoup(amazon_webpage,"html.parser")
# print(soup)
price_whole = soup.find("span", class_= "a-price-whole")
# print(price_whole)

price_fraction = soup.find("span",class_="a-price-fraction")
# price_fraction = "0"
price = 0
target = 100
if price_fraction:
    price = float(price_whole.getText() + price_fraction.getText())
else:
    price = int(price_whole.getText().split(".")[0])
print(price)
if price < target:
    print("send email")
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(my_email, password)
        connection.sendmail(from_addr=my_email,
                            to_addrs="ritujane78@gmail.com",
                            msg=f"Subject: Price Drop!!!\n\n The price you want has dropped to {price}")
