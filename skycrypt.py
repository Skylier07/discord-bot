import requests
import json

floorReqs = [19, 21, 24, 27, 30, 35]


def get_player_profile(player_name, feature, profile=None):
    api_url = "https://sky.shiiyu.moe/api/v2"
    if profile:
        endpoint = f"/{feature}/{player_name}/{profile}"
    else:
        endpoint = f"/{feature}/{player_name}"

    full_url = api_url + endpoint

    try:
        response = requests.get(full_url)
        response.raise_for_status()  
        return response.json()
    except requests.exceptions.HTTPError as errh:
        print("HTTP Error:", errh)
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:", errc)
    except requests.exceptions.Timeout as errt:
        print("Timeout Error:", errt)
    except requests.exceptions.RequestException as err:
        print("Oops: Something went wrong", err)


def extract_catacombs_level(player_name, feature):

        
    try:
        player_json=get_player_profile(player_name, feature)
        # cute_names = [profile['cute_name'] for profile in player_json['profiles'].values()]
        profile_ids = list(player_json['profiles'].keys())
        max_level = 0
        for id in profile_ids:
            # Check if 'dungeons' -> 'catacombs' -> 'level' exist for this profile
            if 'dungeons' in player_json['profiles'][id] and \
            'catacombs' in player_json['profiles'][id]['dungeons'] and \
            'level' in player_json['profiles'][id]['dungeons']['catacombs']:
            
                xp_data = player_json['profiles'][id]['dungeons']['catacombs']['level']['level']
                
                # Check if 'level' is not None and compare it to max_level
                if xp_data is not None and int(xp_data) > max_level:
                    max_level = int(xp_data)
        
        return max_level
    except KeyError:
        print("Error: Player hasn't entered the catacombs")
        return 0
    except Exception as e:
        print(e)
        return 0

def check_reqs_dungeon(floor: int, player_name):
    level = extract_catacombs_level(player_name, "dungeons")
    if floor >=1 and floor <=6:
        if level >= floorReqs[floor-1]:
            return True, level
        else:
            return False, level
    else:
        return False, level
def extract_slayer_level(player_name, slayer_type):
    try:
        player_json=get_player_profile(player_name, "slayers")
        # cute_names = [profile['cute_name'] for profile in player_json['profiles'].values()]

        max_level = max(
            profile['data']['slayers'][slayer_type]['level']['currentLevel'] 
            for profile in player_json.values()
            if 'data' in profile and 'slayers' in profile['data'] and slayer_type in profile['data']['slayers']
        )


        print(max_level)
        return max_level
    except KeyError as e:
        print(player_json)
        print(f"an error occurred {e}")
        return 0
    except Exception as e:
        print(player_json)
        print(f"an error occurred {e}")
        return 0

def check_reqs_slayer(player_name, slayer_type: str):
    level = extract_slayer_level(player_name, slayer_type)
    if level >= 6:
        return True, level
    else:
        return False, level

if __name__ == "__main__":
    print(check_reqs_slayer("Skyzei_", "zombie"))
    