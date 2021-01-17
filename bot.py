# coding=utf-8
''' arbitrage.py

Bot som handlar cryptos vid arbitrage-tillfällen. 
Hur fungerar boten?
Kollar olika exchanges samtidigt. Om den upptäcker ett arbitragetillfälle 
så köper den köper den och säljer valutorna på ett fördelaktigt sätt.

Den kommer att ta värden från Binance. Där hittar den priser för valutor
på olika marknader. Binance streamar data genom något som kallas för en websocket.
Det man då kan göra är att ansluta till en sådan och konstant få in data istället
för att hela tiden behöva skicka http requests. Den skickar all nödvändig data som 
boten behöver för att göra sina moves vid lämpliga tillfällen. Vi kommer använda
Pythons WebSocketClient för att ansluta till denna stream. Vi kommer även använda 
Binance för att köpa och sälja valutor.

Modulen cryptofeed verkar vara ett bra alternativ.

URL för docs: https://github.com/bmoscon/cryptofeed/blob/master/docs/README.md

Skrivet av: Martin Svärdsjö, David Svensson. 2021
฿฿฿฿฿฿฿฿฿฿฿฿฿฿฿฿฿฿฿฿฿฿฿฿฿฿฿฿฿

CCXT = CryptoCurrency eXchange Trading.
Denna kan vi använda för att för att handla mellan exchanges.
'''

from requests import status_codes
import websocket, json, pprint, ccxt, time, requests
from binance.client import Client
from cryptofeed import FeedHandler
from cryptofeed.exchanges import Coinbase, Gemini, Kraken
from datetime import datetime

# För data via BINANCE API
RSI_PERIOD = 14
OVERSOLD_THRESHOLD = 30
OVERBOUGHT_THRESHOLD = 70
TRADE_QUANTITY = 0.01
TRADE_SYMBOL = 'ETHPAX'
FEE = 0.1
SOCKET = "wss://stream.binance.com:9443/ws/ethusdt@kline_1m"

# https://api.binance.com/api/v1/ticker/price?symbol=LTCBTC

def run():
    stnk_number = 0
    opportunity_list = []
    best_op = 0
    while True:
        direct_ex = float(bn_client.get_symbol_ticker(symbol = TRADE_SYMBOL)['price'])
        for symbols in currency_pairs:
            print(symbols)
            arb_percentage = (from_to(symbols) / direct_ex)*100 - (FEE*3)
            if arb_percentage > 100:
                opportunity = True
            else:
                opportunity = False
            if arb_percentage > best_op:
                print("Record!")
                best_op = arb_percentage
            print(arb_percentage, end="")
            if opportunity:
                dt = datetime.now()
                stnk_number += 1
                print_string = f"{dt.strftime('%d%m%Y %H:%M:%S')}"
                print(print_string)
                opportunity_list.append(print_string + " " + str(arb_percentage))
                with open("opp.txt","w") as txt_file:
                    for line in opportunity_list:
                        txt_file.write(line)
                
                
            else:
                print()
        time.sleep(0.5);

        

def from_to(symbol):
    '''
    Get frm/to and compare to (from/via) * (via/to). If the
    latter gives a higher value than the former then the trade could be
    potentially worthwhile.
    '''
    first, second = symbol
    first_price = bn_client.get_symbol_ticker(symbol = first)['price']
    second_price = bn_client.get_symbol_ticker(symbol = second)['price']
    return float(first_price) * float(second_price)



currency_pairs = [
    ['ETHBTC', 'BTCPAX'],
]
api_key = "zVfkDxlQTGaOs34NZw9onfVw75HXgHSuj70gdQlGdWa8RA8XxQnc7VNq1y10zgX4"
secret_key = "qIizDwjHHSQc5JFtWVTc7USUOlj6HmQeHGApiCTyzuwsaNn4ILeDD635AaJcLAQ3"
bn_client = Client(api_key=api_key, api_secret= secret_key)
run()