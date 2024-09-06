from pybit.unified_trading import HTTP
from dotenv import load_dotenv
import os

load_dotenv()
proxy = os.getenv("PROXY")
print(proxy)

http = HTTP(

)