import pymongo

def test_update():
    try:
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        collection = client["pokemon_db"]["pokemon"]
        collection.update_many({"name": "testmon"}, {"$set": {"url": "http://updated.com"}})
        result = list(collection.find({"name": "testmon"}))
        print("Updated:", result)
    except Exception as e:
        print(f"Update failed: {e}")

if __name__ == '__main__':
    test_update()
