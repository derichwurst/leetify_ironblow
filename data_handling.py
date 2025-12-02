import os.path

import pandas as pd
import random
import leetify
import pickle

# Dies sind die SteamIDs, deren Daten du darstellen möchtest
STEAM_IDS = [
    76561197983756284,  # Narf
    76561197961677583,  # jürgen
    76561197971163179,  # markus
    76561197981396218,  # max
    76561198825927278,  # julian
    76561198262480978   # Basti
]


def store_new_player_data():
    for steam_in in STEAM_IDS:
        lettify_obj = leetify.LeetifyAPIClient()
        player_data = lettify_obj.get_player_profile(steam_in)

        # create path
        full_path = os.path.join("player_data", str(steam_in)+"-"+player_data["name"])

        # check if folder is ready
        os.makedirs("player_data", exist_ok=True)

        # dump that shit
        try:
            with open(full_path, "wb") as f:
                pickle.dump(player_data, f)

            print(str(steam_in)+"-"+player_data["name"] + " stored.")
            #return True
        except Exception as e:
            print(f"❌ Fehler beim Speichern: {e}")
            #return False


def get_all_player_data():
    all_play_data = []

    for file_name in os.listdir("player_data"):
        full_path = os.path.join("player_data", file_name)
        try:
            with open(full_path, "rb") as f:
                player_data = pickle.load(f)
        except Exception as e:
            print(f"❌ Fehler beim Laden von {file_name}: {e}")
            return None

        if player_data is not None:
            all_play_data.append(player_data)
            print(f"✅ Geladen: {file_name}")
        else:
            # Fehlermeldungen werden bereits in load_data_pickle ausgegeben
            print(f"⚠️ Übersprungen: {file_name} (Ladefehler)")

    return all_play_data


def get_data_for_dashboard():
    """Ruft die Statistiken für alle vordefinierten SteamIDs ab und gibt sie als DataFrame zurück."""
    all_stats = []

    for player in get_all_player_data():
        stats = {
            "Name": player["name"],
            "SteamID": player["steam64_id"],
            "Aim_Rating": player["rating"]["aim"],
            "Utility_Rating": player["rating"]['utility'],
            "Opening_Kill_Success": player["rating"]["opening"] * 1000,
            "Clutch_Percentage": player["rating"]["clutch"],
            "Positioning_Rating": player["rating"]["positioning"],
            "Leetify_Rating": (player["rating"]["ct_leetify"] + player["rating"]["t_leetify"]) / 2,
            "Headshot_Percentage": player["stats"]["accuracy_head"]
        }

        all_stats.append(stats)

    # Konvertiere die Liste der Dictionaries in einen Pandas DataFrame
    df = pd.DataFrame(all_stats)
    return df


