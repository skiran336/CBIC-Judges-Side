import pymongo
import certifi

url = 'mongodb+srv://Hornets:Hornets123@cbic.jstg3wg.mongodb.net/'

try:
    client = pymongo.MongoClient(url, tlsCAFile=certifi.where())  # 5 seconds timeout
    client.server_info()  # Force connection on a request as the constructor does not connect.
except pymongo.errors.ServerSelectionTimeoutError as err:
    # Do something with the error
    print("Failed to connect to server:", err)

db = client['studentform']

student_collection = db['studentforms']



