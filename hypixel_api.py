import requests
import json
from verification import *
from keys import API_KEY
api_url = "https://api.hypixel.net/v2/resources/skyblock/"
floorReqs = [24, 24, 24, 28, 30, 38] #Floor requirements, change as see fit
slayerReqs = [8, 7, 7, 7] #Slayer requirements, change as see fit

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
    if slayer_type.lower() == "revenant":
        slayer_type = "zombie"
    elif slayer_type.lower() == "tarantula":
        slayer_type = "spider"
    elif slayer_type.lower() == "sven":
        slayer_type = "wolf"
    elif slayer_type.lower() == "voidgloom":
        slayer_type = "enderman"
    xp = get_slayer_xp(player_name, slayer_type)
    if xp >= 100000:
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

    level = get_level(player_name)
    if floor >=1 and floor <=3:
        if level >= floorReqs[floor-1]:
            
            return True, level
        else:
            return False, level
    else:
        return False, level

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
    finally: 
        if(len(guild_members)>0):
            return guild_members
        else:
            return False

CATACOMBS_XP = {
    15: 25340,
    16: 35640,
    17: 50040,
    18: 70040,
    19: 97640,
    20: 135640,
    21: 188140,
    22: 259640,
    23: 356640,
    24: 488640,
    25: 668640,
    26: 911640,
    27: 1239640,
    28: 1684640,
    29: 2284640,
    30: 3084640,
    31: 4149640,
    32: 5559640,
    33: 7459640,
    34: 9959640,
    35: 13259640,
    36: 17559640,
    37: 23159640,
    38: 30359640,
    39: 39559640,
    40: 51559640,
}


def get_level(player_name):
    xp = get_cata_xp(player_name)

    level = 0
    for lvl, required_xp in sorted(CATACOMBS_XP.items()):
        if xp >= required_xp:
            level = lvl
        else:
            break
    return level


if __name__ == "__main__":
    print(len(get_guild_members('Spruce')))