import os.path
import pandas as pd
import pickle


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


def get_all_rating():
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


def get_all_aim_stats():
    weapon_stats = []
    for player in get_all_player_data():
        stats = {
            "Name": player["name"],
            "SteamID": player["steam64_id"],
            "accuracy_enemy_spotted": player["stats"]["accuracy_enemy_spotted"],
            "counter_strafing_good_shots_ratio": player["stats"]["counter_strafing_good_shots_ratio"],
            "reaction_time_ms": player["stats"]["reaction_time_ms"],
            "spray_accuracy": player["stats"]["spray_accuracy"],
            "preaim": player["stats"]["preaim"]
        }
        weapon_stats.append(stats)
    df = pd.DataFrame(weapon_stats)
    return df


def get_all_duell_stats():
    weapon_stats = []
    for player in get_all_player_data():
        stats = {
            "Name": player["name"],
            "SteamID": player["steam64_id"],
            "ct_opening_aggression_success_rate": player["stats"]["ct_opening_aggression_success_rate"],
            "ct_opening_duel_success_percentage": player["stats"]["ct_opening_duel_success_percentage"],
            "t_opening_aggression_success_rate": player["stats"]["t_opening_aggression_success_rate"],
            "t_opening_duel_success_percentage": player["stats"]["t_opening_duel_success_percentage"],
        }
        weapon_stats.append(stats)
    df = pd.DataFrame(weapon_stats)
    return df


def get_all_trade_stats():
    weapon_stats = []
    for player in get_all_player_data():
        stats = {
            "Name": player["name"],
            "SteamID": player["steam64_id"],
            "traded_deaths_success_percentage": player["stats"]["traded_deaths_success_percentage"],
            "trade_kill_opportunities_per_round": player["stats"]["trade_kill_opportunities_per_round"],
            "trade_kills_success_percentage": player["stats"]["trade_kills_success_percentage"],
        }
        weapon_stats.append(stats)
    df = pd.DataFrame(weapon_stats)
    return df


def get_all_flash_stats():
    weapon_stats = []
    for player in get_all_player_data():
        stats = {
            "Name": player["name"],
            "SteamID": player["steam64_id"],
            "flashbang_hit_foe_avg_duration": player["stats"]["flashbang_hit_foe_avg_duration"],
            "flashbang_hit_foe_per_flashbang": player["stats"]["flashbang_hit_foe_per_flashbang"],
            "flashbang_hit_friend_per_flashbang": player["stats"]["flashbang_hit_friend_per_flashbang"],
            "flashbang_leading_to_kill": player["stats"]["flashbang_leading_to_kill"],
            "flashbang_thrown": player["stats"]["flashbang_thrown"],
        }
        weapon_stats.append(stats)
    df = pd.DataFrame(weapon_stats)
    return df


def get_all_he_stats():
    weapon_stats = []
    for player in get_all_player_data():
        stats = {
            "Name": player["name"],
            "SteamID": player["steam64_id"],
            "he_foes_damage_avg": player["stats"]["he_foes_damage_avg"],
            "he_friends_damage_avg": player["stats"]["he_friends_damage_avg"],
            "utility_on_death_avg": player["stats"]["utility_on_death_avg"],
        }
        weapon_stats.append(stats)
    df = pd.DataFrame(weapon_stats)
    return df


## debug stuff
# print(get_all_duell_stats())
#
# print(get_all_player_data()[0]["stats"])
