from investopedia_simulator_api.investopedia_api import InvestopediaApi, TradeExceedsMaxSharesException
import json
import datetime
import math

# sys.path.append('./investopedia_simulator_api')

def buy_stock(ticker, limit):

    credentials = {}
    with open('credentials.json') as ifh:
        credentials = json.load(ifh)
    # look at credentials_example.json
    # credentials = {"username": "you@example.org", "password": "yourpassword" }
    client = InvestopediaApi(credentials)

    p = client.portfolio

    print("account value: %s" % p.account_value)
    print("cash: %s" % p.cash)
    print("buying power: %s" % p.buying_power)
    print("annual return pct: %s" % p.annual_return_pct)
    print("---------------------")



    lookup = client.get_stock_quote(ticker)
    share_number = math.floor( limit / lookup.last) 
    
    print("New trade!")
    print("Ticker: %s",ticker )
    print("Shares: %s", share_number )
    print("Total Cost: %s", share_number*lookup.last)

    # construct a trade (see trade_common.py and stock_trade.py for a hint)
    trade1 = client.StockTrade(symbol=ticker, quantity=share_number, trade_type='buy',
                               order_type='market', duration='good_till_cancelled', send_email=True)
    # validate the trade
    trade_info = trade1.validate()
    print(trade_info)

    # # change the trade to a day order
    # trade1.duration = 'day_order'
    # # Another way to change the trade to a day order
    # trade1.duration = client.TradeProperties.Duration.DAY_ORDER()

    # # make it a limit order
    # trade1.order_type = 'limit 20.00'
    # # alternate way
    # trade1.order_type = client.TradeProperties.OrderType.LIMIT(20.00)

    # validate it, see changes:
    trade_info = trade1.validate()
    if trade1.validated:
        print(trade_info)
        trade1.execute()



    client.refresh_portfolio()
