import pymongo
import certifi

url = 'mongodb+srv://Hornets:Hornets123@cbic.jstg3wg.mongodb.net/'

try:
    client = pymongo.MongoClient(url, tlsCAFile=certifi.where())
    db = client['studentform']
    collection = db['studentforms']
    # Fetch the first document in the collection
    student = collection.find_one()
    if student:
        print("Data retrieved:", student)
    else:
        print("No data found in the collection.")
except pymongo.errors.ServerSelectionTimeoutError as err:
    print("Failed to connect to server:", err)
except Exception as e:
    print("An error occurred:", e)
