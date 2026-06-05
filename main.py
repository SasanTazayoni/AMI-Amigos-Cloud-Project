"""
Create a Python application that:
- Extracts the data from an api or csv
- Stores the data in MongoDB
- Serializes data into JSON
- Uploads exported data to an S3 bucket as json files
"""
import requests
import pymongo
import boto3

def get_all_pokemon(limit=1):
    try:
        response = requests.get(f'https://pokeapi.co/api/v2/pokemon?limit={limit}')
        return response.json()['results']
    
    except Exception as e: 
        print(f'Error {e}')
        return 


def get_pokemon_details():
    all_pokemon = get_all_pokemon()
    for pokemon in all_pokemon:
        try:
            response = requests.get(pokemon['url'])
            details = response.json()

            pokemon['details'] = response.json()

            # pokemon['details'] = {
            #     'id': details['id'],
            #     'name': details['name'],
            #     'height': details['height'],
            #     'weight': details['weight'],
            #     'base_experience': details['base_experience']
            # }


        except Exception as e: 
            print(f'Error {e}')

    return all_pokemon

class S3: 
    def __init__(self, bucket_name = "se-data-with-ai-etl-project"): 
        self.s3_client = boto3.client('s3')
        self.s3_resource = boto3.resource('s3')
        self.bucket_name = bucket_name

    def upload_data(self, data, file_name):
        try:
            self.s3_client.put_object(
                Body = data,
                Bucket = self.bucket_name,
                Key = "AMI-Amigos/" + file_name
            )
            return True
        
        except Exception as e: 
            print(f'Error: {e}')
            return False


class Mongo:
    def __init__(self):
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        db = client["pokemon_db"]
        self.pokemon = db["pokemon"]

    def read_data(self, filter): 
        data = self.pokemon.find(filter)
        return data 
    
    def upload_data(self, data):
        self.pokemon.insert_many(data)
        return True

    def update_data(self, data, filter): 
        self.pokemon.update_many(data, filter)
        return True 

    def delete_data(self, filter):
        self.pokemon.delete_many(filter)
        return True

    def reset(self):
        self.pokemon.delete_many({})
        return True


if __name__=='__main__':
    data=get_pokemon_details()
    db = Mongo() 
    db.reset()
    db.upload_data(data)
