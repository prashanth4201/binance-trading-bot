from binance.client import Client
import os
import time
from dotenv import load_dotenv

load_dotenv()

def get_client():
    client = Client(
        os.getenv("API_KEY"),
        os.getenv("API_SECRET")
    )
    client.FUTURES_URL = "https://testnet.binancefuture.com/fapi"
    server_time = client.get_server_time()['serverTime']
    local_time = int(time.time() * 1000)
    client.timestamp_offset = server_time - local_time

    return client