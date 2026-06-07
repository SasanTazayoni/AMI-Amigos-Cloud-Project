import pymongo

def test_read():
    try:
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        collection = client["pokemon_db"]["pokemon"]
        result = list(collection.find({"name": "testmon"}))
        print("Read:", result)
    except Exception as e:
        print(f"Read failed: {e}")

if __name__ == '__main__':
    test_read()
