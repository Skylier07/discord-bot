import requests
import json
from verification import *
from keys import API_KEY
api_url = "https://api.hypixel.net/v2/resources/skyblock/"
floorReqs = [19, 21, 24, 27, 30, 35] # Need to change into xp
floorReqs = [97640, 188140, 488640, 1239640, 3084640, 13259640]

def get_player_profiles(player_name=None, uuid=None):
    url = f"https://api.hypixel.net/v2/skyblock/profiles?key={API_KEY}"
    if not player_name and not uuid:
        return None
    
    if not uuid:
        uuid = get_uuid(player_name)

    # Use total XP to find level
    try:
        params = {"uuid": uuid}
        response = requests.get(url, params=params)

        response.raise_for_status()  
        profiles = response.json()["profiles"]
        return profiles
    except requests.exceptions.HTTPError as errh:
        print("HTTP Error:", errh)
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:", errc)
    except requests.exceptions.Timeout as errt:
        print("Timeout Error:", errt)
    except requests.exceptions.RequestException as err:
        print("Oops: Something went wrong", err)

def get_slayer_xp(player_name, slayer):
    uuid = get_uuid(player_name)


    profiles = get_player_profiles(uuid=uuid)
    xps=[]
    for profile in profiles:
        try: 
            # print(profile['members'][uuid]['slayer'])
            xps.append(profile['members'][uuid]['slayer']['slayer_bosses'][slayer]['xp'])
        except Exception as e:
            # print(f"Error:{e}")
            pass
    
    return max(xps)

def check_reqs_slayer(player_name, slayer_type: str):
    xp = get_slayer_xp(player_name, slayer_type)
    if xp >= 20000:
        return True, humanize_xp(xp)
    else:
        return False, humanize_xp(xp)

def get_cata_xp(player_name):
    uuid = get_uuid(player_name)

    profiles = get_player_profiles(uuid=uuid)

    xps=[]
    try:
        for profile in profiles:
            try: 
                xps.append(profile['members'][uuid]['dungeons']['dungeon_types']['catacombs']['experience'])


            except Exception as e:
                pass

        return max(xps)
    except Exception as e:
        print("API Key Expired")

def humanize_xp(xp: int) -> str:
    if xp >= 1_000_000:
        return f"{xp / 1_000_000:.1f}M"
    elif xp >= 1_000:
        return f"{xp / 1_000:.1f}k"
    else:
        return str(xp)

def check_reqs_dungeon(player_name, floor: int):

    xp = get_cata_xp(player_name)
    if floor >=1 and floor <=6:
        if xp >= floorReqs[floor-1]:
            
            return True, humanize_xp(xp)
        else:
            return False, humanize_xp(xp)
    else:
        return False, humanize_xp(xp)

def get_skyblock_level(player_name):
    uuid = get_uuid(player_name)


    profiles = get_player_profiles(uuid=uuid)
    xps=[]
    for profile in profiles:
        try: 
            xps.append(profile['members'][uuid]['leveling']['experience'])
        except Exception as e:
            continue
    
    return max(xps)//100

def get_guild_members(guild_name):
    url = f'https://api.hypixel.net/v2/guild?key={API_KEY}&name={guild_name}'
    try:
        response = requests.get(url)

        response.raise_for_status()  
        members = response.json()['guild']['members']
        guild_members = []
        for member in members:
            guild_members.append(member['uuid'])
        return guild_members
    except requests.exceptions.HTTPError as errh:
        print("HTTP Error:", errh)
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:", errc)
    except requests.exceptions.Timeout as errt:
        print("Timeout Error:", errt)
    except requests.exceptions.RequestException as err:
        print("Oops: Something went wrong", err)

if __name__ == "__main__":
    print(len(get_guild_members('Spruce')))