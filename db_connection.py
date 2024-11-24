import pymongo
from urllib.parse import quote_plus


username = quote_plus('rajan123')  # URL encode the username
password = quote_plus('Rajan@123')  # URL encode the password

url = f'mongodb+srv://rajan123:Rajan@123@inventory.yk7ml.mongodb.net/'
client = pymongo.MongoClient(url)

db=client['inventory']
