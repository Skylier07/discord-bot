from pymongo import MongoClient
import requests
from keys import FULL_API_KEY, MONGO_URI

mongo_client = MongoClient(MONGO_URI)
db = mongo_client['Delerious']
users_collection = db['users']


def get_user_discord(username):
    try:
        uuid=get_uuid(username)
        hypixel_user= requests.get(f"https://api.hypixel.net/player?key={FULL_API_KEY}&uuid={uuid}")
        discord = hypixel_user.json()['player']['socialMedia']['links']['DISCORD']
        return discord

    except KeyError as e:
        return None

def get_uuid(username):
    resp = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{username}")
    try:
        uuid = resp.json()["id"]
        return uuid
    except KeyError as e:
        return None

def get_uuid_with_discord(discord_id):
    try: 
        ign = users_collection.find_one({"id": discord_id})['username']
        uuid = get_uuid(ign)
        return uuid
    except TypeError as e:
        print(discord_id)
        return 0

def get_discord_with_uuid(uuid):
    try:
        hypixel_user= requests.get(f"https://api.hypixel.net/player?key={FULL_API_KEY}&uuid={uuid}")
        discord = hypixel_user.json()['player']['socialMedia']['links']['DISCORD']
        discord_id = users_collection.find_one({"discord_tag": discord})['id']

        return discord_id

    except Exception:
        return None


if __name__ == "__main__":
    print(get_user_discord("Automonized"))