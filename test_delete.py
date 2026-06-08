import pymongo

def test_delete():
    try:
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        collection = client["pokemon_db"]["pokemon"]
        collection.delete_many({"name": "testmon"})
        result = list(collection.find({"name": "testmon"}))
        print("Deleted, remaining:", result)
    except Exception as e:
        print(f"Delete failed: {e}")

if __name__ == '__main__':
    test_delete()
