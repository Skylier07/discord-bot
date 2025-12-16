import requests
import time
from keys import JERRY_API_KEY

retry_delay = 3

def check_scammer_id(id):
     url = f"https://jerry.robothanzo.dev/v1/scammers/discord/{id}?key={JERRY_API_KEY}"
     for attempt in range(10):
        try:
            resp = requests.get(url)
            is_scammer = resp.json()["scammer"]



            return is_scammer

        except (requests.exceptions.JSONDecodeError, ValueError) as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < 9:
                time.sleep(retry_delay)
            else:
                print("All retry attempts failed.")
                return None



if __name__ == "__main__":
    print(check_scammer_id(762876001877229588))