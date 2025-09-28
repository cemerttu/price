# import os
# from dotenv import load_dotenv
# import oandapyV20
# import oandapyV20.endpoints.pricing as pricing
# import oandapyV20.endpoints.orders as orders

# # Load API credentials
# load_dotenv()
# API_KEY = os.getenv("OANDA_API_KEY")
# ACCOUNT_ID = os.getenv("OANDA_ACCOUNT_ID")
# OANDA_ENV = os.getenv("OANDA_ENV", "practice")

# # OANDA API client
# client = oandapyV20.API(access_token=API_KEY)

# class OandaBroker:
#     def __init__(self, client, account_id):
#         self.client = client
#         self.account_id = account_id

#     def get_price(self, instrument="EUR_USD"):
#         """Fetch the latest bid/ask price"""
#         params = {"instruments": instrument}
#         r = pricing.PricingInfo(accountID=self.account_id, params=params)
#         self.client.request(r)
#         price_data = r.response["prices"][0]
#         bid = float(price_data["bids"][0]["price"])
#         ask = float(price_data["asks"][0]["price"])
#         return bid, ask

#     def place_order(self, instrument="EUR_USD", units=100):
#         """Place a market order (units > 0 = buy, < 0 = sell)"""
#         order_data = {
#             "order": {
#                 "instrument": instrument,
#                 "units": str(units),
#                 "type": "MARKET",
#                 "positionFill": "DEFAULT"
#             }
#         }
#         r = orders.OrderCreate(accountID=self.account_id, data=order_data)
#         self.client.request(r)
#         return r.response
