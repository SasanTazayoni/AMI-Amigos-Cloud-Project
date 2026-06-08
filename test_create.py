import pymongo

def test_create():
    try:
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        collection = client["pokemon_db"]["pokemon"]
        collection.insert_many([{"name": "testmon", "url": "http://test.com"}])
        result = list(collection.find({"name": "testmon"}))
        print("Created:", result)
    except Exception as e:
        print(f"Create failed: {e}")

if __name__ == '__main__':
    test_create()
